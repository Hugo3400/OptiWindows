"""
Logger configuration
"""

import logging
import os
from pathlib import Path
from datetime import datetime


def setup_logger():
    """Setup main application logger"""
    # Create logs directory
    log_dir = Path(__file__).parent.parent / "logs"
    try:
        log_dir.mkdir(exist_ok=True)
    except Exception as e:
        print(f"Warning: Could not create logs directory: {e}")
        log_dir = Path.cwd() / "logs"
        log_dir.mkdir(exist_ok=True)
    
    # Create log file with timestamp
    log_file = log_dir / f"optiwindows_{datetime.now().strftime('%Y%m%d')}.log"
    
    # Configure logger
    logger = logging.getLogger("OptiWindows")
    logger.setLevel(logging.DEBUG)
    
    # File handler
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(file_formatter)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(levelname)s: %(message)s')
    console_handler.setFormatter(console_formatter)
    
    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


def get_logger(name: str):
    """Get a logger instance"""
    return logging.getLogger(f"OptiWindows.{name}")
