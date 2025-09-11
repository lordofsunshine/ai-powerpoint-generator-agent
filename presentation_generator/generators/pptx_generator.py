import os
import sys
import re
from pathlib import Path
from typing import Optional, List
from pptx import Presentation as PPTXPresentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_VERTICAL_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.dml import MSO_THEME_COLOR
from ..models.presentation import Presentation
from .decorations import SlideDecorator

def get_resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        return Path(sys._MEIPASS) / relative_path
    else:
        return Path(__file__).parent.parent.parent / relative_path


class PPTXGenerator:
    def __init__(self, output_dir: str = "output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.decorator = SlideDecorator()
        
    def _create_title_slide(self, pptx: PPTXPresentation, presentation: Presentation, slide_index: int = 0, total_slides: int = 1) -> None:
        title_slide_layout = pptx.slide_layouts[0]
        slide = pptx.slides.add_slide(title_slide_layout)
        
        self.decorator.add_slide_background(slide, "title")
        
        title = slide.shapes.title
        subtitle = slide.placeholders[1]
        
        title.text = presentation.title
        if presentation.summary:
            subtitle.text = presentation.summary
        else:
            subtitle.text = "Создано с помощью AI генератора презентаций"
            
        self._apply_advanced_title_styling(title.text_frame, subtitle.text_frame)
        
        self.decorator.add_slide_decoration(slide, slide_index, total_slides, "title", presentation.title)
        self.decorator.apply_advanced_text_formatting(title.text_frame, "title")
    
    def _create_section_title_slide(self, pptx: PPTXPresentation, section_title: str, slide_index: int, total_slides: int, presentation_title: str = "") -> None:
        section_header_layout = pptx.slide_layouts[2]
        slide = pptx.slides.add_slide(section_header_layout)
        
        title = slide.shapes.title
        title.text = section_title
        
        self._apply_section_styling(title.text_frame)
        
        self.decorator.add_slide_decoration(slide, slide_index, total_slides, "section", presentation_title)
        self.decorator.apply_advanced_text_formatting(title.text_frame, "section")
    
    def _create_content_slide(self, pptx: PPTXPresentation, slide_title: str, slide_content: str, slide_index: int, total_slides: int, presentation_title: str = "") -> None:
        if not self._validate_slide_content(slide_content):
            slide_content = f"Содержимое для слайда '{slide_title}'"
        
        slide_type = self._determine_slide_type(slide_content)
        
        if slide_type == "list":
            self._create_enhanced_list_slide(pptx, slide_title, slide_content, slide_index, total_slides, presentation_title)
        elif slide_type == "comparison":
            self._create_comparison_slide(pptx, slide_title, slide_content, slide_index, total_slides, presentation_title)
        elif slide_type == "highlight":
            self._create_highlight_slide(pptx, slide_title, slide_content, slide_index, total_slides, presentation_title)
        elif slide_type == "process":
            self._create_process_slide(pptx, slide_title, slide_content, slide_index, total_slides, presentation_title)
        else:
            self._create_modern_content_slide(pptx, slide_title, slide_content, slide_index, total_slides, presentation_title)
    
    def _determine_slide_type(self, content: str) -> str:
        content_lower = content.lower()
        
        list_indicators = ['•', '-', '1.', '2.', '3.', 'этапы:', 'шаги:', 'принципы:', 'методы:']
        if any(indicator in content for indicator in list_indicators):
            return "list"
        
        comparison_indicators = ['преимущества', 'недостатки', 'плюсы', 'минусы', 'vs', 'против', 'сравнение']
        if any(indicator in content_lower for indicator in comparison_indicators):
            return "comparison"
        
        highlight_indicators = ['важно', 'ключевое', 'главное', 'внимание', 'запомните']
        if any(indicator in content_lower for indicator in highlight_indicators):
            return "highlight"
        
        process_indicators = ['процесс', 'алгоритм', 'последовательность', 'порядок', 'сначала', 'затем', 'далее']
        if any(indicator in content_lower for indicator in process_indicators):
            return "process"
        
        return "content"
    
    def _create_enhanced_list_slide(self, pptx: PPTXPresentation, slide_title: str, slide_content: str, slide_index: int, total_slides: int, presentation_title: str) -> None:
        blank_layout = pptx.slide_layouts[6]
        slide = pptx.slides.add_slide(blank_layout)
        
        self.decorator.add_slide_background(slide, "content")
        
        title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(9), Inches(1.2))
        title_frame = title_box.text_frame
        title_frame.text = slide_title
        self._apply_slide_title_styling(title_frame)
        
        truncated_content = self._truncate_content_for_slide(slide_content, "list")
        list_items = self._extract_enhanced_list_items(truncated_content)
        if not list_items:
            list_items = [truncated_content]
        
        content_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(8.4), Inches(5.2))
        content_frame = content_box.text_frame
        content_frame.word_wrap = True
        content_frame.auto_size = None
        content_frame.margin_left = Inches(0.1)
        content_frame.margin_right = Inches(0.1)
        content_frame.margin_top = Inches(0.1)
        content_frame.margin_bottom = Inches(0.1)
        
        for i, item in enumerate(list_items):
            if i == 0:
                p = content_frame.paragraphs[0]
            else:
                p = content_frame.add_paragraph()
            
            p.text = f"• {item.strip()}"
            p.level = 0
            p.space_after = Pt(16)
            self._apply_enhanced_list_styling(p, i)
        
        self.decorator.add_slide_decoration(slide, slide_index, total_slides, "list", presentation_title)
        self.decorator.apply_advanced_text_formatting(content_frame, "list", slide_content)
    
    def _create_comparison_slide(self, pptx: PPTXPresentation, slide_title: str, slide_content: str, slide_index: int, total_slides: int, presentation_title: str) -> None:
        blank_layout = pptx.slide_layouts[6]
        slide = pptx.slides.add_slide(blank_layout)
        
        self.decorator.add_slide_background(slide, "content")
        
        title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(9), Inches(1.2))
        title_frame = title_box.text_frame
        title_frame.text = slide_title
        self._apply_slide_title_styling(title_frame)
        
        truncated_content = self._truncate_content_for_slide(slide_content, "comparison")
        parts = self._split_comparison_content(truncated_content)
        
        left_box = slide.shapes.add_textbox(Inches(0.5), Inches(2), Inches(4.2), Inches(5))
        left_frame = left_box.text_frame
        left_frame.text = parts['left']
        left_frame.word_wrap = True
        left_frame.auto_size = None
        left_frame.margin_left = Inches(0.1)
        left_frame.margin_right = Inches(0.1)
        self._apply_comparison_styling(left_frame, "positive")
        
        right_box = slide.shapes.add_textbox(Inches(5.3), Inches(2), Inches(4.2), Inches(5))
        right_frame = right_box.text_frame
        right_frame.text = parts['right']
        right_frame.word_wrap = True
        right_frame.auto_size = None
        right_frame.margin_left = Inches(0.1)
        right_frame.margin_right = Inches(0.1)
        self._apply_comparison_styling(right_frame, "negative")
        
        separator = slide.shapes.add_connector(1, Inches(4.9), Inches(1.8), Inches(4.9), Inches(6.8))
        separator.line.color.rgb = self.decorator.current_scheme['secondary']
        separator.line.width = Pt(3)
        
        self.decorator.add_slide_decoration(slide, slide_index, total_slides, "content", presentation_title)
    
    def _create_highlight_slide(self, pptx: PPTXPresentation, slide_title: str, slide_content: str, slide_index: int, total_slides: int, presentation_title: str) -> None:
        blank_layout = pptx.slide_layouts[6]
        slide = pptx.slides.add_slide(blank_layout)
        
        title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(9), Inches(1.2))
        title_frame = title_box.text_frame
        title_frame.text = slide_title
        self._apply_slide_title_styling(title_frame)
        
        highlight_box = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(1), Inches(2.5),
            Inches(8), Inches(3)
        )
        
        fill = highlight_box.fill
        fill.solid()
        fill.fore_color.rgb = self.decorator.current_scheme['accent']
        
        highlight_box.line.fill.background()
        
        highlight_frame = highlight_box.text_frame
        highlight_frame.margin_left = Inches(0.5)
        highlight_frame.margin_right = Inches(0.5)
        highlight_frame.margin_top = Inches(0.3)
        highlight_frame.margin_bottom = Inches(0.3)
        highlight_frame.vertical_anchor = MSO_VERTICAL_ANCHOR.MIDDLE
        highlight_frame.word_wrap = True
        truncated_content = self._truncate_content_for_slide(slide_content, "highlight")
        highlight_frame.text = truncated_content
        
        self._apply_highlight_styling(highlight_frame)
        
        self.decorator.add_slide_decoration(slide, slide_index, total_slides, "content", presentation_title)
    
    def _create_process_slide(self, pptx: PPTXPresentation, slide_title: str, slide_content: str, slide_index: int, total_slides: int, presentation_title: str) -> None:
        blank_layout = pptx.slide_layouts[6]
        slide = pptx.slides.add_slide(blank_layout)
        
        self.decorator.add_slide_background(slide, "content")
        
        title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(9), Inches(1.2))
        title_frame = title_box.text_frame
        title_frame.text = slide_title
        self._apply_slide_title_styling(title_frame)
        
        truncated_content = self._truncate_content_for_slide(slide_content, "process")
        process_steps = self._extract_process_steps(truncated_content)
        if not process_steps:
            process_steps = [truncated_content[:100] + "..." if len(truncated_content) > 100 else truncated_content]
        
        step_width = 8 / len(process_steps)
        for i, step in enumerate(process_steps):
            x_pos = 1 + (i * step_width)
            
            step_shape = slide.shapes.add_shape(
                MSO_SHAPE.ROUNDED_RECTANGLE,
                Inches(x_pos), Inches(3),
                Inches(step_width - 0.2), Inches(2)
            )
            
            fill = step_shape.fill
            fill.solid()
            if i % 2 == 0:
                fill.fore_color.rgb = self.decorator.current_scheme['primary']
            else:
                fill.fore_color.rgb = self.decorator.current_scheme['secondary']
            
            step_shape.line.fill.background()
            
            step_frame = step_shape.text_frame
            step_frame.margin_left = Inches(0.1)
            step_frame.margin_right = Inches(0.1)
            step_frame.margin_top = Inches(0.1)
            step_frame.margin_bottom = Inches(0.1)
            step_frame.vertical_anchor = MSO_VERTICAL_ANCHOR.MIDDLE
            step_frame.word_wrap = True
            step_frame.text = f"{i+1}. {step}"
            
            self._apply_process_step_styling(step_frame, i % 2 == 0)
            
            if i < len(process_steps) - 1:
                arrow = slide.shapes.add_connector(
                    1,
                    Inches(x_pos + step_width - 0.2), Inches(4),
                    Inches(x_pos + step_width), Inches(4)
                )
                arrow.line.color.rgb = self.decorator.current_scheme['accent']
                arrow.line.width = Pt(4)
        
        self.decorator.add_slide_decoration(slide, slide_index, total_slides, "content", presentation_title)
    
    def _create_modern_content_slide(self, pptx: PPTXPresentation, slide_title: str, slide_content: str, slide_index: int, total_slides: int, presentation_title: str) -> None:
        blank_layout = pptx.slide_layouts[6]
        slide = pptx.slides.add_slide(blank_layout)
        
        self.decorator.add_slide_background(slide, "content")
        
        title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(9), Inches(1.2))
        title_frame = title_box.text_frame
        title_frame.text = slide_title
        self._apply_slide_title_styling(title_frame)
        
        content_shape = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(0.5), Inches(1.8),
            Inches(9), Inches(5.2)
        )
        
        fill = content_shape.fill
        fill.solid()
        bg_color = self.decorator.current_scheme['background']
        fill.fore_color.rgb = RGBColor(248, 250, 252)
        
        line = content_shape.line
        line.color.rgb = self.decorator.current_scheme['secondary']
        line.width = Pt(2)
        
        content_frame = content_shape.text_frame
        content_frame.margin_left = Inches(0.4)
        content_frame.margin_right = Inches(0.4)
        content_frame.margin_top = Inches(0.4)
        content_frame.margin_bottom = Inches(0.4)
        content_frame.vertical_anchor = MSO_VERTICAL_ANCHOR.TOP
        content_frame.word_wrap = True
        
        truncated_content = self._truncate_content_for_slide(slide_content, "content")
        content_frame.text = truncated_content
        
        self._apply_modern_content_styling(content_frame)
        
        self.decorator.add_slide_decoration(slide, slide_index, total_slides, "content", presentation_title)
        self.decorator.apply_advanced_text_formatting(content_frame, "content", truncated_content)
    
    def _extract_enhanced_list_items(self, content: str) -> List[str]:
        lines = content.split('\n')
        items = []
        current_item = ""
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if line.startswith(('•', '-', '1.', '2.', '3.', '4.', '5.')):
                if current_item:
                    items.append(current_item)
                current_item = re.sub(r'^[•\-\d\.]\s*', '', line)
            else:
                if current_item:
                    current_item += f" {line}"
                else:
                    current_item = line
        
        if current_item:
            items.append(current_item)
        
        if not items:
            sentences = content.split('.')
            items = [s.strip() for s in sentences if s.strip()][:6]
        
        return items[:6]
    
    def _split_comparison_content(self, content: str) -> dict:
        content_lower = content.lower()
        
        if 'преимущества' in content_lower and 'недостатки' in content_lower:
            parts = content.split('недостатки', 1)
            left = parts[0].replace('преимущества', '').strip()
            right = parts[1].strip() if len(parts) > 1 else ""
        elif 'плюсы' in content_lower and 'минусы' in content_lower:
            parts = content.split('минусы', 1)
            left = parts[0].replace('плюсы', '').strip()
            right = parts[1].strip() if len(parts) > 1 else ""
        else:
            mid_point = len(content) // 2
            left = content[:mid_point].strip()
            right = content[mid_point:].strip()
        
        return {'left': left, 'right': right}
    
    def _extract_process_steps(self, content: str) -> List[str]:
        steps = []
        sentences = content.split('.')
        
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence and len(sentence) > 10:
                steps.append(sentence)
        
        return steps[:5]
    
    def _apply_advanced_title_styling(self, title_frame, subtitle_frame) -> None:
        title_frame.word_wrap = True
        title_frame.auto_size = None
        p = title_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        run = p.runs[0] if p.runs else p.add_run()
        font = run.font
        font.name = 'Montserrat'
        font.size = Pt(52)
        font.bold = True
        font.color.rgb = self.decorator.current_scheme['primary']
        
        subtitle_p = subtitle_frame.paragraphs[0]
        subtitle_p.alignment = PP_ALIGN.CENTER
        subtitle_run = subtitle_p.runs[0] if subtitle_p.runs else subtitle_p.add_run()
        subtitle_font = subtitle_run.font
        subtitle_font.name = 'Open Sans'
        subtitle_font.size = Pt(22)
        subtitle_font.color.rgb = self.decorator.current_scheme['text']
    
    def _apply_section_styling(self, text_frame) -> None:
        text_frame.word_wrap = True
        text_frame.auto_size = None
        p = text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        run = p.runs[0] if p.runs else p.add_run()
        font = run.font
        font.name = 'Montserrat'
        font.size = Pt(40)
        font.bold = True
        font.color.rgb = self.decorator.current_scheme['primary']
    
    def _apply_slide_title_styling(self, text_frame) -> None:
        text_frame.word_wrap = True
        text_frame.auto_size = None
        p = text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.LEFT
        run = p.runs[0] if p.runs else p.add_run()
        font = run.font
        font.name = 'Montserrat'
        font.size = Pt(36)
        font.bold = True
        font.color.rgb = self.decorator.current_scheme['primary']
    
    def _apply_enhanced_list_styling(self, paragraph, index: int) -> None:
        paragraph.alignment = PP_ALIGN.LEFT
        paragraph.space_after = Pt(12)
        paragraph.line_spacing = 1.2
        
        for run in paragraph.runs:
            font = run.font
            font.name = 'Open Sans'
            font.size = Pt(18)
            font.color.rgb = self.decorator.current_scheme['text']
            
            if run.text.startswith('•'):
                font.color.rgb = self.decorator.current_scheme['accent']
                font.size = Pt(22)
                font.bold = True
    
    def _apply_comparison_styling(self, text_frame, side: str) -> None:
        for paragraph in text_frame.paragraphs:
            paragraph.alignment = PP_ALIGN.LEFT
            paragraph.space_after = Pt(12)
            paragraph.line_spacing = 1.3
            for run in paragraph.runs:
                font = run.font
                font.name = 'Open Sans'
                font.size = Pt(16)
                if side == "positive":
                    font.color.rgb = self.decorator.current_scheme['primary']
                else:
                    font.color.rgb = self.decorator.current_scheme['text']
    
    def _apply_highlight_styling(self, text_frame) -> None:
        for paragraph in text_frame.paragraphs:
            paragraph.alignment = PP_ALIGN.CENTER
            for run in paragraph.runs:
                font = run.font
                font.name = 'Montserrat'
                font.size = Pt(20)
                font.bold = True
                font.color.rgb = RGBColor(255, 255, 255)
    
    def _apply_process_step_styling(self, text_frame, is_primary: bool) -> None:
        for paragraph in text_frame.paragraphs:
            paragraph.alignment = PP_ALIGN.CENTER
            for run in paragraph.runs:
                font = run.font
                font.name = 'Open Sans'
                font.size = Pt(14)
                font.bold = True
                if is_primary:
                    font.color.rgb = RGBColor(255, 255, 255)
                else:
                    font.color.rgb = self.decorator.current_scheme['text']
    
    def _apply_modern_content_styling(self, text_frame) -> None:
        text_frame.word_wrap = True
        for paragraph in text_frame.paragraphs:
            paragraph.alignment = PP_ALIGN.LEFT
            paragraph.space_after = Pt(12)
            paragraph.line_spacing = 1.4
            for run in paragraph.runs:
                font = run.font
                font.name = 'Open Sans'
                font.size = Pt(16)
                font.color.rgb = self.decorator.current_scheme['text']
    
    def _validate_slide_content(self, content: str) -> bool:
        if not content or len(content.strip()) < 10:
            return False
        
        content_lower = content.lower()
        invalid_indicators = [
            "содержимое для слайда",
            "content for slide",
            "placeholder",
            "заглушка",
            "введите текст",
            "добавьте контент",
            "здесь будет текст",
            "текст для слайда"
        ]
        
        if any(indicator in content_lower for indicator in invalid_indicators):
            return False
        
        return True
    
    def _truncate_content_for_slide(self, content: str, slide_type: str) -> str:
        max_chars = {
            "content": 800,
            "list": 600,
            "comparison": 400,
            "highlight": 300,
            "process": 500
        }
        
        max_length = max_chars.get(slide_type, 600)
        
        if len(content) <= max_length:
            return content
        
        truncated = content[:max_length]
        last_period = truncated.rfind('.')
        last_exclamation = truncated.rfind('!')
        last_question = truncated.rfind('?')
        
        last_sentence_end = max(last_period, last_exclamation, last_question)
        
        if last_sentence_end > max_length * 0.7:
            return truncated[:last_sentence_end + 1]
        
        return truncated + "..."
    
    def _sanitize_filename(self, filename: str) -> str:
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        return filename
    
    def generate_pptx(self, presentation: Presentation, filename: Optional[str] = None) -> str:
        if not filename:
            safe_title = self._sanitize_filename(presentation.title)
            filename = f"{safe_title}.pptx"
        
        if not filename.endswith('.pptx'):
            filename += '.pptx'
            
        output_path = self.output_dir / filename
        
        pptx = PPTXPresentation()
        
        total_slides = 1
        if presentation.sections:
            total_slides += len(presentation.sections)
            for section in presentation.sections:
                if section.slides:
                    total_slides += len(section.slides)
        
        slide_index = 0
        
        self._create_title_slide(pptx, presentation, slide_index, total_slides)
        slide_index += 1
        
        if presentation.sections:
            for section in presentation.sections:
                if section.slides and len(section.slides) > 0:
                    self._create_section_title_slide(pptx, section.title, slide_index, total_slides, presentation.title)
                    slide_index += 1
                    
                    for slide in section.slides:
                        self._create_content_slide(pptx, slide.title, slide.content, slide_index, total_slides, presentation.title)
                        slide_index += 1
        
        pptx.save(str(output_path))
        return str(output_path.absolute())
    
    def list_presentations(self) -> list:
        return [f.name for f in self.output_dir.glob("*.pptx")]
    
    def delete_presentation(self, filename: str) -> bool:
        try:
            file_path = self.output_dir / filename
            if file_path.exists() and file_path.suffix == '.pptx':
                file_path.unlink()
                return True
        except Exception:
            pass
        return False
