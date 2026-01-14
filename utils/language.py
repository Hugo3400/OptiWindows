"""
Language Manager for OptiWindows
"""

import json
from pathlib import Path
from typing import Dict, Any
from utils.logger import get_logger

logger = get_logger(__name__)


class LanguageManager:
    """Manage application languages"""
    
    def __init__(self):
        self.config_dir = Path(__file__).parent.parent / 'config' / 'lang'
        self.settings_path = Path(__file__).parent.parent / 'config' / 'settings.json'
        self.translations: Dict[str, Any] = {}
        self.current_lang = 'fr'
        self.load_current_language()
        self.load_translations()
    
    def load_translations(self):
        """Load translations from separate language file"""
        try:
            lang_file = self.config_dir / f'{self.current_lang}.json'
            if lang_file.exists():
                with open(lang_file, 'r', encoding='utf-8') as f:
                    self.translations = json.load(f)
                logger.info(f"Loaded translations for language: {self.current_lang}")
            else:
                # Fallback to English
                en_file = self.config_dir / 'en.json'
                if en_file.exists():
                    logger.warning(f"Language file not found: {lang_file}, using English")
                    with open(en_file, 'r', encoding='utf-8') as f:
                        self.translations = json.load(f)
                else:
                    logger.error(f"No translation files found in {self.config_dir}")
                    self.translations = {}
        except Exception as e:
            logger.error(f"Failed to load translations: {e}")
            self.translations = {}
    
    def load_current_language(self):
        """Load current language from settings"""
        try:
            with open(self.settings_path, 'r', encoding='utf-8') as f:
                settings = json.load(f)
                self.current_lang = settings.get('language', 'fr')
            logger.info(f"Current language: {self.current_lang}")
        except Exception as e:
            logger.warning(f"Failed to load language setting: {e}")
            self.current_lang = 'fr'
    
    def set_language(self, lang_code: str) -> bool:
        """Set application language"""
        if lang_code not in ['en', 'fr']:
            logger.error(f"Language not available: {lang_code}")
            return False
        
        try:
            # Update settings
            with open(self.settings_path, 'r', encoding='utf-8') as f:
                settings = json.load(f)
            
            settings['language'] = lang_code
            
            with open(self.settings_path, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2, ensure_ascii=False)
            
            self.current_lang = lang_code
            self.load_translations()  # Reload translations for new language
            logger.info(f"Language changed to: {lang_code}")
            return True
        except Exception as e:
            logger.error(f"Failed to save language setting: {e}")
            return False
    
    def get(self, key: str, default: str = "") -> str:
        """
        Get translation for a key
        Keys can be nested using dot notation: 'nav.dashboard'
        """
        try:
            keys = key.split('.')
            value = self.translations
            
            for k in keys:
                if isinstance(value, dict):
                    value = value.get(k)
                else:
                    return default
            
            return value if value is not None else default
        except Exception as e:
            logger.debug(f"Translation key not found: {key}")
            return default
    
    def get_available_languages(self) -> Dict[str, str]:
        """Get list of available languages"""
        return {
            'en': 'English',
            'fr': 'Français'
        }
    
    def get_current_language(self) -> str:
        """Get current language code"""
        return self.current_lang


# Global instance
_lang_manager = None


def get_language_manager() -> LanguageManager:
    """Get global language manager instance"""
    global _lang_manager
    if _lang_manager is None:
        _lang_manager = LanguageManager()
    return _lang_manager


def t(key: str, default: str = "") -> str:
    """Shorthand for translation"""
    return get_language_manager().get(key, default)
