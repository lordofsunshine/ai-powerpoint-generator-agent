import re
import time
from typing import List, Dict, Optional
from ddgs import DDGS
import requests
from bs4 import BeautifulSoup
from ..localization.manager import get_localization_manager


class WebSearchService:
    def __init__(self, settings_manager=None):
        self.loc = get_localization_manager()
        self.settings = settings_manager
        self.max_results = self.settings.get("search_results_count", 5) if self.settings else 5
        self.max_content_length = 2500
        self.request_delay = 1.0
        
    def search_information(self, query: str, language: str = None) -> Dict[str, any]:
        if language is None:
            from ..localization.manager import get_localization_manager
            loc = get_localization_manager()
            language = loc.t('language_russian')
        try:
            search_results = self._perform_search(query, language)
            if not search_results:
                return {"content": "", "sources": []}
                
            combined_content = self._extract_content_from_results(search_results)
            truncated_content = self._truncate_content(combined_content)
            
            return {
                "content": truncated_content,
                "sources": [result.get("href", "") for result in search_results]
            }
        except Exception as e:
            return {"content": "", "sources": []}
    
    async def search_for_slide(self, slide_title: str, presentation_topic: str = "") -> str:
        if not self.is_search_beneficial(slide_title):
            return ""
        
        try:
            if presentation_topic:
                search_query = f"{slide_title} {presentation_topic} информация факты"
            else:
                search_query = f"{slide_title} информация факты"
            
            search_results = await self._perform_search_async(search_query)
            
            if search_results:
                return search_results
            else:
                return ""
                
        except Exception as e:
            print(f"{self.loc.t('search_error')} для слайда '{slide_title}': {e}")
            return ""
    
    def _perform_search(self, query: str, language: str) -> List[Dict]:
        try:
            if self.settings:
                region = self.settings.get("search_region", "ru-ru")
            else:
                from ..localization.manager import get_localization_manager
                loc = get_localization_manager()
                region = "ru-ru" if language == loc.t('language_russian') else "us-en"
            with DDGS() as ddgs:
                results = list(ddgs.text(
                    query=query,
                    region=region,
                    max_results=self.max_results,
                    safesearch="moderate",
                    timelimit="y"
                ))
            return results
        except Exception as e:
            print(f"{self.loc.t('search_error')}: {e}")
            return []
    
    async def _perform_search_async(self, query: str) -> str:
        try:
            region = self.settings.get("search_region", "ru-ru") if self.settings else "ru-ru"
            with DDGS() as ddgs:
                results = list(ddgs.text(
                    query=query,
                    region=region,
                    max_results=self.max_results,
                    safesearch="moderate",
                    timelimit="y"
                ))
            
            if not results:
                return ""
                
            combined_content = self._extract_content_from_results(results)
            return self._truncate_content(combined_content)
            
        except Exception as e:
            print(f"{self.loc.t('async_search_error')}: {e}")
            return ""
    
    def _extract_content_from_results(self, results: List[Dict]) -> str:
        all_content = []
        
        for result in results:
            snippet = result.get("body", "")
            if snippet:
                all_content.append(snippet)
                
            url = result.get("href", "")
            if url:
                page_content = self._scrape_page_content(url)
                if page_content:
                    all_content.append(page_content)
                    
        return " ".join(all_content)
    
    def _scrape_page_content(self, url: str) -> str:
        try:
            time.sleep(self.request_delay)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code != 200:
                return ""
                
            soup = BeautifulSoup(response.content, 'html.parser')
            
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()
                
            text = soup.get_text(separator=' ', strip=True)
            cleaned_text = re.sub(r'\s+', ' ', text)
            
            return cleaned_text[:800]
        except Exception:
            return ""
    
    def _truncate_content(self, content: str) -> str:
        if len(content) <= self.max_content_length:
            return content
            
        truncated = content[:self.max_content_length]
        last_sentence = truncated.rfind('.')
        
        if last_sentence > self.max_content_length * 0.8:
            return truncated[:last_sentence + 1]
        
        return truncated
    
    def is_search_beneficial(self, slide_title: str) -> bool:
        title_lower = slide_title.lower()
        
        low_value_patterns = [
            r'введение|заключение|итоги|спасибо|вопросы',
            r'introduction|conclusion|summary|thank you|questions'
        ]
        
        for pattern in low_value_patterns:
            if re.search(pattern, title_lower):
                return False
                
        if len(slide_title.strip()) < 5:
            return False
            
        return True