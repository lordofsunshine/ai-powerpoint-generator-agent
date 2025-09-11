import random
import sys
from pathlib import Path
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_THEME_COLOR, MSO_FILL
from pptx.enum.text import PP_ALIGN, MSO_VERTICAL_ANCHOR
import math

def get_resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        return Path(sys._MEIPASS) / relative_path
    else:
        return Path(__file__).parent.parent.parent / relative_path


class SlideDecorator:
    def __init__(self):
        self.color_schemes = {
            'modern_blue': {
                'primary': RGBColor(41, 98, 255),
                'secondary': RGBColor(116, 185, 255),
                'accent': RGBColor(255, 107, 107),
                'background': RGBColor(248, 250, 252),
                'text': RGBColor(30, 41, 59)
            },
            'elegant_purple': {
                'primary': RGBColor(139, 69, 255),
                'secondary': RGBColor(196, 181, 253),
                'accent': RGBColor(255, 154, 0),
                'background': RGBColor(250, 249, 255),
                'text': RGBColor(55, 48, 163)
            },
            'warm_orange': {
                'primary': RGBColor(255, 107, 0),
                'secondary': RGBColor(255, 183, 77),
                'accent': RGBColor(34, 197, 94),
                'background': RGBColor(255, 251, 235),
                'text': RGBColor(124, 45, 18)
            },
            'forest_green': {
                'primary': RGBColor(34, 197, 94),
                'secondary': RGBColor(134, 239, 172),
                'accent': RGBColor(239, 68, 68),
                'background': RGBColor(240, 253, 244),
                'text': RGBColor(20, 83, 45)
            },
            'ocean_teal': {
                'primary': RGBColor(20, 184, 166),
                'secondary': RGBColor(153, 246, 228),
                'accent': RGBColor(251, 146, 60),
                'background': RGBColor(240, 253, 250),
                'text': RGBColor(19, 78, 74)
            },
            'sunset_pink': {
                'primary': RGBColor(236, 72, 153),
                'secondary': RGBColor(251, 207, 232),
                'accent': RGBColor(59, 130, 246),
                'background': RGBColor(253, 242, 248),
                'text': RGBColor(131, 24, 67)
            },
            'corporate_navy': {
                'primary': RGBColor(30, 58, 138),
                'secondary': RGBColor(147, 197, 253),
                'accent': RGBColor(245, 158, 11),
                'background': RGBColor(248, 250, 252),
                'text': RGBColor(30, 41, 59)
            },
            'creative_magenta': {
                'primary': RGBColor(192, 38, 211),
                'secondary': RGBColor(233, 213, 255),
                'accent': RGBColor(16, 185, 129),
                'background': RGBColor(253, 244, 255),
                'text': RGBColor(112, 26, 117)
            }
        }
        
        self.decoration_styles = [
            'geometric_modern', 'organic_flow', 'minimal_lines', 'dynamic_shapes',
            'gradient_waves', 'abstract_art', 'tech_grid', 'nature_inspired'
        ]
        
        self.current_scheme = None
        self.slide_counter = 0
    
    def _get_safe_position(self, slide, min_width, max_width, min_height, max_height):
        text_areas = self._get_text_areas(slide)
        max_attempts = 50
        
        for _ in range(max_attempts):
            width = Inches(random.uniform(min_width, max_width))
            height = Inches(random.uniform(min_height, max_height))
            
            x = Inches(random.uniform(7.5, 9.5 - width.inches))
            y = Inches(random.uniform(0.5, 6.5 - height.inches))
            
            if not self._overlaps_with_text(x, y, width, height, text_areas):
                return x, y, width, height
        
        return Inches(8.5), Inches(5.5), width, height
    
    def _get_text_areas(self, slide):
        text_areas = []
        for shape in slide.shapes:
            if hasattr(shape, 'text_frame') and shape.text_frame.text.strip():
                text_areas.append({
                    'left': shape.left,
                    'top': shape.top,
                    'right': shape.left + shape.width,
                    'bottom': shape.top + shape.height
                })
        return text_areas
    
    def _overlaps_with_text(self, x, y, width, height, text_areas):
        buffer = Inches(0.3)
        decoration_left = x - buffer
        decoration_right = x + width + buffer
        decoration_top = y - buffer
        decoration_bottom = y + height + buffer
        
        for area in text_areas:
            if not (decoration_right < area['left'] or 
                   decoration_left > area['right'] or 
                   decoration_bottom < area['top'] or 
                   decoration_top > area['bottom']):
                return True
        return False
    
    def choose_color_scheme(self, presentation_title: str) -> dict:
        title_lower = presentation_title.lower()
        
        if any(word in title_lower for word in ['бизнес', 'корпорат', 'финанс', 'business', 'corporate']):
            return self.color_schemes['corporate_navy']
        elif any(word in title_lower for word in ['креатив', 'дизайн', 'искусство', 'creative', 'design', 'art']):
            return self.color_schemes['creative_magenta']
        elif any(word in title_lower for word in ['природа', 'эко', 'зелен', 'nature', 'eco', 'green']):
            return self.color_schemes['forest_green']
        elif any(word in title_lower for word in ['технолог', 'IT', 'цифров', 'tech', 'digital']):
            return self.color_schemes['modern_blue']
        else:
            return random.choice(list(self.color_schemes.values()))
    
    def add_slide_decoration(self, slide, slide_index: int, total_slides: int, slide_type: str = "content", presentation_title: str = ""):
        if self.current_scheme is None:
            self.current_scheme = self.choose_color_scheme(presentation_title)
        
        self.slide_counter += 1
        decoration_style = self._choose_decoration_style(slide_index, total_slides, slide_type)
        
        if decoration_style == "geometric_modern":
            self._add_geometric_modern(slide)
        elif decoration_style == "organic_flow":
            self._add_organic_flow(slide)
        elif decoration_style == "minimal_lines":
            self._add_minimal_lines(slide)
        elif decoration_style == "dynamic_shapes":
            self._add_dynamic_shapes(slide)
        elif decoration_style == "gradient_waves":
            self._add_gradient_waves(slide)
        elif decoration_style == "abstract_art":
            self._add_abstract_art(slide)
        elif decoration_style == "tech_grid":
            self._add_tech_grid(slide)
        elif decoration_style == "nature_inspired":
            self._add_nature_inspired(slide)
    
    def _choose_decoration_style(self, slide_index: int, total_slides: int, slide_type: str) -> str:
        if slide_index == 0:
            return random.choice(['geometric_modern', 'gradient_waves', 'abstract_art'])
        elif slide_type == "section":
            return random.choice(['minimal_lines', 'dynamic_shapes', 'organic_flow'])
        else:
            return random.choice(self.decoration_styles)
    
    def _add_geometric_modern(self, slide):
        shapes_count = random.randint(3, 6)
        for i in range(shapes_count):
            shape_type = random.choice([MSO_SHAPE.RECTANGLE, MSO_SHAPE.ROUNDED_RECTANGLE, MSO_SHAPE.HEXAGON])
            
            x, y, width, height = self._get_safe_position(slide, 0.8, 2, 0.8, 2)
            
            shape = slide.shapes.add_shape(shape_type, x, y, width, height)
            
            if i % 2 == 0:
                fill = shape.fill
                fill.solid()
                fill.fore_color.rgb = self.current_scheme['primary']
                shape.line.fill.background()
            else:
                shape.fill.background()
                line = shape.line
                line.color.rgb = self.current_scheme['secondary']
                line.width = Pt(3)
            
            shape.rotation = random.randint(-30, 30)
    
    def _add_organic_flow(self, slide):
        for i in range(random.randint(2, 4)):
            x, y, width, height = self._get_safe_position(slide, 1, 3, 0.5, 2)
            
            shape = slide.shapes.add_shape(MSO_SHAPE.OVAL, x, y, width, height)
            
            fill = shape.fill
            fill.solid()
            color = self.current_scheme['secondary']
            fill.fore_color.rgb = RGBColor(
                random.randint(100, 200),
                random.randint(150, 255),
                random.randint(150, 255)
            )
            
            shape.line.fill.background()
            shape.rotation = random.randint(-45, 45)
    
    def _add_minimal_lines(self, slide):
        line_count = random.randint(2, 5)
        for i in range(line_count):
            if random.choice([True, False]):
                line = slide.shapes.add_connector(
                    1,
                    Inches(random.uniform(0.5, 9)),
                    Inches(random.uniform(1, 2)),
                    Inches(random.uniform(0.5, 9)),
                    Inches(random.uniform(1, 2))
                )
            else:
                line = slide.shapes.add_connector(
                    1,
                    Inches(random.uniform(0.5, 1.5)),
                    Inches(random.uniform(1, 6)),
                    Inches(random.uniform(0.5, 1.5)),
                    Inches(random.uniform(1, 6))
                )
            
            line.line.color.rgb = self.current_scheme['primary']
            line.line.width = Pt(random.randint(2, 6))
    
    def _add_dynamic_shapes(self, slide):
        shapes = [MSO_SHAPE.DIAMOND, MSO_SHAPE.PENTAGON, MSO_SHAPE.HEXAGON, MSO_SHAPE.ROUNDED_RECTANGLE]
        
        for i in range(random.randint(3, 5)):
            x, y, width, height = self._get_safe_position(slide, 0.6, 1.5, 0.6, 1.5)
            
            shape = slide.shapes.add_shape(random.choice(shapes), x, y, width, height)
            
            if i % 3 == 0:
                fill = shape.fill
                fill.solid()
                fill.fore_color.rgb = self.current_scheme['accent']
                shape.line.fill.background()
            else:
                shape.fill.background()
                line = shape.line
                line.color.rgb = self.current_scheme['primary']
                line.width = Pt(2)
            
            shape.rotation = random.randint(0, 360)
    
    def _add_gradient_waves(self, slide):
        wave_shape = slide.shapes.add_shape(
            MSO_SHAPE.WAVE,
            Inches(0), Inches(6),
            Inches(10), Inches(1.5)
        )
        
        fill = wave_shape.fill
        fill.solid()
        fill.fore_color.rgb = self.current_scheme['background']
        
        line = wave_shape.line
        line.color.rgb = self.current_scheme['secondary']
        line.width = Pt(2)
    
    def _add_abstract_art(self, slide):
        for i in range(random.randint(4, 7)):
            shape_type = random.choice([MSO_SHAPE.OVAL, MSO_SHAPE.ROUNDED_RECTANGLE, MSO_SHAPE.DIAMOND])
            
            x, y, width, height = self._get_safe_position(slide, 0.3, 1.2, 0.3, 1.2)
            
            shape = slide.shapes.add_shape(shape_type, x, y, width, height)
            
            colors = [self.current_scheme['primary'], self.current_scheme['secondary'], self.current_scheme['accent']]
            
            fill = shape.fill
            fill.solid()
            fill.fore_color.rgb = random.choice(colors)
            
            shape.line.fill.background()
            shape.rotation = random.randint(0, 360)
    
    def _add_tech_grid(self, slide):
        grid_size = 0.3
        for x in range(int(10 / grid_size)):
            for y in range(int(7.5 / grid_size)):
                if random.random() < 0.1:
                    dot = slide.shapes.add_shape(
                        MSO_SHAPE.OVAL,
                        Inches(x * grid_size),
                        Inches(y * grid_size),
                        Inches(0.05),
                        Inches(0.05)
                    )
                    
                    fill = dot.fill
                    fill.solid()
                    fill.fore_color.rgb = self.current_scheme['secondary']
                    dot.line.fill.background()
    
    def _add_nature_inspired(self, slide):
        leaf_shapes = [MSO_SHAPE.OVAL, MSO_SHAPE.ROUNDED_RECTANGLE, MSO_SHAPE.TEAR]
        
        for i in range(random.randint(3, 6)):
            x, y, width, height = self._get_safe_position(slide, 0.4, 1, 0.8, 2)
            
            shape = slide.shapes.add_shape(random.choice(leaf_shapes), x, y, width, height)
            
            green_variations = [
                RGBColor(34, 197, 94),
                RGBColor(22, 163, 74),
                RGBColor(21, 128, 61),
                RGBColor(134, 239, 172)
            ]
            
            fill = shape.fill
            fill.solid()
            fill.fore_color.rgb = random.choice(green_variations)
            
            shape.line.fill.background()
            shape.rotation = random.randint(-30, 30)
    
    def apply_advanced_text_formatting(self, text_frame, slide_type: str = "content", content: str = ""):
        if self.current_scheme is None:
            self.current_scheme = self.choose_color_scheme("")
            
        if slide_type == "title":
            self._format_title_advanced(text_frame)
        elif slide_type == "section":
            self._format_section_advanced(text_frame)
        elif slide_type == "content":
            self._format_content_advanced(text_frame, content)
        elif slide_type == "list":
            self._format_list_advanced(text_frame, content)
    
    def _format_title_advanced(self, text_frame):
        for paragraph in text_frame.paragraphs:
            paragraph.alignment = PP_ALIGN.CENTER
            for run in paragraph.runs:
                font = run.font
                font.name = 'Montserrat'
                font.size = Pt(48)
                font.bold = True
                font.color.rgb = self.current_scheme['primary']
                
                if any(word in run.text.lower() for word in ['важн', 'ключев', 'главн', 'important', 'key', 'main']):
                    font.color.rgb = self.current_scheme['accent']
    
    def _format_section_advanced(self, text_frame):
        for paragraph in text_frame.paragraphs:
            paragraph.alignment = PP_ALIGN.CENTER
            for run in paragraph.runs:
                font = run.font
                font.name = 'Montserrat'
                font.size = Pt(36)
                font.bold = True
                font.color.rgb = self.current_scheme['primary']
    
    def _format_content_advanced(self, text_frame, content: str):
        sentences = content.split('.')
        
        for paragraph in text_frame.paragraphs:
            paragraph.alignment = PP_ALIGN.LEFT
            paragraph.space_after = Pt(12)
            
            if ':' in paragraph.text:
                parts = paragraph.text.split(':', 1)
                if len(parts) >= 2:
                    paragraph.clear()
                    
                    title_run = paragraph.add_run()
                    title_run.text = parts[0] + ':'
                    title_run.font.name = 'Montserrat'
                    title_run.font.size = Pt(18)
                    title_run.font.bold = True
                    title_run.font.color.rgb = self.current_scheme['primary']
                    
                    content_run = paragraph.add_run()
                    content_run.text = parts[1]
                    content_run.font.name = 'Open Sans'
                    content_run.font.size = Pt(16)
                    content_run.font.color.rgb = self.current_scheme['text']
            else:
                for run in paragraph.runs:
                    font = run.font
                    font.name = 'Open Sans'
                    font.size = Pt(16)
                    font.color.rgb = self.current_scheme['text']
                    
                    if any(word in run.text.lower() for word in ['важн', 'ключев', 'главн', 'important', 'key', 'main']):
                        font.bold = True
                        font.color.rgb = self.current_scheme['accent']
    
    def _format_list_advanced(self, text_frame, content: str):
        for paragraph in text_frame.paragraphs:
            paragraph.space_after = Pt(8)
            
            if paragraph.text.strip().startswith(('•', '-', '1.', '2.', '3.')):
                for run in paragraph.runs:
                    if run.text.strip().startswith(('•', '-')):
                        run.font.color.rgb = self.current_scheme['accent']
                        run.font.size = Pt(20)
                        run.font.bold = True
                    else:
                        run.font.name = 'Open Sans'
                        run.font.size = Pt(16)
                        run.font.color.rgb = self.current_scheme['text']
    
    def add_slide_background(self, slide, slide_type: str = "content"):
        if self.current_scheme is None:
            self.current_scheme = self.choose_color_scheme("")
            
        if slide_type == "title":
            self._add_title_background(slide)
        elif random.random() < 0.3:
            self._add_subtle_background(slide)
    
    def _add_title_background(self, slide):
        bg_shape = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(0), Inches(0),
            Inches(10), Inches(7.5)
        )
        
        fill = bg_shape.fill
        fill.solid()
        fill.fore_color.rgb = self.current_scheme['background']
        
        bg_shape.line.fill.background()
        
        bg_shape.element.getparent().remove(bg_shape.element)
        slide.shapes._spTree.insert(2, bg_shape.element)
    
    def _add_subtle_background(self, slide):
        bg_shape = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(0.3), Inches(1.5),
            Inches(9.4), Inches(5.5)
        )
        
        fill = bg_shape.fill
        fill.solid()
        bg_color = self.current_scheme['background']
        fill.fore_color.rgb = RGBColor(250, 250, 252)
        
        line = bg_shape.line
        line.color.rgb = self.current_scheme['secondary']
        line.width = Pt(1)
        
        bg_shape.element.getparent().remove(bg_shape.element)
        slide.shapes._spTree.insert(2, bg_shape.element)
