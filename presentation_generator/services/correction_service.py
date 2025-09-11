import sys
import time
from pathlib import Path
from typing import Optional, Dict, Any, Callable
from ..models.presentation import Presentation, Section, Slide
from ..services.ai_service import AIService
from ..database.db_manager import DatabaseManager
from ..localization.manager import get_localization_manager

def get_resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        return Path(sys._MEIPASS) / relative_path
    else:
        return Path(__file__).parent.parent.parent / relative_path


class CorrectionService:
    def __init__(self, ai_model: str = "gpt-4o-mini"):
        self.ai_service = AIService(model=ai_model)
        self.db_manager = DatabaseManager()
        self.loc = get_localization_manager()
    
    def save_presentation_to_db(self, presentation: Presentation) -> int:
        return self.db_manager.save_presentation(presentation)
    
    def get_presentation_from_db(self, presentation_id: int) -> Optional[Presentation]:
        return self.db_manager.get_presentation(presentation_id)
    
    def apply_correction(
        self, 
        presentation_id: int, 
        correction_prompt: str, 
        language: str = "русский",
        progress_callback: Optional[Callable[[str], None]] = None
    ) -> Optional[Presentation]:
        presentation = self.get_presentation_from_db(presentation_id)
        if not presentation:
            return None
        
        if progress_callback:
            progress_callback(self.loc.t("analyzing_request"))
        
        correction_type = self._analyze_correction_type(correction_prompt)
        
        if progress_callback:
            progress_callback(f"{self.loc.t('applying_correction_type')} {correction_type}")
        
        time.sleep(0.5)
        
        if correction_type == "title":
            corrected_presentation = self._correct_title(presentation, correction_prompt, language, progress_callback)
        elif correction_type == "content":
            corrected_presentation = self._correct_content(presentation, correction_prompt, language, progress_callback)
        elif correction_type == "structure":
            corrected_presentation = self._correct_structure(presentation, correction_prompt, language, progress_callback)
        elif correction_type == "style":
            corrected_presentation = self._correct_style(presentation, correction_prompt, language, progress_callback)
        else:
            corrected_presentation = self._apply_general_correction(presentation, correction_prompt, language, progress_callback)
        
        if corrected_presentation and progress_callback:
            progress_callback(self.loc.t("saving_changes"))
            time.sleep(0.3)
            
        if corrected_presentation:
            self.db_manager.update_presentation(presentation_id, corrected_presentation)
        
        return corrected_presentation
    
    def _analyze_correction_type(self, prompt: str) -> str:
        prompt_lower = prompt.lower()
        
        title_keywords = ['заголовок', 'название', 'тему', 'переименуй', 'title']
        content_keywords = ['содержание', 'текст', 'информацию', 'добавь', 'убери', 'content', 'text']
        structure_keywords = ['структуру', 'слайды', 'секции', 'разделы', 'structure', 'slides']
        style_keywords = ['стиль', 'оформление', 'дизайн', 'формат', 'style', 'design']
        
        if any(keyword in prompt_lower for keyword in title_keywords):
            return "title"
        elif any(keyword in prompt_lower for keyword in content_keywords):
            return "content"
        elif any(keyword in prompt_lower for keyword in structure_keywords):
            return "structure"
        elif any(keyword in prompt_lower for keyword in style_keywords):
            return "style"
        else:
            return "general"
    
    def _correct_title(self, presentation: Presentation, prompt: str, language: str, progress_callback: Optional[Callable[[str], None]] = None) -> Presentation:
        if progress_callback:
            progress_callback(self.loc.t("changing_title"))
        
        new_title_prompt = self.loc.get_prompt(
            "correct_title",
            current_title=presentation.title,
            user_request=prompt
        )
        
        response = self.ai_service._make_request(new_title_prompt, temperature=0.7)
        if response:
            parsed = self.ai_service._parse_json_response(response)
            if parsed and 'title' in parsed:
                presentation.title = parsed['title']
        
        return presentation
    
    def _correct_content(self, presentation: Presentation, prompt: str, language: str, progress_callback: Optional[Callable[[str], None]] = None) -> Presentation:
        total_slides = sum(len(section.slides) for section in presentation.sections)
        current_slide = 0
        
        for section in presentation.sections:
            for slide in section.slides:
                current_slide += 1
                if progress_callback:
                    progress_callback(f"{self.loc.t('correcting_slide')} {current_slide}/{total_slides}: {slide.title}")
                
                correction_prompt = self.loc.get_prompt(
                    "correct_content",
                    slide_title=slide.title,
                    slide_content=slide.content,
                    user_request=prompt
                )
                
                response = self.ai_service._make_request(correction_prompt, temperature=0.8)
                if response:
                    parsed = self.ai_service._parse_json_response(response)
                    if parsed and 'content' in parsed:
                        slide.content = parsed['content']
                
                time.sleep(0.5)
        
        return presentation
    
    def _correct_structure(self, presentation: Presentation, prompt: str, language: str, progress_callback: Optional[Callable[[str], None]] = None) -> Presentation:
        structure_prompt = self.loc.get_prompt(
            "correct_structure",
            presentation_title=presentation.title,
            sections_list=[section.title for section in presentation.sections],
            user_request=prompt
        )
        
        response = self.ai_service._make_request(structure_prompt, temperature=0.8)
        if response:
            parsed = self.ai_service._parse_json_response(response)
            if parsed and 'sections' in parsed:
                new_section_titles = parsed['sections']
                
                for i, section in enumerate(presentation.sections):
                    if i < len(new_section_titles):
                        section.title = new_section_titles[i]
        
        return presentation
    
    def _correct_style(self, presentation: Presentation, prompt: str, language: str, progress_callback: Optional[Callable[[str], None]] = None) -> Presentation:
        for section in presentation.sections:
            for slide in section.slides:
                style_prompt = self.loc.get_prompt(
                    "correct_style",
                    slide_content=slide.content,
                    user_request=prompt
                )
                
                response = self.ai_service._make_request(style_prompt, temperature=0.7)
                if response:
                    parsed = self.ai_service._parse_json_response(response)
                    if parsed and 'content' in parsed:
                        slide.content = parsed['content']
        
        return presentation
    
    def _apply_general_correction(self, presentation: Presentation, prompt: str, language: str, progress_callback: Optional[Callable[[str], None]] = None) -> Presentation:
        general_prompt = self.loc.get_prompt(
            "correct_general",
            presentation_title=presentation.title,
            presentation_summary=presentation.summary or "",
            user_request=prompt
        )
        
        response = self.ai_service._make_request(general_prompt, temperature=0.8)
        if response:
            parsed = self.ai_service._parse_json_response(response)
            if parsed:
                if 'title' in parsed:
                    presentation.title = parsed['title']
                if 'summary' in parsed:
                    presentation.summary = parsed['summary']
        
        return presentation
    
    def get_db_presentations(self) -> list:
        return self.db_manager.list_presentations()
    
    def delete_db_presentation(self, presentation_id: int) -> bool:
        return self.db_manager.delete_presentation(presentation_id)
    
    def cleanup_db(self):
        self.db_manager.clear_all()
