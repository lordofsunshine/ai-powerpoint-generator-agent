import json
import sys
import time
import asyncio
from pathlib import Path
from typing import List, Optional
from ..models.presentation import Presentation, Section, Slide
from ..localization.manager import get_localization_manager
from ..localization.prompts import get_current_date
from .ionet_service import IoNetService

def get_resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        return Path(sys._MEIPASS) / relative_path
    else:
        return Path(__file__).parent.parent.parent / relative_path


class AIService:
    def __init__(self, api_key: str, model: str = "deepseek-ai/DeepSeek-R1-0528"):
        self.ionet_service = IoNetService(api_key, model)
        self.max_attempts = 3
        self.retry_delay = 1.0
        self.loc = get_localization_manager()
        
    async def _make_request(self, prompt: str, temperature: float = 1.0) -> Optional[str]:
        for attempt in range(self.max_attempts):
            try:
                response = await self.ionet_service.generate_response(prompt, temperature)
                if response:
                    return response
            except Exception as e:
                if attempt < self.max_attempts - 1:
                    await asyncio.sleep(self.retry_delay * (attempt + 1))
                    continue
                raise e
        return None
    
    def _parse_json_response(self, response_text: str) -> Optional[dict]:
        return self.ionet_service.parse_json_response(response_text)
    
    async def generate_filename(self, title: str, language: str = None) -> str:
        if language is None:
            language = self.loc.t('language_russian')
        try:
            prompt_template = PROMPTS[language]["generate_filename"]
            prompt = prompt_template.format(
                title=title,
                current_date=get_current_date()
            )
            
            response = await self._make_request(prompt, temperature=0.3)
            if response:
                parsed = self._parse_json_response(response)
                if parsed and "filename" in parsed:
                    filename = parsed["filename"].strip()
                    if filename and len(filename) <= 50:
                        return filename
            
            fallback_name = title.replace(" ", "_")[:20]
            safe_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-"
            return "".join(c for c in fallback_name if c in safe_chars) or "Presentation"
            
        except Exception:
            return "Presentation"
    
    async def generate_section_titles(self, presentation_title: str, count: int, language: str = None) -> List[str]:
        if language is None:
            language = self.loc.t('language_russian')
        prompt = self.loc.get_prompt(
            "section_titles",
            count=count,
            title=presentation_title,
            current_date=get_current_date()
        )
        
        for attempt in range(self.max_attempts):
            response = await self._make_request(prompt, temperature=0.7)
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
                await asyncio.sleep(self.retry_delay)
        
        default_text = self.loc.t("section_default")
        return [f"{default_text} {i+1}" for i in range(count)]
    
    def _is_valid_section_title(self, title: str) -> bool:
        if not title or len(title.strip()) < 3:
            return False
        
        title_lower = title.lower().strip()
        invalid_patterns = [
            self.loc.t("section"),
            "section",
            "раздел",
            self.loc.t("part"),
            "part"
        ]
        
        for pattern in invalid_patterns:
            if title_lower.startswith(pattern) and any(char.isdigit() for char in title_lower):
                return False
        
        if title_lower in [f"{self.loc.t('section')} 1", f"{self.loc.t('section')} 2", f"{self.loc.t('section')} 3", f"{self.loc.t('section')} 4", f"{self.loc.t('section')} 5",
                          "section 1", "section 2", "section 3", "section 4", "section 5"]:
            return False
        
        return True
    
    async def generate_slide_titles(self, section_title: str, presentation_title: str, count: int, language: str = None) -> List[str]:
        if language is None:
            language = self.loc.t('language_russian')
        prompt = self.loc.get_prompt(
            "slide_titles",
            count=count,
            section_title=section_title,
            presentation_title=presentation_title,
            current_date=get_current_date()
        )
        
        for attempt in range(self.max_attempts):
            response = await self._make_request(prompt, temperature=0.7)
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
                await asyncio.sleep(self.retry_delay)
        
        default_text = self.loc.t("slide_default")
        return [f"{default_text} {i+1}" for i in range(count)]
    
    def _is_valid_slide_title(self, title: str) -> bool:
        if not title or len(title.strip()) < 3:
            return False
        
        title_lower = title.lower().strip()
        invalid_patterns = [
            self.loc.t("slide"),
            "slide",
            self.loc.t("page"),
            "page",
            "раздел",
            "section"
        ]
        
        for pattern in invalid_patterns:
            if title_lower.startswith(pattern) and any(char.isdigit() for char in title_lower):
                return False
        
        if title_lower in [f"{self.loc.t('slide')} 1", f"{self.loc.t('slide')} 2", f"{self.loc.t('slide')} 3", f"{self.loc.t('slide')} 4", f"{self.loc.t('slide')} 5", 
                          "slide 1", "slide 2", "slide 3", "slide 4", "slide 5"]:
            return False
        
        return True
    
    async def generate_slide_content(self, slide_title: str, section_title: str, language: str = None) -> str:
        if language is None:
            language = self.loc.t('language_russian')
        prompt = self.loc.get_prompt(
            "slide_content",
            slide_title=slide_title,
            section_title=section_title,
            current_date=get_current_date(),
            language=language
        )
        
        for attempt in range(self.max_attempts):
            response = await self._make_request(prompt, temperature=0.5)
            if not response:
                continue
                
            parsed = self._parse_json_response(response)
            if parsed and 'content' in parsed:
                content = parsed['content']
                if self._is_valid_content(content) and not self._is_placeholder_content(content):
                    return content
            
            if attempt < self.max_attempts - 1:
                await asyncio.sleep(self.retry_delay)
        
        default_text = self.loc.t("slide_content_default")
        return f"{default_text} '{slide_title}'"
    
    def _is_placeholder_content(self, content: str) -> bool:
        if not content or len(content.strip()) < 15:
            return True
        
        content_lower = content.lower()
        placeholder_indicators = [
            self.loc.t("content_for_slide"),
            "content for slide",  
            self.loc.t("placeholder"),
            self.loc.t("placeholder"),
            "здесь будет",
            self.loc.t("text_for_slide")
        ]
        
        for indicator in placeholder_indicators:
            if indicator in content_lower:
                return True
            
        return False
    
    def _is_valid_content(self, content: str) -> bool:
        if not content or len(content.strip()) < 20:
            return False
        
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
        
        if any(indicator in content_lower for indicator in placeholder_indicators):
            return False
        
        return True
    
    async def generate_presentation_summary(self, presentation_title: str, language: str = None) -> str:
        if language is None:
            language = self.loc.t('language_russian')
        prompt = self.loc.get_prompt(
            "presentation_summary",
            title=presentation_title,
            current_date=get_current_date()
        )
        
        response = await self._make_request(prompt, temperature=0.7)
        if not response:
            default_text = self.loc.t("presentation_topic")
            return f"{default_text} {presentation_title}"
            
        parsed = self._parse_json_response(response)
        if parsed and 'summary' in parsed:
            return parsed['summary']
        
        default_text = self.loc.t("presentation_topic")
        return f"{default_text} {presentation_title}"
    
    async def generate_title_slide_header(self, topic: str, language: str = None) -> str:
        if language is None:
            language = self.loc.t('language_russian')
        prompt = self.loc.get_prompt(
            "title_slide_header",
            topic=topic
        )
        
        response = await self._make_request(prompt, temperature=0.8)
        if not response:
            return topic
            
        parsed = self._parse_json_response(response)
        if parsed and 'title' in parsed:
            return parsed['title']
        
        return topic
    
    async def generate_conclusion_slide(self, presentation_title: str, language: str = None) -> dict:
        if language is None:
            language = self.loc.t('language_russian')
        prompt = self.loc.get_prompt(
            "conclusion_slide",
            presentation_title=presentation_title
        )
        
        response = await self._make_request(prompt, temperature=0.7)
        if not response:
            return {
                "title": self.loc.t("conclusion") if language == self.loc.t('language_russian') else "Conclusion",
                "content": f"{self.loc.t('thank_you_attention')} '{presentation_title}' завершена."
            }
            
        parsed = self._parse_json_response(response)
        if parsed and 'title' in parsed and 'content' in parsed:
            return {"title": parsed['title'], "content": parsed['content']}
        
        return {
            "title": self.loc.t("conclusion") if language == self.loc.t('language_russian') else "Conclusion", 
            "content": f"{self.loc.t('thank_you_attention')} '{presentation_title}' завершена."
        }
    
    async def enhance_content_with_web_info(self, base_content: str, web_summary: str, slide_title: str, language: str = None) -> str:
        if language is None:
            language = self.loc.t('language_russian')
        if not web_summary or len(web_summary.strip()) < 20:
            return base_content
            
        prompt = self.loc.get_prompt(
            "web_enhanced_content",
            base_content=base_content,
            web_summary=web_summary,
            slide_title=slide_title
        )
        
        for attempt in range(self.max_attempts):
            response = await self._make_request(prompt, temperature=0.7)
            if not response:
                continue
                
            parsed = self._parse_json_response(response)
            if parsed and 'content' in parsed:
                enhanced_content = parsed['content']
                if self._is_valid_content(enhanced_content):
                    return enhanced_content
            
            if attempt < self.max_attempts - 1:
                await asyncio.sleep(self.retry_delay)
        
        return base_content
    
    def fix_line_breaks(self, content: str, language: str = None) -> str:
        if language is None:
            language = self.loc.t('language_russian')
        if not content or len(content.strip()) < 10:
            return content
        
        if content.strip().startswith('TABLE|'):
            return content
        
        content = self._clean_markdown(content)
        return self._add_line_breaks_manually(content)
    
    def _clean_markdown(self, content: str) -> str:
        import re
        
        if not content:
            return content
        
        content = re.sub(r'\*\*(.*?)\*\*', r'\1', content)
        content = re.sub(r'\*(.*?)\*', r'\1', content)
        content = re.sub(r'__(.*?)__', r'\1', content)
        content = re.sub(r'_(.*?)_', r'\1', content)
        content = re.sub(r'~~(.*?)~~', r'\1', content)
        content = re.sub(r'`(.*?)`', r'\1', content)
        content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
        content = re.sub(r'```.*', '', content, flags=re.DOTALL)
        content = re.sub(r'#{1,6}\s*', '', content)
        content = re.sub(r'^\s*[-*+]\s*', '', content, flags=re.MULTILINE)
        content = re.sub(r'^\s*\d+\.\s*', '', content, flags=re.MULTILINE)
        content = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', content)
        content = re.sub(r'!\[([^\]]*)\]\([^)]+\)', r'\1', content)
        content = re.sub(r'^---+$', '', content, flags=re.MULTILINE)
        content = re.sub(r'^\s*>\s*', '', content, flags=re.MULTILINE)
        content = re.sub(r'^\s*\|.*\|.*$', '', content, flags=re.MULTILINE)
        content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)
        content = content.strip()
        
        return content
    
    def _add_line_breaks_manually(self, content: str) -> str:
        if not content:
            return content
        
        import re
        
        lines = []
        
        if ':' in content and any(word in content.lower() for word in ['основные', 'ключевые', 'главные', 'важные', 'преимущества', 'недостатки', 'этапы', 'шаги', 'причины', 'результаты', 'направления', 'включают', 'будет', 'рост', 'повышение', 'новые', 'этапы роста', 'олицетворяли', 'символизировал', 'подчеркивает', 'выражает', 'оборачивался']):
            parts = content.split(':', 1)
            if len(parts) == 2:
                lines.append(parts[0].strip() + ':')
                items_text = parts[1].strip()
                
                if '•' in items_text:
                    items = [item.strip() for item in items_text.split('•') if item.strip()]
                    for item in items:
                        if item:
                            lines.append('• ' + item)
                else:
                    items = [item.strip() for item in items_text.replace('.', '').split(',') if item.strip()]
                    for item in items:
                        if item:
                            lines.append('• ' + item)
            else:
                lines.append(content)
        else:
            sentences = re.split(r'[.!?]\s+', content)
            for sentence in sentences:
                sentence = sentence.strip()
                if sentence:
                    if not sentence.endswith(('.', '!', '?')):
                        sentence += '.'
                    
                    if '•' in sentence:
                        parts = sentence.split('•')
                        if len(parts) > 1:
                            lines.append(parts[0].strip())
                            for part in parts[1:]:
                                part = part.strip()
                                if part:
                                    lines.append('• ' + part)
                        else:
                            lines.append(sentence)
                    elif any(word in sentence.lower() for word in ['позволяющее', 'зависит', 'такие как', 'в то время как', 'отличаются', 'потерей', 'беспомощность', 'утрату', 'каждый', 'уравнение', 'технологический', 'разрушение', 'сломанный']) and ',' in sentence:
                        parts = sentence.split(',', 1)
                        if len(parts) == 2:
                            lines.append(parts[0].strip())
                            items = [item.strip() for item in parts[1].replace('.', '').split(',') if item.strip()]
                            for item in items:
                                if item:
                                    lines.append('• ' + item)
                        else:
                            lines.append(sentence)
                    else:
                        lines.append(sentence)
        
        result_lines = []
        for line in lines:
            if len(line) > 45:
                words = line.split()
                current_line = ""
                for i, word in enumerate(words):
                    if len(current_line + " " + word) <= 45:
                        if current_line:
                            current_line += " " + word
                        else:
                            current_line = word
                    else:
                        if current_line:
                            last_word = current_line.split()[-1] if current_line.split() else ""
                            if len(last_word) < 3 and i < len(words) - 1 and len(current_line + " " + word) <= 50:
                                current_line += " " + word
                            else:
                                result_lines.append(current_line)
                                current_line = word
                        else:
                            current_line = word
                if current_line:
                    result_lines.append(current_line)
            else:
                result_lines.append(line)
        
        result = '\n'.join(result_lines)
        
        if len(result) < len(content) * 0.7:
            return content
            
        return result