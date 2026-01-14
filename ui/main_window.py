"""
Main Window UI - OptiWindows
"""

import customtkinter as ctk
from tkinter import messagebox
import threading
from typing import Dict, Any

from modules.cleaner import CleanerModule
from modules.optimizer import OptimizerModule
from modules.privacy import PrivacyModule
from modules.gaming import GamingModule
from modules.disk_manager import DiskManagerModule
from modules.startup_manager import StartupManagerModule
from modules.apps_installer import AppsInstallerModule
from modules.tweaks import TweaksModule
from modules.repair import RepairModule
from modules.features import FeaturesModule
from modules.settings import SettingsModule
from utils.system_info import SystemInfo
from utils.logger import get_logger
from utils.auto_update import AutoUpdater
from utils.language import get_language_manager, t

logger = get_logger(__name__)


class MainWindow(ctk.CTk):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        
        # Window configuration
        self.title("OptiWindows - Ultimate Windows Optimizer")
        self.geometry("1400x900")
        self.minsize(1200, 800)
        
        # State
        self.current_module = None
        self.system_info = SystemInfo()
        self.modules: Dict[str, Any] = {}
        self.updater = AutoUpdater()
        self.update_available = False
        
        # Setup UI
        self.setup_ui()
        
        # Load system info (avec délai pour alléger le démarrage)
        threading.Timer(0.5, self.load_system_info).start()
        
        # Check for updates in background
        threading.Timer(2.0, self.check_for_updates).start()
        
        logger.info("MainWindow initialized")
    
    def setup_ui(self):
        """Setup the user interface"""
        # Configure grid
        self.grid_rowconfigure(0, weight=0)  # Header
        self.grid_rowconfigure(1, weight=1)  # Content
        self.grid_columnconfigure(0, weight=0)  # Sidebar
        self.grid_columnconfigure(1, weight=1)  # Main content
        
        # Create header
        self.create_header()
        
        # Create main content area (AVANT sidebar pour que content_frame existe)
        self.create_content_area()
        
        # Create sidebar
        self.create_sidebar()
        
        # Create status bar
        self.create_status_bar()
        
        # Show dashboard AFTER everything is created
        self.show_module("dashboard")
    
    def create_header(self):
        """Create header with logo and system info"""
        header_frame = ctk.CTkFrame(self, height=80, corner_radius=0)
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=0, pady=0)
        header_frame.grid_columnconfigure(1, weight=1)
        
        # Logo and title
        title_label = ctk.CTkLabel(
            header_frame,
            text="⚡ OptiWindows",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.grid(row=0, column=0, padx=20, pady=20, sticky="w")
        
        # System info
        self.system_info_label = ctk.CTkLabel(
            header_frame,
            text="Loading system info...",
            font=ctk.CTkFont(size=12)
        )
        self.system_info_label.grid(row=0, column=1, padx=20, pady=20, sticky="e")
        
        # Health score (will be updated)
        self.health_score_label = ctk.CTkLabel(
            header_frame,
            text="Health: --/100",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="green"
        )
        self.health_score_label.grid(row=0, column=2, padx=20, pady=20, sticky="e")
    
    def create_sidebar(self):
        """Create sidebar with navigation"""
        sidebar_frame = ctk.CTkFrame(self, width=250, corner_radius=0)
        sidebar_frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        sidebar_frame.grid_rowconfigure(20, weight=1)
        
        # Navigation buttons
        nav_items = [
            ("🏠 Dashboard", "dashboard"),
            ("🧹 Cleaner", "cleaner"),
            ("⚡ Optimizer", "optimizer"),
            ("� Privacy", "privacy"),
            ("🎮 Gaming", "gaming"),
            ("💿 Disk Manager", "disk"),
            ("🚀 Startup", "startup"),
            ("📦 Apps", "apps"),
            ("🔧 Tweaks", "tweaks"),
            ("🔨 Repair", "repair"),
            ("✨ Features", "features"),
            ("📈 Monitoring", "monitoring"),
            ("⚙️ Settings", "settings"),
        ]
        
        self.nav_buttons = {}
        for idx, (text, module_id) in enumerate(nav_items):
            btn = ctk.CTkButton(
                sidebar_frame,
                text=text,
                command=lambda m=module_id: self.show_module(m),
                anchor="w",
                height=40,
                font=ctk.CTkFont(size=13)
            )
            btn.grid(row=idx, column=0, padx=10, pady=5, sticky="ew")
            self.nav_buttons[module_id] = btn
    
    def create_content_area(self):
        """Create main content area"""
        self.content_frame = ctk.CTkFrame(self, corner_radius=0)
        self.content_frame.grid(row=1, column=1, sticky="nsew", padx=0, pady=0)
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)
    
    def create_status_bar(self):
        """Create status bar at bottom"""
        status_frame = ctk.CTkFrame(self, height=30, corner_radius=0)
        status_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=0, pady=0)
        
        self.status_label = ctk.CTkLabel(
            status_frame,
            text="Ready",
            font=ctk.CTkFont(size=11)
        )
        self.status_label.pack(side="left", padx=10, pady=5)
    
    def show_module(self, module_id: str):
        """Show specific module"""
        # Clear current content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Update button states
        for btn_id, btn in self.nav_buttons.items():
            if btn_id == module_id:
                btn.configure(fg_color=("gray75", "gray25"))
            else:
                btn.configure(fg_color=("gray85", "gray15"))
        
        # Load module
        self.current_module = module_id
        
        if module_id == "dashboard":
            self.show_dashboard()
        elif module_id == "cleaner":
            if "cleaner" not in self.modules:
                self.modules["cleaner"] = CleanerModule(self.content_frame)
            self.modules["cleaner"].show()
        elif module_id == "optimizer":
            if "optimizer" not in self.modules:
                self.modules["optimizer"] = OptimizerModule(self.content_frame)
            self.modules["optimizer"].show()
        elif module_id == "privacy":
            if "privacy" not in self.modules:
                self.modules["privacy"] = PrivacyModule(self.content_frame)
            self.modules["privacy"].show()
        elif module_id == "gaming":
            if "gaming" not in self.modules:
                self.modules["gaming"] = GamingModule(self.content_frame)
            self.modules["gaming"].show()
        elif module_id == "disk":
            if "disk" not in self.modules:
                self.modules["disk"] = DiskManagerModule(self.content_frame)
            self.modules["disk"].show()
        elif module_id == "startup":
            if "startup" not in self.modules:
                self.modules["startup"] = StartupManagerModule(self.content_frame)
            self.modules["startup"].show()
        elif module_id == "apps":
            if "apps" not in self.modules:
                self.modules["apps"] = AppsInstallerModule(self.content_frame)
            self.modules["apps"].show()
        elif module_id == "tweaks":
            if "tweaks" not in self.modules:
                self.modules["tweaks"] = TweaksModule(self.content_frame)
            self.modules["tweaks"].show()
        elif module_id == "repair":
            if "repair" not in self.modules:
                self.modules["repair"] = RepairModule(self.content_frame)
            self.modules["repair"].show()
        elif module_id == "features":
            if "features" not in self.modules:
                self.modules["features"] = FeaturesModule(self.content_frame)
            self.modules["features"].show()
        elif module_id == "monitoring":
            self.show_monitoring_placeholder()
        elif module_id == "settings":
            self.show_settings()
        else:
            self.show_module_placeholder(module_id)
        
        self.update_status(f"Showing {module_id.title()}")
    
    def show_dashboard(self):
        """Show dashboard with overview"""
        dashboard = ctk.CTkFrame(self.content_frame)
        dashboard.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Welcome message
        welcome = ctk.CTkLabel(
            dashboard,
            text="Welcome to OptiWindows! 🚀",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        welcome.pack(pady=20)
        
        info = ctk.CTkLabel(
            dashboard,
            text="Your Ultimate Windows Optimization Suite with 150+ Features",
            font=ctk.CTkFont(size=14)
        )
        info.pack(pady=10)
        
        # Quick actions grid
        quick_frame = ctk.CTkFrame(dashboard)
        quick_frame.pack(fill="both", expand=True, padx=20, pady=20)
        quick_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Quick action cards
        actions = [
            ("🧹 Quick Clean", "Run quick system cleanup", lambda: self.show_module("cleaner")),
            ("⚡ Quick Optimize", "Optimize system performance", lambda: self.show_module("optimizer")),
            ("🛡️ Privacy Check", "Check privacy settings", lambda: self.show_module("privacy")),
            ("🎮 Gaming Boost", "Activate gaming mode", lambda: self.show_module("gaming")),
            ("💾 Disk Analysis", "Analyze disk usage", lambda: self.show_module("disk")),
            ("📦 Install Apps", "Install essential apps", lambda: self.show_module("apps")),
        ]
        
        for idx, (title, desc, cmd) in enumerate(actions):
            card = ctk.CTkFrame(quick_frame)
            card.grid(row=idx // 3, column=idx % 3, padx=10, pady=10, sticky="nsew")
            
            ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
            ctk.CTkLabel(card, text=desc, font=ctk.CTkFont(size=11)).pack(pady=5)
            ctk.CTkButton(card, text="Open", command=cmd, height=35).pack(pady=10)
    
    def load_system_info(self):
        """Load system information"""
        try:
            info = self.system_info.get_summary()
            self.after(0, lambda: self.system_info_label.configure(
                text=f"💻 {info['os']} | 🖥️ {info['cpu']} | 💾 {info['ram']}"
            ))
            
            # Calculate health score
            health = self.system_info.calculate_health_score()
            color = "green" if health >= 80 else "orange" if health >= 60 else "red"
            self.after(0, lambda: self.health_score_label.configure(
                text=f"Health: {health}/100",
                text_color=color
            ))
        except Exception as e:
            logger.error(f"Error loading system info: {e}")
    
    def update_status(self, message: str):
        """Update status bar message"""
        self.status_label.configure(text=message)
        logger.info(f"Status: {message}")
    
    def show_monitoring_placeholder(self):
        """Show monitoring module placeholder (coming soon)"""
        frame = ctk.CTkFrame(self.content_frame)
        frame.pack(fill="both", expand=True, padx=50, pady=50)
        
        ctk.CTkLabel(
            frame,
            text="📊 Monitoring Module",
            font=ctk.CTkFont(size=28, weight="bold")
        ).pack(pady=30)
        
        ctk.CTkLabel(
            frame,
            text="Real-time system monitoring with graphs",
            font=ctk.CTkFont(size=14)
        ).pack(pady=10)
        
        ctk.CTkLabel(
            frame,
            text="⏳ Coming in version 1.1.0",
            font=ctk.CTkFont(size=12),
            text_color="orange"
        ).pack(pady=20)
        
        ctk.CTkButton(
            frame,
            text="← Back to Dashboard",
            command=lambda: self.show_module("dashboard"),
            width=200
        ).pack(pady=10)
    
    def show_settings(self):
        """Show settings module"""
        if "settings" not in self.modules:
            self.modules["settings"] = SettingsModule(self.content_frame)
        self.modules["settings"].get_frame().pack(fill="both", expand=True)
    
    def show_module_placeholder(self, module_id: str):
        """Show generic module placeholder"""
        frame = ctk.CTkFrame(self.content_frame)
        frame.pack(fill="both", expand=True, padx=50, pady=50)
        
        ctk.CTkLabel(
            frame,
            text=f"⚠️ {module_id.title()}",
            font=ctk.CTkFont(size=28, weight="bold")
        ).pack(pady=30)
        
        ctk.CTkLabel(
            frame,
            text="Module not yet implemented",
            font=ctk.CTkFont(size=14),
            text_color="red"
        ).pack(pady=10)
        
        ctk.CTkButton(
            frame,
            text="← Back to Dashboard",
            command=lambda: self.show_module("dashboard"),
            width=200
        ).pack(pady=10)
    
    def check_for_updates(self):
        """Check for updates in background"""
        try:
            if self.updater.check_for_updates():
                self.update_available = True
                self.show_update_notification()
        except Exception as e:
            logger.error(f"Update check failed: {e}")
    
    def show_update_notification(self):
        """Show update notification banner"""
        try:
            update_info = self.updater.get_update_info()
            
            # Create notification banner at top
            notif_frame = ctk.CTkFrame(self, fg_color="#2B5A8C", height=40)
            notif_frame.place(x=0, y=0, relwidth=1.0)
            
            msg = f"🎉 New version {update_info.get('version')} available!"
            ctk.CTkLabel(
                notif_frame,
                text=msg,
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color="white"
            ).pack(side="left", padx=20, pady=8)
            
            ctk.CTkButton(
                notif_frame,
                text="Update Now",
                command=self.start_update,
                width=120,
                height=30,
                fg_color="#4A9EFF"
            ).pack(side="right", padx=10, pady=5)
            
            ctk.CTkButton(
                notif_frame,
                text="Later",
                command=lambda: notif_frame.place_forget(),
                width=80,
                height=30,
                fg_color="transparent",
                border_width=1
            ).pack(side="right", padx=5, pady=5)
            
        except Exception as e:
            logger.error(f"Failed to show update notification: {e}")
    
    def start_update(self):
        """Start the update process"""
        try:
            from tkinter import messagebox
            
            if messagebox.askyesno("Update", 
                f"Update to version {self.updater.latest_version}?\n\n"
                "The application will restart after update."):
                
                # Show progress window
                progress_window = ctk.CTkToplevel(self)
                progress_window.title("Updating...")
                progress_window.geometry("400x150")
                progress_window.transient(self)
                progress_window.grab_set()
                
                status_label = ctk.CTkLabel(
                    progress_window,
                    text="Preparing update...",
                    font=ctk.CTkFont(size=14)
                )
                status_label.pack(pady=20)
                
                progress_bar = ctk.CTkProgressBar(progress_window, width=350)
                progress_bar.pack(pady=20)
                progress_bar.set(0)
                
                def update_progress(message, value):
                    status_label.configure(text=message)
                    progress_bar.set(value / 100)
                    progress_window.update()
                
                # Perform update
                def do_update():
                    try:
                        if self.updater.full_update_process(update_progress):
                            messagebox.showinfo("Success", 
                                "Update installed successfully!\n\n"
                                "Application will restart now.")
                            self.updater.restart_application()
                        else:
                            messagebox.showerror("Error", 
                                "Update failed. Check logs for details.")
                    finally:
                        progress_window.destroy()
                
                threading.Thread(target=do_update, daemon=True).start()
                
        except Exception as e:
            logger.error(f"Update failed: {e}")
            from tkinter import messagebox
            messagebox.showerror("Error", f"Update failed: {e}")
