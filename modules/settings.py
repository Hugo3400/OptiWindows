"""
Settings Module - Configure application settings
"""

import customtkinter as ctk
from tkinter import messagebox, filedialog
import json
from pathlib import Path
from utils.logger import get_logger
from utils.config_manager import ConfigManager
from utils.language import get_language_manager, t

logger = get_logger(__name__)


class SettingsModule:
    """Settings module for OptiWindows"""
    
    def __init__(self, parent):
        self.parent = parent
        self.frame = ctk.CTkScrollableFrame(parent, fg_color="transparent")
        self.config = ConfigManager()
        self.lang = get_language_manager()
        self.settings = self.config.settings.copy()
        
        self.create_ui()
    
    def create_ui(self):
        """Create settings UI"""
        # Title
        title = ctk.CTkLabel(
            self.frame,
            text="⚙️ " + t('settings.title', 'Settings'),
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.pack(pady=20)
        
        # General Settings Section
        self.create_section(t('settings.general', 'General Settings'))
        
        # Language
        lang_frame = self.create_setting_frame()
        ctk.CTkLabel(
            lang_frame,
            text="🌐 " + t('settings.language', 'Language'),
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=10)
        
        self.lang_var = ctk.StringVar(value=self.settings.get('language', 'fr'))
        lang_menu = ctk.CTkOptionMenu(
            lang_frame,
            values=['English', 'Français'],
            command=self.change_language,
            variable=self.lang_var,
            width=150
        )
        # Set display value
        lang_menu.set('Français' if self.lang_var.get() == 'fr' else 'English')
        lang_menu.pack(side="right", padx=10)
        
        # Theme
        theme_frame = self.create_setting_frame()
        ctk.CTkLabel(
            theme_frame,
            text="🎨 " + t('settings.theme', 'Theme'),
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=10)
        
        self.theme_var = ctk.StringVar(value=self.settings.get('theme', 'dark'))
        theme_menu = ctk.CTkOptionMenu(
            theme_frame,
            values=[t('settings.dark', 'Dark'), t('settings.light', 'Light'), t('settings.system', 'System')],
            command=self.change_theme,
            variable=self.theme_var,
            width=150
        )
        theme_menu.pack(side="right", padx=10)
        
        # Auto Backup
        self.create_toggle_setting(
            "💾 " + t('settings.auto_backup', 'Automatic Backup Before Changes'),
            'auto_backup',
            self.settings.get('auto_backup', True)
        )
        
        # Show Warnings
        self.create_toggle_setting(
            "⚠️ " + t('settings.show_warnings', 'Show Warning Messages'),
            'show_warnings',
            self.settings.get('show_warnings', True)
        )
        
        # Advanced Mode
        self.create_toggle_setting(
            "🔧 " + t('settings.advanced_mode', 'Advanced Mode'),
            'advanced_mode',
            self.settings.get('advanced_mode', False)
        )
        
        # Auto Update Check
        self.create_toggle_setting(
            "🔄 " + t('settings.auto_update', 'Automatic Update Check'),
            'auto_update_check',
            self.settings.get('auto_update_check', True)
        )
        
        # Optimization Settings Section
        self.create_section(t('settings.optimization', 'Optimization Settings'))
        
        # Create Restore Point
        self.create_toggle_setting(
            "📌 " + t('settings.restore_point', 'Create Restore Point Before Optimization'),
            'optimization.create_restore_point',
            self.settings.get('optimization', {}).get('create_restore_point', True)
        )
        
        # Aggressive Cleaning
        self.create_toggle_setting(
            "⚡ " + t('settings.aggressive', 'Aggressive Cleaning Mode'),
            'optimization.aggressive_cleaning',
            self.settings.get('optimization', {}).get('aggressive_cleaning', False)
        )
        
        # Deep Scan
        self.create_toggle_setting(
            "🔍 " + t('settings.deep_scan', 'Deep Scan'),
            'optimization.deep_scan',
            self.settings.get('optimization', {}).get('deep_scan', True)
        )
        
        # Scheduled Tasks Section
        self.create_section(t('settings.scheduled', 'Scheduled Tasks'))
        
        # Enable Scheduled Tasks
        self.create_toggle_setting(
            "⏰ " + t('settings.enable_scheduled', 'Enable Scheduled Tasks'),
            'scheduled_tasks.enabled',
            self.settings.get('scheduled_tasks', {}).get('enabled', False)
        )
        
        # Frequency
        freq_frame = self.create_setting_frame()
        ctk.CTkLabel(
            freq_frame,
            text="📅 " + t('settings.frequency', 'Frequency'),
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=10)
        
        self.freq_var = ctk.StringVar(
            value=self.settings.get('scheduled_tasks', {}).get('frequency', 'weekly')
        )
        freq_menu = ctk.CTkOptionMenu(
            freq_frame,
            values=[
                t('settings.daily', 'Daily'),
                t('settings.weekly', 'Weekly'),
                t('settings.monthly', 'Monthly')
            ],
            variable=self.freq_var,
            width=150
        )
        freq_menu.pack(side="right", padx=10)
        
        # About Section
        self.create_section(t('settings.about', 'About'))
        
        # Version
        version_frame = self.create_setting_frame()
        ctk.CTkLabel(
            version_frame,
            text="ℹ️ " + t('settings.version', 'Version'),
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=10)
        
        ctk.CTkLabel(
            version_frame,
            text="1.0.0",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(side="right", padx=10)
        
        # Action Buttons
        button_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=20, pady=30)
        
        # Check Update
        ctk.CTkButton(
            button_frame,
            text="🔄 " + t('settings.check_update', 'Check for Updates'),
            command=self.check_update,
            width=200,
            height=40,
            fg_color="#2196F3",
            hover_color="#1976D2"
        ).pack(side="left", padx=10)
        
        # GitHub
        ctk.CTkButton(
            button_frame,
            text="🔗 " + t('settings.github', 'View on GitHub'),
            command=self.open_github,
            width=200,
            height=40,
            fg_color="#4CAF50",
            hover_color="#388E3C"
        ).pack(side="left", padx=10)
        
        # Export Config
        ctk.CTkButton(
            button_frame,
            text="📤 " + t('settings.export', 'Export Configuration'),
            command=self.export_config,
            width=200,
            height=40,
            fg_color="#FF9800",
            hover_color="#F57C00"
        ).pack(side="left", padx=10)
        
        # Import Config
        ctk.CTkButton(
            button_frame,
            text="📥 " + t('settings.import', 'Import Configuration'),
            command=self.import_config,
            width=200,
            height=40,
            fg_color="#9C27B0",
            hover_color="#7B1FA2"
        ).pack(side="left", padx=10)
        
        # Bottom Buttons
        bottom_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        bottom_frame.pack(fill="x", padx=20, pady=20)
        
        # Save
        ctk.CTkButton(
            bottom_frame,
            text="💾 " + t('settings.save', 'Save Settings'),
            command=self.save_settings,
            width=250,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#4CAF50",
            hover_color="#388E3C"
        ).pack(side="left", padx=10)
        
        # Reset
        ctk.CTkButton(
            bottom_frame,
            text="🔄 " + t('settings.reset', 'Reset to Defaults'),
            command=self.reset_settings,
            width=250,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#F44336",
            hover_color="#D32F2F"
        ).pack(side="right", padx=10)
    
    def create_section(self, title: str):
        """Create a section header"""
        frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        frame.pack(fill="x", padx=20, pady=(20, 10))
        
        ctk.CTkLabel(
            frame,
            text=title,
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#1E88E5"
        ).pack(anchor="w")
        
        # Separator
        separator = ctk.CTkFrame(frame, height=2, fg_color="#1E88E5")
        separator.pack(fill="x", pady=(5, 0))
    
    def create_setting_frame(self) -> ctk.CTkFrame:
        """Create a frame for a setting"""
        frame = ctk.CTkFrame(self.frame, height=50, fg_color="#2B2B2B")
        frame.pack(fill="x", padx=20, pady=5)
        return frame
    
    def create_toggle_setting(self, label: str, key: str, default: bool):
        """Create a toggle setting"""
        frame = self.create_setting_frame()
        
        ctk.CTkLabel(
            frame,
            text=label,
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=10, pady=10)
        
        switch = ctk.CTkSwitch(
            frame,
            text="",
            command=lambda: self.toggle_setting(key, switch.get())
        )
        if default:
            switch.select()
        switch.pack(side="right", padx=10, pady=10)
    
    def toggle_setting(self, key: str, value: bool):
        """Toggle a setting"""
        keys = key.split('.')
        if len(keys) == 1:
            self.settings[key] = value
        else:
            if keys[0] not in self.settings:
                self.settings[keys[0]] = {}
            self.settings[keys[0]][keys[1]] = value
    
    def change_language(self, choice: str):
        """Change application language"""
        lang_code = 'fr' if choice == 'Français' else 'en'
        if self.lang.set_language(lang_code):
            messagebox.showinfo(
                t('common.success', 'Success'),
                "Language changed! Please restart the application for full effect.\n\n"
                "Langue modifiée ! Veuillez redémarrer l'application pour un effet complet."
            )
    
    def change_theme(self, choice: str):
        """Change application theme"""
        theme_map = {
            'Dark': 'dark',
            'Sombre': 'dark',
            'Light': 'light',
            'Clair': 'light',
            'System': 'system',
            'Système': 'system'
        }
        theme = theme_map.get(choice, 'dark')
        ctk.set_appearance_mode(theme)
        self.settings['theme'] = theme
    
    def check_update(self):
        """Check for updates"""
        try:
            from utils.auto_update import AutoUpdater
            updater = AutoUpdater()
            update_info = updater.check_for_updates()
            
            if update_info:
                messagebox.showinfo(
                    t('common.success', 'Success'),
                    f"Update available: {update_info.get('version')}\n{update_info.get('notes', '')}"
                )
            else:
                messagebox.showinfo(
                    t('common.success', 'Success'),
                    "You have the latest version!"
                )
        except Exception as e:
            messagebox.showerror(
                t('common.error', 'Error'),
                f"Failed to check for updates: {e}"
            )
    
    def open_github(self):
        """Open GitHub repository"""
        import webbrowser
        webbrowser.open('https://github.com/Hugo3400/OptiWindows')
    
    def export_config(self):
        """Export configuration"""
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(self.settings, f, indent=2, ensure_ascii=False)
                
                messagebox.showinfo(
                    t('common.success', 'Success'),
                    "Configuration exported successfully!"
                )
        except Exception as e:
            messagebox.showerror(t('common.error', 'Error'), f"Export failed: {e}")
    
    def import_config(self):
        """Import configuration"""
        try:
            file_path = filedialog.askopenfilename(
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            if file_path:
                with open(file_path, 'r', encoding='utf-8') as f:
                    imported = json.load(f)
                
                self.settings.update(imported)
                messagebox.showinfo(
                    t('common.success', 'Success'),
                    "Configuration imported! Please save and restart."
                )
        except Exception as e:
            messagebox.showerror(t('common.error', 'Error'), f"Import failed: {e}")
    
    def save_settings(self):
        """Save settings to file"""
        try:
            # Update config manager settings
            self.config.settings = self.settings
            self.config.save_settings()
            messagebox.showinfo(
                t('common.success', 'Success'),
                "Settings saved successfully!"
            )
            logger.info("Settings saved")
        except Exception as e:
            messagebox.showerror(
                t('common.error', 'Error'),
                f"Failed to save settings: {e}"
            )
    
    def reset_settings(self):
        """Reset settings to defaults"""
        if messagebox.askyesno(
            t('common.warning', 'Warning'),
            "Reset all settings to default values?"
        ):
            try:
                # Default settings
                defaults = {
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
                    "scheduled_tasks": {
                        "enabled": False,
                        "frequency": "weekly"
                    }
                }
                
                self.config.settings = defaults
                self.config.save_settings()
                messagebox.showinfo(
                    t('common.success', 'Success'),
                    "Settings reset! Please restart the application."
                )
            except Exception as e:
                messagebox.showerror(
                    t('common.error', 'Error'),
                    f"Failed to reset settings: {e}"
                )
    
    def get_frame(self):
        """Return the module frame"""
        return self.frame
