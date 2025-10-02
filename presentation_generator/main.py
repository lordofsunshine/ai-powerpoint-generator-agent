
import sys
import os
import signal
import atexit
import asyncio
from pathlib import Path
from .localization.manager import get_localization_manager

os.environ['PYTHONHTTPSVERIFY'] = '0'

def get_base_path():
    if getattr(sys, 'frozen', False):
        return Path(sys._MEIPASS)
    else:
        return Path(__file__).parent.parent

def get_resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        return Path(sys._MEIPASS) / relative_path
    else:
        return Path(__file__).parent.parent / relative_path

base_path = get_base_path()
sys.path.insert(0, str(base_path))

from presentation_generator.ui.cli_interface import CLIInterface
from presentation_generator.services.presentation_service import PresentationService
from presentation_generator.config.api_config import ApiKeyManager

app = None
service = None
loc = get_localization_manager()

def cleanup_on_exit():
    global service
    if service:
        try:
            service.cleanup_database()
        except Exception:
            pass

def signal_handler(signum, frame):
    cleanup_on_exit()
    print(f"\n\n{loc.t('program_terminated')}")
    sys.exit(0)

def main():
    global app, service
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    atexit.register(cleanup_on_exit)
    
    try:
        api_manager = ApiKeyManager()
        api_key = api_manager.get_api_key()
        
        app = CLIInterface()
        service = app.service
        app.run()
    except KeyboardInterrupt:
        cleanup_on_exit()
        print(f"\n\n{loc.t('program_terminated')}")
        sys.exit(0)
    except Exception as e:
        cleanup_on_exit()
        print(f"\n{loc.t('critical_error')} {e}")
        print(f"{loc.t('press_enter_exit')}")
        input()
        sys.exit(1)
    finally:
        cleanup_on_exit()


if __name__ == "__main__":
    main()
