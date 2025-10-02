import os
import sys
from pathlib import Path
from ..localization.manager import get_localization_manager


class ApiKeyManager:
    def __init__(self):
        self.config_file = self._get_config_path()
        self.loc = get_localization_manager()
        
    def _get_config_path(self) -> Path:
        if getattr(sys, 'frozen', False):
            base_dir = Path(sys._MEIPASS).parent
        else:
            base_dir = Path(__file__).parent.parent.parent
            
        config_dir = base_dir / "config"
        config_created = not config_dir.exists()
        config_dir.mkdir(exist_ok=True)
        
        if config_created:
            self._config_was_created = True
        else:
            self._config_was_created = False
            
        return config_dir / "api_key.txt"
    
    def get_api_key(self) -> str:
        if hasattr(self, '_config_was_created') and self._config_was_created:
            print(f"\n{self.loc.t('config_directory_created')}")
            return self._request_new_key()
        
        if not self.config_file.exists():
            print(f"\n{self.loc.t('api_key_file_not_found')}")
            return self._request_new_key()
            
        api_key = self._load_saved_key()
        
        if api_key and self._is_key_valid(api_key):
            return api_key
            
        return self._request_new_key()
    
    def _load_saved_key(self) -> str:
        try:
            if self.config_file.exists():
                return self.config_file.read_text().strip()
        except:
            pass
        return ""
    
    def _save_key(self, api_key: str):
        try:
            self.config_file.write_text(api_key)
        except:
            pass
    
    def _is_key_valid(self, api_key: str) -> bool:
        if not api_key or len(api_key) < 10:
            return False
            
        try:
            import asyncio
            from ..services.ionet_service import IoNetService
            service = IoNetService(api_key)
            result = asyncio.run(service.test_api_key())
            return result
        except Exception as e:
            print(f"{self.loc.t('api_key_check_error')}: {e}")
            return False
    
    def _request_new_key(self) -> str:
        while True:
            print(f"\n{self.loc.t('ionet_api_key_required')}")
            print(f"{self.loc.t('ionet_api_key_info')}")
            
            api_key = input(f"{self.loc.t('enter_ionet_api_key')}: ").strip()
            
            if not api_key:
                print(f"{self.loc.t('api_key_empty')}")
                continue
                
            print(f"{self.loc.t('testing_api_key')}")
            
            if self._is_key_valid(api_key):
                self._save_key(api_key)
                print(f"{self.loc.t('api_key_valid')}")
                return api_key
            else:
                print(f"{self.loc.t('api_key_invalid')}")
                retry = input(f"{self.loc.t('try_again')} (y/n): ").lower()
                if retry != 'y':
                    sys.exit(1)
