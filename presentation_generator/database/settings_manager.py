import sqlite3
import json
from pathlib import Path
from ..localization.manager import get_localization_manager


class SettingsManager:
    def __init__(self, db_path: str = "config/settings.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.loc = get_localization_manager()
        self._init_database()
        self._load_defaults()
    
    def _init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
        """)
        
        conn.commit()
        conn.close()
    
    def _load_defaults(self):
        defaults = {
            "interface_language": self.loc.t('language_russian'),
            "slide_size": "16:9",
            "ai_model": "meta-llama/Llama-3.3-70B-Instruct",
            "search_engine": "DuckDuckGo",
            "search_results_count": 5,
            "search_region": "ru-ru",
            "auto_open_presentation": True,
            "developer_mode": False
        }
        
        for key, value in defaults.items():
            if self.get(key) is None:
                self.set(key, value)
    
    def get(self, key: str, default=None):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
            result = cursor.fetchone()
            conn.close()
            
            if result:
                try:
                    return json.loads(result[0])
                except:
                    return result[0]
            return default
        except:
            return default
    
    def set(self, key: str, value):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            json_value = json.dumps(value) if not isinstance(value, str) else value
            
            cursor.execute("""
                INSERT OR REPLACE INTO settings (key, value)
                VALUES (?, ?)
            """, (key, json_value))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            from ..localization.manager import get_localization_manager
            loc = get_localization_manager()
            print(f"{loc.t('settings_save_error')}: {e}")
            return False
    
    def get_all(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT key, value FROM settings")
            results = cursor.fetchall()
            conn.close()
            
            settings = {}
            for key, value in results:
                try:
                    settings[key] = json.loads(value)
                except:
                    settings[key] = value
            
            return settings
        except:
            return {}
    
    def close_connection(self):
        pass
