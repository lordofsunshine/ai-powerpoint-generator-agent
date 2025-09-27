import sys
import time
from typing import Callable, Optional
from pathlib import Path
from ..models.presentation import Presentation, Section, Slide
from ..services.ai_service import AIService
from ..services.correction_service import CorrectionService
from ..generators.pptx_generator import PPTXGenerator
from ..localization.manager import LocalizationManager

def get_resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        return Path(sys._MEIPASS) / relative_path
    else:
        return Path(__file__).parent.parent.parent / relative_path


class PresentationService:
    def __init__(self, ai_model: str = "gpt-4o-mini", output_dir: str = "output", interface_language: str = "русский"):
        self.ai_service = AIService(model=ai_model)
        self.pptx_generator = PPTXGenerator(output_dir=output_dir)
        self.correction_service = CorrectionService(ai_model=ai_model)
        self.loc = LocalizationManager()
        self.loc.set_language(interface_language)
        self.avg_step_time = 5.0
        self.step_times = []
    
    def generate_presentation(
        self, 
        title: str, 
        max_sections: int = 3, 
        max_slides: int = 4,
        language: str = "русский",
        progress_callback: Optional[Callable[[str, int, int], None]] = None
    ) -> Presentation:
        
        presentation = Presentation(
            title=title,
            language=language,
            max_sections=max_sections,
            max_slides=max_slides
        )
        
        total_steps = 1 + max_sections * (1 + max_slides)
        current_step = 0
        start_time = time.time()
        
        if progress_callback:
            progress_callback(self.loc.t("gen_summary"), current_step, total_steps)
        
        step_start = time.time()
        presentation.summary = self.ai_service.generate_presentation_summary(title, language)
        presentation.title_slide_header = self.ai_service.generate_title_slide_header(title, language)
        step_duration = time.time() - step_start
        self._update_step_timing(step_duration)
        current_step += 1
        
        if progress_callback:
            remaining_time = self._calculate_remaining_time(current_step, total_steps, start_time)
            progress_callback(f"{self.loc.t('gen_sections')} ({self.loc.t('remaining_time')} ~{self._format_time(remaining_time)})", current_step, total_steps)
        
        step_start = time.time()
        section_titles = self.ai_service.generate_section_titles(title, max_sections, language)
        step_duration = time.time() - step_start
        self._update_step_timing(step_duration)
        if not section_titles or len(section_titles) < max_sections:
            section_titles = [f"Секция {i+1}" for i in range(max_sections)]
        
        for section_index, section_title in enumerate(section_titles):
            if progress_callback:
                remaining_time = self._calculate_remaining_time(current_step, total_steps, start_time)
                progress_callback(f"{self.loc.t('processing_section')} '{section_title}'... ({self.loc.t('remaining_time')} ~{self._format_time(remaining_time)})", current_step, total_steps)
            
            section = Section(title=section_title)
            current_step += 1
            
            step_start = time.time()
            slide_titles = self.ai_service.generate_slide_titles(
                section_title, title, max_slides, language
            )
            step_duration = time.time() - step_start
            self._update_step_timing(step_duration)
            if not slide_titles or len(slide_titles) < max_slides:
                slide_titles = [f"Слайд {i+1}" for i in range(max_slides)]
            
            for slide_index, slide_title in enumerate(slide_titles):
                if progress_callback:
                    remaining_time = self._calculate_remaining_time(current_step, total_steps, start_time)
                    progress_callback(
                        f"{self.loc.t('generating_slide')} '{slide_title}'... ({self.loc.t('remaining_time')} ~{self._format_time(remaining_time)})", 
                        current_step, 
                        total_steps
                    )
                
                step_start = time.time()
                slide_content = self.ai_service.generate_slide_content(
                    slide_title, section_title, language
                )
                step_duration = time.time() - step_start
                self._update_step_timing(step_duration)
                if not slide_content or len(slide_content.strip()) < 20:
                    slide_content = f"Содержимое для слайда '{slide_title}'"
                
                slide = Slide(title=slide_title, content=slide_content)
                section.add_slide(slide)
                current_step += 1
            
            presentation.add_section(section)
        
        
        presentation.generated = True
        
        if progress_callback:
            progress_callback(self.loc.t("presentation_ready"), current_step, total_steps)
        
        return presentation
    
    def save_presentation(self, presentation: Presentation, filename: Optional[str] = None) -> str:
        return self.pptx_generator.generate_pptx(presentation, filename)
    
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
        return self.correction_service.save_presentation_to_db(presentation)
    
    def get_from_database(self, presentation_id: int) -> Optional[Presentation]:
        return self.correction_service.get_presentation_from_db(presentation_id)
    
    def apply_correction(self, presentation_id: int, correction_prompt: str, language: str = "русский", progress_callback: Optional[Callable[[str], None]] = None) -> Optional[Presentation]:
        return self.correction_service.apply_correction(presentation_id, correction_prompt, language, progress_callback)
    
    def get_database_presentations(self) -> list:
        return self.correction_service.get_db_presentations()
    
    def delete_database_presentation(self, presentation_id: int) -> bool:
        return self.correction_service.delete_db_presentation(presentation_id)
    
    def cleanup_database(self):
        self.correction_service.cleanup_db()
    
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
