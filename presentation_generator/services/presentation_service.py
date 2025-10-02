import sys
import time
import asyncio
from typing import Callable, Optional
from pathlib import Path
from ..models.presentation import Presentation, Section, Slide
from ..services.ai_service import AIService
from ..database.db_manager import DatabaseManager
from ..services.web_search_service import WebSearchService
from ..services.summary_service import SummaryService
from ..generators.pptx_generator import PPTXGenerator
from ..localization.manager import LocalizationManager

def get_resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        return Path(sys._MEIPASS) / relative_path
    else:
        return Path(__file__).parent.parent.parent / relative_path


class PresentationService:
    def __init__(self, api_key: str, ai_model: str = "meta-llama/Llama-3.3-70B-Instruct", output_dir: str = "output", interface_language: str = None):
        if interface_language is None:
            from ..localization.manager import get_localization_manager
            loc = get_localization_manager()
            interface_language = loc.t('language_russian')
        from ..database.settings_manager import SettingsManager
        self.settings = SettingsManager()
        
        ai_model = self.settings.get("ai_model", "meta-llama/Llama-3.3-70B-Instruct")
        
        self.ai_service = AIService(api_key, model=ai_model)
        self.web_search_service = WebSearchService(self.settings)
        self.summary_service = SummaryService(api_key, model=ai_model)
        self.pptx_generator = PPTXGenerator(output_dir=output_dir)
        self.db_manager = DatabaseManager()
        self.loc = LocalizationManager()
        self.loc.set_language(interface_language)
        self.avg_step_time = 5.0
        self.step_times = []
        self.developer_mode = self.settings.get("developer_mode", False)
    
    async def generate_presentation(
        self, 
        title: str, 
        max_sections: int = 3, 
        max_slides: int = 4,
        language: str = None,
        enable_web_search: bool = False,
        progress_callback: Optional[Callable[[str, int, int], None]] = None
    ) -> Presentation:
        if language is None:
            language = self.loc.t('language_russian')
        self.developer_mode = self.settings.get("developer_mode", False)
        
        if progress_callback:
            progress_callback(self.loc.t("initializing"), 0, 1)
        
        from ..utils.project_validator import ProjectValidator
        from pathlib import Path
        
        output_dir = Path("output")
        if not output_dir.exists():
            output_dir.mkdir(exist_ok=True)
        
        validator = ProjectValidator()
        is_valid, errors = validator.validate_project()
        
        if not is_valid:
            for error in errors:
                print(f"{self.loc.t('error_marker')} {error}")
            print(f"\n{self.loc.t('critical_error_stop')}")
            raise Exception(self.loc.t("project_validation_failed"))
        
        presentation = Presentation(
            title=title,
            language=language,
            max_sections=max_sections,
            max_slides=max_slides
        )
        
        web_search_multiplier = 2 if enable_web_search else 1
        total_steps = 2 + max_sections * (1 + max_slides * web_search_multiplier)
        current_step = 1
        start_time = time.time()
        
        if progress_callback:
            progress_callback(self.loc.t("gen_summary"), current_step, total_steps)
        
        step_start = time.time()
        presentation.summary = await self.ai_service.generate_presentation_summary(title, language)
        presentation.title_slide_header = await self.ai_service.generate_title_slide_header(title, language)
        step_duration = time.time() - step_start
        self._update_step_timing(step_duration)
        current_step += 1
        
        if progress_callback:
            remaining_time = self._calculate_remaining_time(current_step, total_steps, start_time)
            progress_callback(f"{self.loc.t('gen_sections')} ({self.loc.t('remaining_time')} ~{self._format_time(remaining_time)})", current_step, total_steps)
        
        self._debug_log(f"{self.loc.t('debug_ai_request')} {self.loc.t('debug_section_titles')}", f"{self.loc.t('debug_title')}: {title}, {self.loc.t('debug_count')}: {max_sections}")
        
        step_start = time.time()
        section_titles = await self.ai_service.generate_section_titles(title, max_sections, language)
        
        self._debug_log(f"{self.loc.t('debug_ai_response')} {self.loc.t('debug_section_titles')}", str(section_titles))
        
        step_duration = time.time() - step_start
        self._update_step_timing(step_duration)
        if not section_titles or len(section_titles) < max_sections:
            section_titles = [f"{self.loc.t('section_default')} {i+1}" for i in range(max_sections)]
        
        for section_index, section_title in enumerate(section_titles):
            if progress_callback:
                remaining_time = self._calculate_remaining_time(current_step, total_steps, start_time)
                section_short = section_title[:30] + "..." if len(section_title) > 30 else section_title
                progress_callback(f"{self.loc.t('processing_section')} '{section_short}'... ({self.loc.t('remaining_time')} ~{self._format_time(remaining_time)})", current_step, total_steps)
            
            section = Section(title=section_title)
            current_step += 1
            
            self._debug_log(f"{self.loc.t('debug_ai_request')} {self.loc.t('debug_slide_titles')}", f"{self.loc.t('debug_section')}: {section_title}, {self.loc.t('debug_count')}: {max_slides}")
            
            step_start = time.time()
            slide_titles = await self.ai_service.generate_slide_titles(
                section_title, title, max_slides, language
            )
            
            self._debug_log(f"{self.loc.t('debug_ai_response')} {self.loc.t('debug_slide_titles')}", str(slide_titles))
            
            step_duration = time.time() - step_start
            self._update_step_timing(step_duration)
            if not slide_titles or len(slide_titles) < max_slides:
                slide_titles = [f"{self.loc.t('slide_default')} {i+1}" for i in range(max_slides)]
            
            for slide_index, slide_title in enumerate(slide_titles):
                if progress_callback:
                    remaining_time = self._calculate_remaining_time(current_step, total_steps, start_time)
                    title_short = slide_title[:30] + "..." if len(slide_title) > 30 else slide_title
                    progress_callback(
                        f"{self.loc.t('generating_slide')} '{title_short}'... ({self.loc.t('remaining_time')} ~{self._format_time(remaining_time)})", 
                        current_step, 
                        total_steps
                    )
                
                web_content = None
                if enable_web_search and self.web_search_service.is_search_beneficial(slide_title):
                    self._debug_log(f"{self.loc.t('debug_web_search')} {slide_title}")
                    
                    if progress_callback:
                        remaining_time = self._calculate_remaining_time(current_step, total_steps, start_time)
                        title_short = slide_title[:30] + "..." if len(slide_title) > 30 else slide_title
                        progress_callback(
                            f"{self.loc.t('searching_web')} '{title_short}'... ({self.loc.t('remaining_time')} ~{self._format_time(remaining_time)})", 
                            current_step, 
                            total_steps
                        )
                    
                    step_start = time.time()
                    search_result = self.web_search_service.search_information(slide_title, language)
                    
                    if search_result and isinstance(search_result, dict) and 'content' in search_result:
                        web_content = search_result['content']
                        self._debug_log(f"{self.loc.t('debug_web_result')} {slide_title}", web_content[:200] + "..." if len(web_content) > 200 else web_content)
                    
                    step_duration = time.time() - step_start
                    self._update_step_timing(step_duration)
                
                current_step += 1
                
                step_start = time.time()
                self._debug_log(f"{self.loc.t('debug_ai_request')} {slide_title}", f"{self.loc.t('debug_section')}: {section_title}")
                
                if web_content:
                    slide_content = await self.ai_service.enhance_content_with_web_info(
                        "", web_content, slide_title, language
                    )
                    if not slide_content or len(slide_content.strip()) < 20:
                        slide_content = await self.ai_service.generate_slide_content(
                            slide_title, section_title, language
                        )
                else:
                    slide_content = await self.ai_service.generate_slide_content(
                        slide_title, section_title, language
                    )
                
                self._debug_log(f"{self.loc.t('debug_ai_response')} {slide_title}", slide_content)
                
                slide_content = self.ai_service.fix_line_breaks(slide_content, language)
                
                step_duration = time.time() - step_start
                self._update_step_timing(step_duration)
                
                if not slide_content or len(slide_content.strip()) < 20 or self._is_placeholder_content(slide_content):
                    slide_content = await self.ai_service.generate_slide_content(slide_title, section_title, language)
                    if not slide_content or len(slide_content.strip()) < 20 or self._is_placeholder_content(slide_content):
                        slide_content = f"{self.loc.t('slide_content_default')} '{slide_title}'"
                
                
                current_step += 1
                
                slide = Slide(title=slide_title, content=slide_content)
                section.add_slide(slide)
            
            presentation.add_section(section)
        
        
        presentation.generated = True
        
        if progress_callback:
            progress_callback(self.loc.t("presentation_ready"), current_step, total_steps)
        
        return presentation
    
    def save_presentation(self, presentation: Presentation, filename: Optional[str] = None) -> str:
        file_path = self.pptx_generator.generate_pptx(presentation, filename)
        self.db_manager.save_presentation(presentation)
        return file_path
    
    def get_presentation_stats(self, presentation: Presentation) -> dict:
        return {
            'title': presentation.title,
            'sections_count': len(presentation.sections),
            'total_slides': presentation.get_total_slides(),
            'language': presentation.language,
            'generated': presentation.generated,
            'created_at': presentation.created_at.strftime('%d.%m.%Y %H:%M:%S')
        }
    
    def list_saved_presentations(self) -> list:
        return self.pptx_generator.list_presentations()
    
    def delete_saved_presentation(self, filename: str) -> bool:
        return self.pptx_generator.delete_presentation(filename)
    
    def save_to_database(self, presentation: Presentation) -> int:
        return self.db_manager.save_presentation(presentation)
    
    def get_from_database(self, presentation_id: int) -> Optional[Presentation]:
        return self.db_manager.get_presentation(presentation_id)
    
    
    def get_database_presentations(self) -> list:
        return self.db_manager.list_presentations()
    
    def delete_database_presentation(self, presentation_id: int) -> bool:
        return self.db_manager.delete_presentation(presentation_id)
    
    def cleanup_database(self):
        self.db_manager.clear_all()
    
    def _update_step_timing(self, step_duration: float):
        self.step_times.append(step_duration)
        if len(self.step_times) > 10:
            self.step_times.pop(0)
        self.avg_step_time = sum(self.step_times) / len(self.step_times)
    
    def _format_time(self, seconds: float) -> str:
        if seconds < 60:
            return f"{int(seconds)} {self.loc.t('seconds')}"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            remaining_seconds = int(seconds % 60)
            if remaining_seconds == 0:
                return f"{minutes} {self.loc.t('minutes')}"
            else:
                return f"{minutes} {self.loc.t('minutes')} {remaining_seconds} {self.loc.t('seconds')}"
        else:
            hours = int(seconds // 3600)
            remaining_minutes = int((seconds % 3600) // 60)
            if remaining_minutes == 0:
                return f"{hours} {self.loc.t('hours')}"
            else:
                return f"{hours} {self.loc.t('hours')} {remaining_minutes} {self.loc.t('minutes')}"
    
    def _is_placeholder_content(self, content: str) -> bool:
        if not content or len(content.strip()) < 10:
            return True
        
        content_lower = content.lower()
        placeholder_indicators = [
            self.loc.t("content_for_slide"),
            "content for slide",
            self.loc.t("placeholder"),
            self.loc.t("placeholder"),
            self.loc.t("enter_text"),
            self.loc.t("add_content"),
            self.loc.t("text_will_be_here"),
            self.loc.t("text_for_slide")
        ]
        
        return any(indicator in content_lower for indicator in placeholder_indicators)
    
    def _is_table_content(self, content: str) -> bool:
        return content.strip().startswith("TABLE|")
    
    
    def _debug_log(self, message: str, data: str = ""):
        if self.developer_mode:
            print(f"\n[DEBUG] {message}")
            if data:
                print(f"[DEBUG] {data}")
            print("-" * 50)
    
    def _calculate_remaining_time(self, current_step: int, total_steps: int, start_time: float) -> int:
        if current_step == 0:
            return int(total_steps * self.avg_step_time)
        
        elapsed_time = time.time() - start_time
        remaining_steps = total_steps - current_step
        
        if remaining_steps <= 0:
            return 0
        
        if len(self.step_times) > 0:
            estimated_time = remaining_steps * self.avg_step_time
        else:
            avg_time_per_step = elapsed_time / current_step
            estimated_time = remaining_steps * avg_time_per_step
        
        return max(1, int(estimated_time))
