"""
Auto-Update Module - Automatic GitHub Updates
Checks for new releases and updates the application automatically
"""

import requests
import json
import os
import sys
import shutil
import zipfile
import subprocess
from pathlib import Path
from packaging import version
from utils.logger import get_logger

logger = get_logger(__name__)

# Configuration
GITHUB_REPO = "Hugo3400/OptiWindows"
GITHUB_API = f"https://api.github.com/repos/{GITHUB_REPO}"


def get_current_version() -> str:
    """Read current version from VERSION file"""
    try:
        version_file = Path(__file__).parent.parent / 'VERSION'
        if version_file.exists():
            with open(version_file, 'r', encoding='utf-8') as f:
                return f.read().strip()
    except Exception as e:
        logger.warning(f"Failed to read VERSION file: {e}")
    return "1.0.0"  # Fallback version


CURRENT_VERSION = get_current_version()


class AutoUpdater:
    """Automatic update manager"""
    
    def __init__(self):
        self.repo = GITHUB_REPO
        self.api_url = GITHUB_API
        self.current_version = get_current_version()
        self.update_available = False
        self.latest_version = None
        self.download_url = None
        
    def check_for_updates(self) -> bool:
        """
        Check if updates are available on GitHub
        
        Returns:
            bool: True if update available, False otherwise
        """
        try:
            logger.info("Checking for updates...")
            
            # Get latest release from GitHub API
            response = requests.get(
                f"{self.api_url}/releases/latest",
                timeout=10
            )
            
            if response.status_code != 200:
                logger.warning(f"Failed to check updates: HTTP {response.status_code}")
                return False
            
            release_data = response.json()
            
            # Extract version info
            latest_tag = release_data.get('tag_name', '')
            self.latest_version = latest_tag.lstrip('v')
            
            # Compare versions
            if version.parse(self.latest_version) > version.parse(self.current_version):
                self.update_available = True
                self.download_url = release_data.get('zipball_url')
                
                logger.info(f"Update available: {self.current_version} -> {self.latest_version}")
                return True
            else:
                logger.info(f"Application is up to date ({self.current_version})")
                return False
                
        except Exception as e:
            logger.error(f"Failed to check for updates: {e}")
            return False
    
    def get_update_info(self) -> dict:
        """
        Get detailed information about the latest release
        
        Returns:
            dict: Release information
        """
        try:
            response = requests.get(
                f"{self.api_url}/releases/latest",
                timeout=10
            )
            
            if response.status_code == 200:
                release_data = response.json()
                return {
                    'version': release_data.get('tag_name', '').lstrip('v'),
                    'name': release_data.get('name', ''),
                    'description': release_data.get('body', ''),
                    'published_at': release_data.get('published_at', ''),
                    'html_url': release_data.get('html_url', ''),
                    'download_url': release_data.get('zipball_url', '')
                }
            
            return {}
            
        except Exception as e:
            logger.error(f"Failed to get update info: {e}")
            return {}
    
    def download_update(self, progress_callback=None) -> bool:
        """
        Download the latest update
        
        Args:
            progress_callback: Optional callback function for progress updates
            
        Returns:
            bool: True if download successful
        """
        try:
            if not self.download_url:
                logger.error("No download URL available")
                return False
            
            logger.info(f"Downloading update from {self.download_url}")
            
            # Create temp directory
            temp_dir = Path('temp_update')
            temp_dir.mkdir(exist_ok=True)
            
            # Download file
            response = requests.get(self.download_url, stream=True, timeout=30)
            total_size = int(response.headers.get('content-length', 0))
            
            zip_path = temp_dir / 'update.zip'
            downloaded = 0
            
            with open(zip_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        if progress_callback and total_size > 0:
                            progress = (downloaded / total_size) * 100
                            progress_callback(progress)
            
            logger.info("Update downloaded successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to download update: {e}")
            return False
    
    def apply_update(self) -> bool:
        """
        Apply the downloaded update
        
        Returns:
            bool: True if update applied successfully
        """
        try:
            temp_dir = Path('temp_update')
            zip_path = temp_dir / 'update.zip'
            
            if not zip_path.exists():
                logger.error("Update file not found")
                return False
            
            logger.info("Applying update...")
            
            # Extract update
            extract_dir = temp_dir / 'extracted'
            extract_dir.mkdir(exist_ok=True)
            
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
            
            # Find the extracted folder (GitHub adds repo name prefix)
            extracted_folders = list(extract_dir.glob('Hugo3400-OptiWindows-*'))
            if not extracted_folders:
                logger.error("Extracted folder not found")
                return False
            
            source_dir = extracted_folders[0]
            
            # Backup current installation
            backup_dir = Path('backup_before_update')
            if backup_dir.exists():
                shutil.rmtree(backup_dir)
            
            # Files to backup
            important_files = ['config/', 'logs/', 'backups/']
            backup_dir.mkdir(exist_ok=True)
            
            for item in important_files:
                src = Path(item)
                if src.exists():
                    dst = backup_dir / item
                    if src.is_dir():
                        shutil.copytree(src, dst, dirs_exist_ok=True)
                    else:
                        shutil.copy2(src, dst)
            
            # Copy new files (exclude config, logs, backups)
            exclude_dirs = {'config', 'logs', 'backups', 'temp_update', 'backup_before_update', '.git', '__pycache__'}
            
            for item in source_dir.rglob('*'):
                if item.is_file():
                    rel_path = item.relative_to(source_dir)
                    
                    # Skip excluded directories
                    if any(part in exclude_dirs for part in rel_path.parts):
                        continue
                    
                    dest_path = Path(rel_path)
                    dest_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    shutil.copy2(item, dest_path)
                    logger.debug(f"Updated: {rel_path}")
            
            # Restore important files
            for item in important_files:
                src = backup_dir / item
                dst = Path(item)
                if src.exists() and src.is_dir():
                    dst.mkdir(exist_ok=True)
                    for file in src.rglob('*'):
                        if file.is_file():
                            rel = file.relative_to(src)
                            dest_file = dst / rel
                            dest_file.parent.mkdir(parents=True, exist_ok=True)
                            shutil.copy2(file, dest_file)
            
            # Cleanup
            shutil.rmtree(temp_dir)
            
            logger.info("Update applied successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to apply update: {e}")
            return False
    
    def restart_application(self):
        """Restart the application after update"""
        try:
            logger.info("Restarting application...")
            
            # Get current script path
            script = sys.argv[0]
            
            # Restart
            if sys.platform == 'win32':
                subprocess.Popen(['python', script])
            else:
                subprocess.Popen(['python3', script])
            
            # Exit current instance
            sys.exit(0)
            
        except Exception as e:
            logger.error(f"Failed to restart application: {e}")
    
    def full_update_process(self, progress_callback=None) -> bool:
        """
        Perform complete update process: check, download, apply
        
        Args:
            progress_callback: Optional callback for progress updates
            
        Returns:
            bool: True if update successful
        """
        try:
            # Check for updates
            if not self.check_for_updates():
                return False
            
            # Download
            if progress_callback:
                progress_callback("Downloading update...", 0)
            
            if not self.download_update(
                lambda p: progress_callback(f"Downloading... {p:.1f}%", p) if progress_callback else None
            ):
                return False
            
            # Apply
            if progress_callback:
                progress_callback("Applying update...", 90)
            
            if not self.apply_update():
                return False
            
            if progress_callback:
                progress_callback("Update complete!", 100)
            
            return True
            
        except Exception as e:
            logger.error(f"Update process failed: {e}")
            return False


def check_and_notify_update():
    """
    Check for updates and return info (non-blocking)
    
    Returns:
        dict: Update information or None
    """
    try:
        updater = AutoUpdater()
        
        if updater.check_for_updates():
            return updater.get_update_info()
        
        return None
        
    except Exception as e:
        logger.error(f"Update check failed: {e}")
        return None
