import json
import os
import sys
from pathlib import Path
from .translations import TRANSLATIONS

DEFAULT_LANGUAGE = "русский"
from .prompts import PROMPTS, get_current_date

def get_resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        return Path(sys._MEIPASS) / relative_path
    else:
        return Path(__file__).parent.parent.parent / relative_path


class LocalizationManager:
    def __init__(self):
        self.config_file = get_resource_path("presentation_generator/config/language.json")
        self.config_file.parent.mkdir(exist_ok=True)
        self.current_language = self._load_language()
    
    def _load_language(self) -> str:
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    return config.get('language', DEFAULT_LANGUAGE)
        except Exception:
            pass
        return DEFAULT_LANGUAGE
    
    def _save_language(self, language: str):
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump({'language': language}, f, ensure_ascii=False, indent=2)
        except Exception:
            pass
    
    def set_language(self, language: str):
        if language in TRANSLATIONS:
            self.current_language = language
            self._save_language(language)
            return True
        return False
    
    def get_language(self) -> str:
        return self.current_language
    
    def get_available_languages(self) -> list:
        return list(TRANSLATIONS.keys())
    
    def t(self, key: str, *args, **kwargs) -> str:
        try:
            text = TRANSLATIONS[self.current_language].get(key, key)
            if args:
                return text.format(*args)
            elif kwargs:
                return text.format(**kwargs)
            return text
        except Exception:
            return key
    
    def get_prompt(self, prompt_type: str, **kwargs) -> str:
        try:
            prompt_template = PROMPTS[self.current_language][prompt_type]
            if 'current_date' not in kwargs:
                kwargs['current_date'] = get_current_date()
            return prompt_template.format(**kwargs)
        except Exception as e:
            print(f"ERROR in get_prompt: {e}")
            return ""


_localization_manager = LocalizationManager()

def get_localization_manager() -> LocalizationManager:
    return _localization_manager
