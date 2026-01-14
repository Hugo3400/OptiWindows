"""
Gestionnaire de configuration pour OptiWindows
Gère les paramètres et profils de l'application
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional

class ConfigManager:
    def __init__(self, config_dir: str = "config"):
        """
        Initialise le gestionnaire de configuration
        
        Args:
            config_dir: Répertoire contenant les fichiers de configuration
        """
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(exist_ok=True)
        
        self.settings_file = self.config_dir / "settings.json"
        self.profiles_file = self.config_dir / "profiles.json"
        
        self.settings = self.load_settings()
        self.profiles = self.load_profiles()
    
    def load_settings(self) -> Dict[str, Any]:
        """Charge les paramètres depuis le fichier"""
        if self.settings_file.exists():
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Erreur lors du chargement des paramètres: {e}")
                return self.get_default_settings()
        return self.get_default_settings()
    
    def load_profiles(self) -> Dict[str, Any]:
        """Charge les profils depuis le fichier"""
        if self.profiles_file.exists():
            try:
                with open(self.profiles_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Erreur lors du chargement des profils: {e}")
                return self.get_default_profiles()
        return self.get_default_profiles()
    
    def save_settings(self) -> bool:
        """Sauvegarde les paramètres"""
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Erreur lors de la sauvegarde des paramètres: {e}")
            return False
    
    def save_profiles(self) -> bool:
        """Sauvegarde les profils"""
        try:
            with open(self.profiles_file, 'w', encoding='utf-8') as f:
                json.dump(self.profiles, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Erreur lors de la sauvegarde des profils: {e}")
            return False
    
    def get_setting(self, key: str, default: Any = None) -> Any:
        """
        Récupère un paramètre
        
        Args:
            key: Clé du paramètre (peut être imbriquée avec '.')
            default: Valeur par défaut si non trouvé
        """
        keys = key.split('.')
        value = self.settings
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set_setting(self, key: str, value: Any) -> bool:
        """
        Définit un paramètre
        
        Args:
            key: Clé du paramètre (peut être imbriquée avec '.')
            value: Nouvelle valeur
        """
        keys = key.split('.')
        settings = self.settings
        
        for k in keys[:-1]:
            if k not in settings:
                settings[k] = {}
            settings = settings[k]
        
        settings[keys[-1]] = value
        return self.save_settings()
    
    def get_active_profile(self) -> Dict[str, Any]:
        """Récupère le profil actif"""
        active_name = self.get_setting('custom_profiles.active_profile', 'default')
        return self.profiles.get('profiles', {}).get(active_name, {})
    
    def set_active_profile(self, profile_name: str) -> bool:
        """Définit le profil actif"""
        if profile_name in self.profiles.get('profiles', {}):
            return self.set_setting('custom_profiles.active_profile', profile_name)
        return False
    
    def get_all_profiles(self) -> Dict[str, Dict[str, Any]]:
        """Récupère tous les profils"""
        return self.profiles.get('profiles', {})
    
    def export_config(self, filepath: str) -> bool:
        """Exporte la configuration complète"""
        try:
            config = {
                'settings': self.settings,
                'active_profile': self.get_setting('custom_profiles.active_profile')
            }
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Erreur lors de l'export: {e}")
            return False
    
    def import_config(self, filepath: str) -> bool:
        """Importe une configuration"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            if 'settings' in config:
                self.settings = config['settings']
                self.save_settings()
            
            if 'active_profile' in config:
                self.set_active_profile(config['active_profile'])
            
            return True
        except Exception as e:
            print(f"Erreur lors de l'import: {e}")
            return False
    
    @staticmethod
    def get_default_settings() -> Dict[str, Any]:
        """Retourne les paramètres par défaut"""
        return {
            "version": "1.0.0",
            "language": "fr",
            "theme": "dark",
            "auto_backup": True,
            "show_warnings": True,
            "advanced_mode": False,
            "telemetry": False,
            "auto_update_check": True,
            "optimization": {
                "create_restore_point": True,
                "aggressive_cleaning": False,
                "deep_scan": True
            },
            "privacy": {
                "disable_telemetry": True,
                "disable_cortana": True,
                "disable_ads": True,
                "disable_suggestions": True
            },
            "gaming": {
                "ultimate_performance": False,
                "disable_game_bar": True,
                "optimize_gpu": True
            },
            "custom_profiles": {
                "active_profile": "default"
            }
        }
    
    @staticmethod
    def get_default_profiles() -> Dict[str, Any]:
        """Retourne les profils par défaut"""
        return {
            "profiles": {
                "default": {
                    "name": "Par défaut",
                    "description": "Configuration équilibrée",
                    "settings": {
                        "clean_temp": True,
                        "clean_cache": True,
                        "optimize_startup": True,
                        "disable_telemetry": True
                    }
                }
            }
        }
