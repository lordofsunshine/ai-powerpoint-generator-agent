#!/usr/bin/env python3

import sys
import os
from pathlib import Path

os.environ['PYTHONHTTPSVERIFY'] = '0'
os.environ['REQUESTS_CA_BUNDLE'] = ''
os.environ['CURL_CA_BUNDLE'] = ''

sys.path.insert(0, str(Path(__file__).parent))

from presentation_generator.utils.project_validator import ProjectValidator

def check_project():
    validator = ProjectValidator()
    is_valid, errors = validator.validate_project()
    
    if not is_valid:
        from presentation_generator.localization.manager import get_localization_manager
        loc = get_localization_manager()
        print(loc.t("problems_detected"))
        for error in errors:
            print(f"{loc.t('error_marker')} {error}")
        print(f"\n{loc.t('continue_with_errors')}")
        print(loc.t("press_enter_continue"))
        input()

if __name__ == "__main__":
    check_project()
    
    from presentation_generator.main import main
    main()
