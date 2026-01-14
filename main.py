"""
OptiWindows - Ultimate Windows Optimization Suite
Created by: AI Assistant
Version: 1.0.0
Description: Comprehensive Windows optimization tool with 150+ features
"""

import sys
import os
import ctypes
import customtkinter as ctk
from pathlib import Path

# Add modules to path
sys.path.insert(0, str(Path(__file__).parent))

from ui.main_window import MainWindow
from utils.admin_check import check_admin_privileges, restart_as_admin
from utils.logger import setup_logger

# Configuration
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def main():
    """Main entry point for OptiWindows"""
    # Setup logger
    logger = setup_logger()
    logger.info("OptiWindows starting...")
    
    # Check admin privileges
    if not check_admin_privileges():
        logger.warning("Not running as administrator")
        print("\n" + "="*60)
        print("⚠️  Administrator privileges recommended for full functionality")
        print("="*60)
        
        response = input("\nContinue without admin rights? (y/n): ").lower()
        if response != 'y':
            print("\nPlease restart as Administrator (Right-click → Run as administrator)")
            sys.exit(0)
    
    logger.info("Running with administrator privileges")
    
    # Create and run main window
    try:
        app = MainWindow()
        app.mainloop()
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    main()
