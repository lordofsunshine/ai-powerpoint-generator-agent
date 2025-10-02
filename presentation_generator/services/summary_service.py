import time
import asyncio
from typing import Optional
from ..localization.manager import get_localization_manager
from .ionet_service import IoNetService


class SummaryService:
    def __init__(self, api_key: str, model: str = "meta-llama/Llama-3.3-70B-Instruct"):
        self.ionet_service = IoNetService(api_key, model)
        self.max_attempts = 3
        self.retry_delay = 1.0
        self.loc = get_localization_manager()
        
    async def summarize_web_content(self, content: str, slide_title: str, language: str = None) -> str:
        if language is None:
            language = self.loc.t('language_russian')
        if not content or len(content.strip()) < 50:
            return ""
            
        prompt = self._build_summary_prompt(content, slide_title, language)
        
        for attempt in range(self.max_attempts):
            try:
                summary = await self.ionet_service.generate_response(prompt, temperature=0.7)
                
                if summary and self._is_valid_summary(summary):
                    return summary
                    
            except Exception as e:
                if attempt < self.max_attempts - 1:
                    await asyncio.sleep(self.retry_delay * (attempt + 1))
                    continue
                    
        return ""
    
    def _build_summary_prompt(self, content: str, slide_title: str, language: str) -> str:
        if language == self.loc.t('language_russian'):
            return f"""
            Ты эксперт по анализу и обработке информации для презентаций. Твоя задача - создать краткое, информативное резюме для слайда презентации.

            ИСХОДНАЯ ИНФОРМАЦИЯ ИЗ ИНТЕРНЕТА:
            {content}

            ЗАГОЛОВОК СЛАЙДА:
            {slide_title}

            ТРЕБОВАНИЯ К РЕЗЮМЕ:
            - Выбери только самую РЕЛЕВАНТНУЮ информацию, которая подходит к заголовку слайда
            - Создай структурированный, логичный текст для использования в презентации
            - Объем: 60-120 слов
            - Используй профессиональный, но доступный язык
            - Включи только проверенные факты и актуальную информацию
            - НЕ используй markdown форматирование
            - Сделай текст готовым для прямого использования в слайде
            - Избегай повторений и воды
            - Фокусируйся на ключевых моментах темы

            СТИЛЬ:
            - Информативный и увлекательный
            - Подходящий для презентации
            - Без избыточных деталей
            - С акцентом на практическую ценность

            Создай качественное резюме, которое дополнит содержание слайда актуальной информацией из интернета.
            """
        else:
            return f"""
            You are an expert in analyzing and processing information for presentations. Your task is to create a brief, informative summary for a presentation slide.

            SOURCE INFORMATION FROM INTERNET:
            {content}

            SLIDE TITLE:
            {slide_title}

            SUMMARY REQUIREMENTS:
            - Select only the most RELEVANT information that fits the slide title
            - Create structured, logical text for use in presentation
            - Length: 60-120 words
            - Use professional but accessible language
            - Include only verified facts and current information
            - DO NOT use markdown formatting
            - Make text ready for direct use in slide
            - Avoid repetitions and filler
            - Focus on key topic points

            STYLE:
            - Informative and engaging
            - Suitable for presentation
            - Without excessive details
            - With emphasis on practical value

            Create a quality summary that will complement slide content with current information from the internet.
            """
    
    def _is_valid_summary(self, summary: str) -> bool:
        if not summary or len(summary.strip()) < 30:
            return False
            
        summary_lower = summary.lower()
        
        invalid_indicators = [
            self.loc.t("cannot"),
            "cannot",
            "sorry",
            self.loc.t("sorry"), 
            "no information",
            self.loc.t("no_information"),
            self.loc.t("insufficient_data"),
            "insufficient data"
        ]
        
        if any(indicator in summary_lower for indicator in invalid_indicators):
            return False
            
        if len(summary.strip()) > 800:
            return False
            
        return True
