import json
import sys
import time
from pathlib import Path
from typing import List, Optional
from g4f.client import Client
from ..models.presentation import Presentation, Section, Slide
from ..localization.manager import get_localization_manager

def get_resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        return Path(sys._MEIPASS) / relative_path
    else:
        return Path(__file__).parent.parent.parent / relative_path


class AIService:
    def __init__(self, model: str = "gpt-4o-mini"):
        self.client = Client()
        self.model = model
        self.max_attempts = 3
        self.retry_delay = 1.0
        self.loc = get_localization_manager()
        
    def _make_request(self, prompt: str, temperature: float = 1.0) -> Optional[str]:
        for attempt in range(self.max_attempts):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=temperature
                )
                return response.choices[0].message.content.strip()
            except Exception as e:
                if attempt < self.max_attempts - 1:
                    time.sleep(self.retry_delay * (attempt + 1))
                    continue
                raise e
        return None
    
    def _parse_json_response(self, response_text: str) -> Optional[dict]:
        try:
            cleaned_response = response_text.replace('\n', '').replace('\r', '')
            return json.loads(cleaned_response)
        except json.JSONDecodeError:
            try:
                start_idx = cleaned_response.find('{')
                end_idx = cleaned_response.rfind('}') + 1
                if start_idx != -1 and end_idx != 0:
                    json_part = cleaned_response[start_idx:end_idx]
                    return json.loads(json_part)
            except json.JSONDecodeError:
                pass
        return None
    
    def generate_section_titles(self, presentation_title: str, count: int, language: str = "русский") -> List[str]:
        prompt = self.loc.get_prompt(
            "section_titles",
            count=count,
            title=presentation_title
        )
        
        for attempt in range(self.max_attempts):
            response = self._make_request(prompt, temperature=1.0)
            if not response:
                continue
                
            parsed = self._parse_json_response(response)
            if parsed and 'titles' in parsed:
                titles = parsed['titles']
                if isinstance(titles, list):
                    valid_titles = [title for title in titles if self._is_valid_section_title(title)]
                    if len(valid_titles) >= count:
                        return valid_titles[:count]
                elif isinstance(titles, str) and self._is_valid_section_title(titles):
                    return [titles]
            
            if attempt < self.max_attempts - 1:
                time.sleep(self.retry_delay)
        
        default_text = self.loc.t("section_default")
        return [f"{default_text} {i+1}" for i in range(count)]
    
    def _is_valid_section_title(self, title: str) -> bool:
        if not title or len(title.strip()) < 3:
            return False
        
        title_lower = title.lower().strip()
        invalid_patterns = [
            "секция",
            "section",
            "раздел",
            "часть",
            "part"
        ]
        
        for pattern in invalid_patterns:
            if title_lower.startswith(pattern) and any(char.isdigit() for char in title_lower):
                return False
        
        return True
    
    def generate_slide_titles(self, section_title: str, presentation_title: str, count: int, language: str = "русский") -> List[str]:
        prompt = self.loc.get_prompt(
            "slide_titles",
            count=count,
            section_title=section_title,
            presentation_title=presentation_title
        )
        
        for attempt in range(self.max_attempts):
            response = self._make_request(prompt, temperature=1.0)
            if not response:
                continue
                
            parsed = self._parse_json_response(response)
            if parsed and 'titles' in parsed:
                titles = parsed['titles']
                if isinstance(titles, list):
                    valid_titles = [title for title in titles if self._is_valid_slide_title(title)]
                    if len(valid_titles) >= count:
                        return valid_titles[:count]
                elif isinstance(titles, str) and self._is_valid_slide_title(titles):
                    return [titles]
            
            if attempt < self.max_attempts - 1:
                time.sleep(self.retry_delay)
        
        default_text = self.loc.t("slide_default")
        return [f"{default_text} {i+1}" for i in range(count)]
    
    def _is_valid_slide_title(self, title: str) -> bool:
        if not title or len(title.strip()) < 3:
            return False
        
        title_lower = title.lower().strip()
        invalid_patterns = [
            "слайд",
            "slide",
            "страница",
            "page",
            "раздел",
            "section"
        ]
        
        for pattern in invalid_patterns:
            if title_lower.startswith(pattern) and any(char.isdigit() for char in title_lower):
                return False
        
        return True
    
    def generate_slide_content(self, slide_title: str, section_title: str, language: str = "русский") -> str:
        prompt = self.loc.get_prompt(
            "slide_content",
            slide_title=slide_title,
            section_title=section_title
        )
        
        for attempt in range(self.max_attempts):
            response = self._make_request(prompt, temperature=0.8)
            if not response:
                continue
                
            parsed = self._parse_json_response(response)
            if parsed and 'content' in parsed:
                content = parsed['content']
                if self._is_valid_content(content):
                    return content
            
            if attempt < self.max_attempts - 1:
                time.sleep(self.retry_delay)
        
        default_text = self.loc.t("slide_content_default")
        return f"{default_text} '{slide_title}'"
    
    def _is_valid_content(self, content: str) -> bool:
        if not content or len(content.strip()) < 20:
            return False
        
        content_lower = content.lower()
        placeholder_indicators = [
            "содержимое для слайда",
            "content for slide",
            "placeholder",
            "заглушка",
            "введите текст",
            "добавьте контент"
        ]
        
        if any(indicator in content_lower for indicator in placeholder_indicators):
            return False
        
        return True
    
    def generate_presentation_summary(self, presentation_title: str, language: str = "русский") -> str:
        prompt = self.loc.get_prompt(
            "presentation_summary",
            title=presentation_title
        )
        
        response = self._make_request(prompt, temperature=0.7)
        if not response:
            default_text = self.loc.t("presentation_topic")
            return f"{default_text} {presentation_title}"
            
        parsed = self._parse_json_response(response)
        if parsed and 'summary' in parsed:
            return parsed['summary']
        
        default_text = self.loc.t("presentation_topic")
        return f"{default_text} {presentation_title}"
    
    def generate_title_slide_header(self, topic: str, language: str = "русский") -> str:
        prompt = self.loc.get_prompt(
            "title_slide_header",
            topic=topic
        )
        
        response = self._make_request(prompt, temperature=0.8)
        if not response:
            return topic
            
        parsed = self._parse_json_response(response)
        if parsed and 'title' in parsed:
            return parsed['title']
        
        return topic
    
    def generate_title_slide_header(self, topic: str, language: str = "русский") -> str:
        prompt = self.loc.get_prompt("title_slide_header", topic=topic)
        
        response = self._make_request(prompt, temperature=0.8)
        if not response:
            return topic
            
        parsed = self._parse_json_response(response)
        if parsed and 'title' in parsed:
            return parsed['title']
        
        return topic
    
    def generate_conclusion_slide(self, presentation_title: str, language: str = "русский") -> dict:
        prompt = self.loc.get_prompt(
            "conclusion_slide",
            presentation_title=presentation_title
        )
        
        response = self._make_request(prompt, temperature=0.7)
        if not response:
            return {
                "title": "Заключение" if language == "русский" else "Conclusion",
                "content": f"Спасибо за внимание! Презентация на тему '{presentation_title}' завершена."
            }
            
        parsed = self._parse_json_response(response)
        if parsed and 'title' in parsed and 'content' in parsed:
            return {"title": parsed['title'], "content": parsed['content']}
        
        return {
            "title": "Заключение" if language == "русский" else "Conclusion", 
            "content": f"Спасибо за внимание! Презентация на тему '{presentation_title}' завершена."
        }