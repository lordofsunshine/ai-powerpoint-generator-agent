import os
import sys
import subprocess
import importlib
from pathlib import Path
from typing import List, Tuple

class ProjectValidator:
    def __init__(self):
        self.base_path = self._get_base_path()
        self.required_files = [
            "presentation_generator/__init__.py",
            "presentation_generator/main.py",
            "presentation_generator/models/__init__.py",
            "presentation_generator/models/presentation.py",
            "presentation_generator/services/__init__.py",
            "presentation_generator/services/ai_service.py",
            "presentation_generator/services/presentation_service.py",
            "presentation_generator/services/ionet_service.py",
            "presentation_generator/services/web_search_service.py",
            "presentation_generator/services/summary_service.py",
            "presentation_generator/generators/__init__.py",
            "presentation_generator/generators/pptx_generator.py",
            "presentation_generator/generators/decorations.py",
            "presentation_generator/ui/__init__.py",
            "presentation_generator/ui/cli_interface.py",
            "presentation_generator/localization/__init__.py",
            "presentation_generator/localization/manager.py",
            "presentation_generator/localization/translations.py",
            "presentation_generator/localization/prompts.py",
            "presentation_generator/database/__init__.py",
            "presentation_generator/database/db_manager.py",
            "presentation_generator/config/__init__.py",
            "presentation_generator/config/api_config.py",
            "presentation_generator/config/language.json",
            "requirements.txt",
            "run.py"
        ]
        
        self.required_dirs = [
            "presentation_generator",
            "presentation_generator/models",
            "presentation_generator/services",
            "presentation_generator/generators",
            "presentation_generator/ui",
            "presentation_generator/localization",
            "presentation_generator/database",
            "presentation_generator/config",
            "output"
        ]
    
    def _get_base_path(self) -> Path:
        if getattr(sys, 'frozen', False):
            return Path(sys._MEIPASS).parent
        else:
            return Path(__file__).parent.parent.parent
    
    def validate_project(self) -> Tuple[bool, List[str]]:
        errors = []
        
        if not self._check_files():
            from ..localization.manager import get_localization_manager
            loc = get_localization_manager()
            errors.append(loc.t("project_damaged"))
            return False, errors
        
        self._create_missing_dirs()
        
        missing_packages = self._check_packages()
        if missing_packages:
            from ..localization.manager import get_localization_manager
            loc = get_localization_manager()
            errors.append(f"{loc.t('missing_libraries')}: {', '.join(missing_packages)}")
            return False, errors
        
        return True, []
    
    def _check_files(self) -> bool:
        for file_path in self.required_files:
            full_path = self.base_path / file_path
            if not full_path.exists():
                return False
        return True
    
    def _create_missing_dirs(self):
        for dir_path in self.required_dirs:
            full_path = self.base_path / dir_path
            if not full_path.exists():
                full_path.mkdir(parents=True, exist_ok=True)
    
    def _check_packages(self) -> List[str]:
        requirements_file = self.base_path / "requirements.txt"
        if not requirements_file.exists():
            from ..localization.manager import get_localization_manager
            loc = get_localization_manager()
            return [loc.t("requirements_not_found")]
        
        missing_packages = []
        
        package_mapping = {
            'python-pptx': 'pptx',
            'aiohttp': 'aiohttp',
            'rich': 'rich',
            'requests': 'requests',
            'urllib3': 'urllib3',
            'ddgs': 'ddgs',
            'beautifulsoup4': 'bs4',
            'psutil': 'psutil'
        }
        
        try:
            with open(requirements_file, 'r', encoding='utf-8') as f:
                requirements = f.readlines()
            
            for requirement in requirements:
                requirement = requirement.strip()
                if not requirement or requirement.startswith('#'):
                    continue
                
                package_name = requirement.split('==')[0].split('>=')[0].split('<=')[0].split('>')[0].split('<')[0].split('~')[0]
                
                import_name = package_mapping.get(package_name, package_name)
                
                try:
                    importlib.import_module(import_name)
                except ImportError:
                    missing_packages.append(package_name)
        
        except Exception:
            from ..localization.manager import get_localization_manager
            loc = get_localization_manager()
            missing_packages.append(loc.t("requirements_read_error"))
        
        return missing_packages
