import sys
from typing import Callable, Optional
from pathlib import Path
from ..models.presentation import Presentation, Section, Slide
from ..services.ai_service import AIService
from ..services.correction_service import CorrectionService
from ..generators.pptx_generator import PPTXGenerator

def get_resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        return Path(sys._MEIPASS) / relative_path
    else:
        return Path(__file__).parent.parent.parent / relative_path


class PresentationService:
    def __init__(self, ai_model: str = "gpt-4o-mini", output_dir: str = "output"):
        self.ai_service = AIService(model=ai_model)
        self.pptx_generator = PPTXGenerator(output_dir=output_dir)
        self.correction_service = CorrectionService(ai_model=ai_model)
    
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
        
        if progress_callback:
            progress_callback("Генерация описания презентации...", current_step, total_steps)
        
        presentation.summary = self.ai_service.generate_presentation_summary(title, language)
        current_step += 1
        
        if progress_callback:
            progress_callback("Генерация заголовков секций...", current_step, total_steps)
        
        section_titles = self.ai_service.generate_section_titles(title, max_sections, language)
        if not section_titles or len(section_titles) < max_sections:
            section_titles = [f"Секция {i+1}" for i in range(max_sections)]
        
        for section_index, section_title in enumerate(section_titles):
            if progress_callback:
                progress_callback(f"Обработка секции '{section_title}'...", current_step, total_steps)
            
            section = Section(title=section_title)
            current_step += 1
            
            slide_titles = self.ai_service.generate_slide_titles(
                section_title, title, max_slides, language
            )
            if not slide_titles or len(slide_titles) < max_slides:
                slide_titles = [f"Слайд {i+1}" for i in range(max_slides)]
            
            for slide_index, slide_title in enumerate(slide_titles):
                if progress_callback:
                    progress_callback(
                        f"Генерация слайда '{slide_title}'...", 
                        current_step, 
                        total_steps
                    )
                
                slide_content = self.ai_service.generate_slide_content(
                    slide_title, section_title, language
                )
                if not slide_content or len(slide_content.strip()) < 20:
                    slide_content = f"Содержимое для слайда '{slide_title}'"
                
                slide = Slide(title=slide_title, content=slide_content)
                section.add_slide(slide)
                current_step += 1
            
            presentation.add_section(section)
        
        presentation.generated = True
        
        if progress_callback:
            progress_callback("Презентация готова!", current_step, total_steps)
        
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
