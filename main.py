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
        print("⚠️  OptiWindows requires Administrator privileges")
        print("="*60)
        print("\nThe application will now restart with elevated privileges...\n")
        
        try:
            restart_as_admin()
            sys.exit(0)
        except Exception as e:
            logger.error(f"Failed to restart as admin: {e}")
            print(f"\n❌ Error: {e}")
            print("\nPlease manually run as Administrator (Right-click → Run as administrator)")
            input("\nPress Enter to exit...")
            sys.exit(1)
    
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
