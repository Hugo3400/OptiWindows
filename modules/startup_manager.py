"""Startup Manager Module - Placeholder"""
import customtkinter as ctk
from utils.logger import get_logger
logger = get_logger(__name__)

class StartupManagerModule:
    def __init__(self, parent):
        self.parent = parent
        self.frame = None
    
    def show(self):
        self.frame = ctk.CTkFrame(self.parent)
        self.frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title = ctk.CTkLabel(self.frame, text="🚀 Startup Manager",
                            font=ctk.CTkFont(size=24, weight="bold"))
        title.pack(pady=20)
        
        desc = ctk.CTkLabel(self.frame,
                           text="Manage programs that start with Windows",
                           font=ctk.CTkFont(size=14))
        desc.pack(pady=10)
        
        ctk.CTkLabel(self.frame, text="🛠️ Under Development - Coming Soon!",
                    font=ctk.CTkFont(size=16), text_color="orange").pack(pady=30)
        
        ctk.CTkLabel(self.frame, text="Planned Features: Startup Programs, Services, Scheduled Tasks",
                    font=ctk.CTkFont(size=12), text_color="gray").pack(pady=5)
