"""
Cleaner Module - System Cleaning Operations
"""

import customtkinter as ctk
import threading
from tkinter import messagebox
from pathlib import Path
import shutil
import subprocess
import winreg
from typing import List, Tuple
from utils.logger import get_logger
from utils.safe_commands import run_command

logger = get_logger(__name__)


class CleanerModule:
    """System cleaner module"""
    
    def __init__(self, parent):
        self.parent = parent
        self.frame = None
        self.cleaning_in_progress = False
        self.total_cleaned = 0
        
    def show(self):
        """Display the cleaner module"""
        self.frame = ctk.CTkFrame(self.parent)
        self.frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title = ctk.CTkLabel(
            self.frame,
            text="🧹 System Cleaner",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(pady=20)
        
        # Description
        desc = ctk.CTkLabel(
            self.frame,
            text="Clean temporary files, cache, and unnecessary data to free up disk space",
            font=ctk.CTkFont(size=12)
        )
        desc.pack(pady=10)
        
        # Content container
        content = ctk.CTkFrame(self.frame)
        content.pack(fill="both", expand=True, padx=20, pady=20)
        content.grid_columnconfigure(0, weight=1)
        
        # Checkboxes for cleaning options
        self.options = {}
        clean_options = [
            ("temp_files", "🗑️ Temporary Files (Windows Temp, User Temp)", True),
            ("windows_cache", "💾 Windows Cache (Prefetch, Font Cache)", True),
            ("browser_cache", "🌐 Browser Cache (Chrome, Firefox, Edge, Opera)", True),
            ("recycle_bin", "🗑️ Empty Recycle Bin", True),
            ("windows_update", "📦 Windows Update Cache", True),
            ("thumbnails", "🖼️ Thumbnail Cache", True),
            ("delivery_opt", "📥 Delivery Optimization Files", True),
            ("log_files", "📝 Old Log Files (*.log)", True),
            ("crash_dumps", "💥 Crash Dumps and Error Reports", False),
            ("windows_old", "📁 Windows.old Folder (Old Windows Installation)", False),
            ("defender_logs", "🛡️ Windows Defender Logs", False),
        ]
        
        for idx, (key, text, default) in enumerate(clean_options):
            var = ctk.BooleanVar(value=default)
            checkbox = ctk.CTkCheckBox(
                content,
                text=text,
                variable=var,
                font=ctk.CTkFont(size=13)
            )
            checkbox.grid(row=idx, column=0, sticky="w", padx=20, pady=5)
            self.options[key] = var
        
        # Progress info
        self.progress_label = ctk.CTkLabel(
            content,
            text="Ready to clean. Select options and click 'Start Cleaning'",
            font=ctk.CTkFont(size=12)
        )
        self.progress_label.grid(row=len(clean_options), column=0, pady=20)
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(content)
        self.progress_bar.grid(row=len(clean_options) + 1, column=0, sticky="ew", padx=20, pady=10)
        self.progress_bar.set(0)
        
        # Buttons
        button_frame = ctk.CTkFrame(content, fg_color="transparent")
        button_frame.grid(row=len(clean_options) + 2, column=0, pady=20)
        
        self.scan_btn = ctk.CTkButton(
            button_frame,
            text="🔍 Scan Only",
            command=self.scan_only,
            width=200,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.scan_btn.pack(side="left", padx=10)
        
        self.clean_btn = ctk.CTkButton(
            button_frame,
            text="🧹 Start Cleaning",
            command=self.start_cleaning,
            width=200,
            height=40,
            font=ctk.CTkFont(size=14),
            fg_color="green",
            hover_color="darkgreen"
        )
        self.clean_btn.pack(side="left", padx=10)
    
    def scan_only(self):
        """Scan for cleanable items without deleting"""
        threading.Thread(target=self._scan_thread, daemon=True).start()
    
    def _scan_thread(self):
        """Scan thread"""
        self.progress_label.configure(text="Scanning...")
        self.progress_bar.set(0)
        
        total_size = 0
        items_found = 0
        
        try:
            # Scan temp files
            if self.options["temp_files"].get():
                temp_paths = [
                    Path(os.environ.get('TEMP', '')),
                    Path('C:\\Windows\\Temp')
                ]
                for path in temp_paths:
                    if path.exists():
                        size, count = self._calculate_folder_size(path)
                        total_size += size
                        items_found += count
            
            # Scan browser cache
            if self.options["browser_cache"].get():
                browser_paths = self._get_browser_cache_paths()
                for path in browser_paths:
                    if path.exists():
                        size, count = self._calculate_folder_size(path)
                        total_size += size
                        items_found += count
            
            # Update result
            size_mb = total_size / (1024 * 1024)
            size_gb = size_mb / 1024
            
            if size_gb >= 1:
                size_str = f"{size_gb:.2f} GB"
            else:
                size_str = f"{size_mb:.2f} MB"
            
            self.progress_label.configure(
                text=f"✅ Scan Complete: {items_found:,} items found ({size_str})"
            )
            self.progress_bar.set(1)
            
        except Exception as e:
            logger.error(f"Scan error: {e}")
            self.progress_label.configure(text=f"❌ Scan error: {str(e)}")
    
    def start_cleaning(self):
        """Start the cleaning process"""
        if self.cleaning_in_progress:
            messagebox.showwarning("Cleaning in Progress", "A cleaning operation is already running.")
            return
        
        # Confirm
        if not messagebox.askyesno(
            "Confirm Cleaning",
            "Are you sure you want to clean the selected items?\nThis action cannot be undone."
        ):
            return
        
        self.cleaning_in_progress = True
        self.clean_btn.configure(state="disabled")
        threading.Thread(target=self._clean_thread, daemon=True).start()
    
    def _clean_thread(self):
        """Cleaning thread"""
        self.total_cleaned = 0
        self.progress_bar.set(0)
        self.progress_label.configure(text="Starting cleaning...")
        
        try:
            total_steps = sum(1 for v in self.options.values() if v.get())
            current_step = 0
            
            # Clean temp files
            if self.options["temp_files"].get():
                self.progress_label.configure(text="Cleaning temporary files...")
                self._clean_temp_files()
                current_step += 1
                self.progress_bar.set(current_step / total_steps)
            
            # Clean Windows cache
            if self.options["windows_cache"].get():
                self.progress_label.configure(text="Cleaning Windows cache...")
                self._clean_windows_cache()
                current_step += 1
                self.progress_bar.set(current_step / total_steps)
            
            # Clean browser cache
            if self.options["browser_cache"].get():
                self.progress_label.configure(text="Cleaning browser cache...")
                self._clean_browser_cache()
                current_step += 1
                self.progress_bar.set(current_step / total_steps)
            
            # Empty recycle bin
            if self.options["recycle_bin"].get():
                self.progress_label.configure(text="Emptying recycle bin...")
                self._empty_recycle_bin()
                current_step += 1
                self.progress_bar.set(current_step / total_steps)
            
            # Clean Windows Update cache
            if self.options["windows_update"].get():
                self.progress_label.configure(text="Cleaning Windows Update cache...")
                self._clean_windows_update()
                current_step += 1
                self.progress_bar.set(current_step / total_steps)
            
            # Clean thumbnails
            if self.options["thumbnails"].get():
                self.progress_label.configure(text="Cleaning thumbnail cache...")
                self._clean_thumbnails()
                current_step += 1
                self.progress_bar.set(current_step / total_steps)
            
            # Delivery Optimization
            if self.options["delivery_opt"].get():
                self.progress_label.configure(text="Cleaning delivery optimization...")
                self._clean_delivery_optimization()
                current_step += 1
                self.progress_bar.set(current_step / total_steps)
            
            # Log files
            if self.options["log_files"].get():
                self.progress_label.configure(text="Cleaning log files...")
                self._clean_log_files()
                current_step += 1
                self.progress_bar.set(current_step / total_steps)
            
            # Crash dumps
            if self.options["crash_dumps"].get():
                self.progress_label.configure(text="Cleaning crash dumps...")
                self._clean_crash_dumps()
                current_step += 1
                self.progress_bar.set(current_step / total_steps)
            
            # Windows.old
            if self.options["windows_old"].get():
                self.progress_label.configure(text="Removing Windows.old...")
                self._remove_windows_old()
                current_step += 1
                self.progress_bar.set(current_step / total_steps)
            
            # Defender logs
            if self.options["defender_logs"].get():
                self.progress_label.configure(text="Cleaning Defender logs...")
                self._clean_defender_logs()
                current_step += 1
                self.progress_bar.set(current_step / total_steps)
            
            # Complete
            self.progress_bar.set(1)
            size_mb = self.total_cleaned / (1024 * 1024)
            size_gb = size_mb / 1024
            
            if size_gb >= 1:
                size_str = f"{size_gb:.2f} GB"
            else:
                size_str = f"{size_mb:.2f} MB"
            
            self.progress_label.configure(
                text=f"✅ Cleaning Complete! {size_str} freed"
            )
            
            messagebox.showinfo(
                "Cleaning Complete",
                f"Successfully cleaned {size_str} of disk space!"
            )
            
        except Exception as e:
            logger.error(f"Cleaning error: {e}")
            self.progress_label.configure(text=f"❌ Error during cleaning: {str(e)}")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        finally:
            self.cleaning_in_progress = False
            self.clean_btn.configure(state="normal")
    
    def _clean_temp_files(self):
        """Clean temporary files"""
        import os
        temp_paths = [
            Path(os.environ.get('TEMP', '')),
            Path('C:\\Windows\\Temp')
        ]
        
        for path in temp_paths:
            if path.exists():
                self.total_cleaned += self._delete_folder_contents(path)
    
    def _clean_windows_cache(self):
        """Clean Windows cache"""
        cache_paths = [
            Path('C:\\Windows\\Prefetch'),
            Path(f"C:\\Users\\{os.getlogin()}\\AppData\\Local\\Microsoft\\Windows\\Explorer"),
        ]
        
        for path in cache_paths:
            if path.exists():
                self.total_cleaned += self._delete_folder_contents(path, pattern="*.db")
    
    def _clean_browser_cache(self):
        """Clean browser cache"""
        browser_paths = self._get_browser_cache_paths()
        for path in browser_paths:
            if path.exists():
                self.total_cleaned += self._delete_folder_contents(path)
    
    def _empty_recycle_bin(self):
        """Empty recycle bin"""
        try:
            import ctypes
            ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, 0)
        except:
            pass
    
    def _clean_windows_update(self):
        """Clean Windows Update cache"""
        update_path = Path('C:\\Windows\\SoftwareDistribution\\Download')
        if update_path.exists():
            self.total_cleaned += self._delete_folder_contents(update_path)
    
    def _clean_thumbnails(self):
        """Clean thumbnail cache"""
        import os
        thumb_path = Path(f"C:\\Users\\{os.getlogin()}\\AppData\\Local\\Microsoft\\Windows\\Explorer")
        if thumb_path.exists():
            self.total_cleaned += self._delete_folder_contents(thumb_path, pattern="thumbcache_*.db")
    
    def _clean_delivery_optimization(self):
        """Clean delivery optimization files"""
        do_path = Path('C:\\Windows\\SoftwareDistribution\\DeliveryOptimization')
        if do_path.exists():
            self.total_cleaned += self._delete_folder_contents(do_path)
    
    def _clean_log_files(self):
        """Clean log files"""
        log_path = Path('C:\\Windows\\Logs')
        if log_path.exists():
            self.total_cleaned += self._delete_folder_contents(log_path, pattern="*.log")
    
    def _clean_crash_dumps(self):
        """Clean crash dumps"""
        dump_paths = [
            Path('C:\\Windows\\Minidump'),
            Path('C:\\Windows\\MEMORY.DMP'),
        ]
        
        for path in dump_paths:
            if path.exists():
                if path.is_file():
                    try:
                        size = path.stat().st_size
                        path.unlink()
                        self.total_cleaned += size
                    except:
                        pass
                else:
                    self.total_cleaned += self._delete_folder_contents(path)
    
    def _remove_windows_old(self):
        """Remove Windows.old folder"""
        old_path = Path('C:\\Windows.old')
        if old_path.exists():
            try:
                    run_command(['cmd', '/c', 'rd', '/s', '/q', str(old_path)], 
                             timeout=300)
                pass
    
    def _clean_defender_logs(self):
        """Clean Windows Defender logs"""
        defender_path = Path('C:\\ProgramData\\Microsoft\\Windows Defender\\Scans\\History')
        if defender_path.exists():
            self.total_cleaned += self._delete_folder_contents(defender_path)
    
    def _get_browser_cache_paths(self) -> List[Path]:
        """Get browser cache paths"""
        import os
        username = os.getlogin()
        base = f"C:\\Users\\{username}\\AppData"
        
        return [
            # Chrome
            Path(f"{base}\\Local\\Google\\Chrome\\User Data\\Default\\Cache"),
            Path(f"{base}\\Local\\Google\\Chrome\\User Data\\Default\\Code Cache"),
            # Firefox
            Path(f"{base}\\Local\\Mozilla\\Firefox\\Profiles"),
            # Edge
            Path(f"{base}\\Local\\Microsoft\\Edge\\User Data\\Default\\Cache"),
            # Opera
            Path(f"{base}\\Roaming\\Opera Software\\Opera Stable\\Cache"),
        ]
    
    def _calculate_folder_size(self, folder: Path) -> Tuple[int, int]:
        """Calculate folder size and item count"""
        total_size = 0
        item_count = 0
        
        # Protection: Skip critical system folders
        critical_paths = ['system32', 'syswow64', 'program files']
        folder_str = str(folder).lower()
        for critical in critical_paths:
            if critical in folder_str and 'temp' not in folder_str and 'cache' not in folder_str:
                logger.warning(f"Skipping critical folder: {folder}")
                return 0, 0
        
        try:
            for item in folder.rglob('*'):
                if item.is_file():
                    try:
                        total_size += item.stat().st_size
                        item_count += 1
                    except (PermissionError, OSError):
                        # Skip inaccessible files
                        pass
        except Exception as e:
            logger.debug(f"Error scanning {folder}: {e}")
        
        return total_size, item_count
    
    def _delete_folder_contents(self, folder: Path, pattern: str = '*') -> int:
        """Delete folder contents and return total size deleted"""
        total_deleted = 0
        
        # Protection: Don't delete from critical folders
        critical_paths = ['system32', 'syswow64', 'program files', 'windows\\system']
        folder_str = str(folder).lower()
        for critical in critical_paths:
            if critical in folder_str and 'temp' not in folder_str and 'cache' not in folder_str:
                logger.error(f"BLOCKED: Attempted to delete from critical folder: {folder}")
                return 0
        
        if not folder.exists():
            return 0
        
        try:
            for item in folder.glob(pattern):
                try:
                    if item.is_file():
                        # Additional protection for system files
                        if item.suffix.lower() in ['.sys', '.dll', '.exe'] and 'temp' not in str(item).lower():
                            logger.warning(f"Skipping system file: {item}")
                            continue
                        
                        size = item.stat().st_size
                        item.unlink()
                        total_deleted += size
                    elif item.is_dir():
                        size, _ = self._calculate_folder_size(item)
                        shutil.rmtree(item, ignore_errors=True)
                        total_deleted += size
                except PermissionError:
                    logger.debug(f"Permission denied: {item}")
                except Exception as e:
                    logger.debug(f"Could not delete {item}: {e}")
        except Exception as e:
            logger.error(f"Error deleting folder contents: {e}")
        
        return total_deleted
