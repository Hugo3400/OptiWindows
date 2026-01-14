"""
Repair Module - System Repair Tools
"""

import customtkinter as ctk
import threading
from tkinter import messagebox
from utils.logger import get_logger
from utils.safe_commands import run_command

logger = get_logger(__name__)


class RepairModule:
    """System repair tools module"""
    
    def __init__(self, parent):
        self.parent = parent
        self.frame = None
        
    def show(self):
        """Display the repair module"""
        self.frame = ctk.CTkFrame(self.parent)
        self.frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title = ctk.CTkLabel(
            self.frame,
            text="🔨 System Repair Tools",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(pady=20)
        
        desc = ctk.CTkLabel(
            self.frame,
            text="Advanced system repair and diagnostic tools",
            font=ctk.CTkFont(size=12)
        )
        desc.pack(pady=5)
        
        # Scrollable frame for repair options
        options_frame = ctk.CTkScrollableFrame(self.frame)
        options_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # System File Checker
        self._create_repair_card(
            options_frame,
            "🛠️ System File Checker (SFC)",
            "Scan and repair corrupted system files",
            [
                ("Scan Only", self.sfc_scan),
                ("Scan & Repair", self.sfc_scan_now),
            ]
        )
        
        # DISM Tools
        self._create_repair_card(
            options_frame,
            "📦 DISM Repair",
            "Deployment Image Servicing and Management",
            [
                ("Check Health", self.dism_check_health),
                ("Scan Health", self.dism_scan_health),
                ("Restore Health", self.dism_restore_health),
            ]
        )
        
        # Disk Tools
        self._create_repair_card(
            options_frame,
            "💾 Disk Repair",
            "Check and repair disk errors",
            [
                ("Check Disk (C:)", self.chkdsk_c),
                ("Scan Drive Health", self.scan_drive_health),
            ]
        )
        
        # Network Repair
        self._create_repair_card(
            options_frame,
            "🌐 Network Repair",
            "Fix network and internet issues",
            [
                ("Reset TCP/IP", self.reset_tcpip),
                ("Reset Winsock", self.reset_winsock),
                ("Reset Network", self.reset_network_full),
            ]
        )
        
        # Windows Update
        self._create_repair_card(
            options_frame,
            "🔄 Windows Update Repair",
            "Fix Windows Update issues",
            [
                ("Reset Update Components", self.reset_windows_update),
                ("Clear Update Cache", self.clear_update_cache),
            ]
        )
        
        # Registry Repair
        self._create_repair_card(
            options_frame,
            "📋 Registry Tools",
            "Registry maintenance and repair",
            [
                ("Scan Registry", self.scan_registry),
                ("Rebuild Icon Cache", self.rebuild_icon_cache),
            ]
        )
        
    def _create_repair_card(self, parent, title, description, buttons):
        """Create a repair tool card"""
        card = ctk.CTkFrame(parent)
        card.pack(fill="x", padx=10, pady=10)
        
        # Title
        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.pack(anchor="w", padx=15, pady=(15, 5))
        
        # Description
        desc_label = ctk.CTkLabel(
            card,
            text=description,
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        desc_label.pack(anchor="w", padx=15, pady=(0, 10))
        
        # Buttons
        button_frame = ctk.CTkFrame(card, fg_color="transparent")
        button_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        for text, command in buttons:
            btn = ctk.CTkButton(
                button_frame,
                text=text,
                command=lambda cmd=command: threading.Thread(target=cmd, daemon=True).start(),
                width=150,
                height=35
            )
            btn.pack(side="left", padx=5)
    
    # SFC Tools
    def sfc_scan(self):
        """Run SFC scan only"""
        try:
            messagebox.showinfo("SFC Scan", 
                "Running System File Checker...\nThis may take 10-30 minutes.\n\n"
                "Check logs folder for results.")
            
            result = run_command(
                ['sfc', '/verifyonly'],
                timeout=1800  # 30 minutes
            )
            
            if result and result.returncode == 0:
                messagebox.showinfo("Success", "SFC scan completed!\n\nCheck logs for details.")
            else:
                messagebox.showwarning("Warning", "SFC scan completed with warnings.\n\nCheck logs for details.")
                
            logger.info("SFC scan completed")
        except Exception as e:
            messagebox.showerror("Error", f"SFC scan failed: {e}")
            logger.error(f"SFC scan error: {e}")
    
    def sfc_scan_now(self):
        """Run SFC scan and repair"""
        if messagebox.askyesno("Confirm", 
            "This will scan and repair system files.\n"
            "This may take 10-30 minutes.\n\nContinue?"):
            try:
                messagebox.showinfo("SFC Repair", 
                    "Running System File Checker with repair...\n"
                    "This may take 10-30 minutes.\n\n"
                    "DO NOT close this window or restart your PC!")
                
                result = run_command(
                    ['sfc', '/scannow'],
                    timeout=1800  # 30 minutes
                )
                
                if result and result.returncode == 0:
                    messagebox.showinfo("Success", 
                        "SFC scan and repair completed!\n\n"
                        "Restart may be required for changes to take effect.")
                else:
                    messagebox.showwarning("Warning", 
                        "SFC completed with warnings.\n\n"
                        "Check CBS.log for details:\n"
                        "C:\\Windows\\Logs\\CBS\\CBS.log")
                    
                logger.info("SFC scan with repair completed")
            except Exception as e:
                messagebox.showerror("Error", f"SFC repair failed: {e}")
                logger.error(f"SFC repair error: {e}")
    
    # DISM Tools
    def dism_check_health(self):
        """DISM check health (quick)"""
        try:
            messagebox.showinfo("DISM", "Checking image health...")
            
            result = run_command(
                ['DISM', '/Online', '/Cleanup-Image', '/CheckHealth'],
                timeout=300
            )
            
            if result and result.returncode == 0:
                messagebox.showinfo("Success", "Image health check completed!\n\nNo issues detected.")
            else:
                messagebox.showwarning("Warning", "Issues may be present.\n\nRun 'Scan Health' for detailed check.")
                
            logger.info("DISM CheckHealth completed")
        except Exception as e:
            messagebox.showerror("Error", f"DISM check failed: {e}")
            logger.error(f"DISM check error: {e}")
    
    def dism_scan_health(self):
        """DISM scan health (thorough)"""
        try:
            messagebox.showinfo("DISM", 
                "Scanning image health...\n"
                "This may take 10-20 minutes.")
            
            result = run_command(
                ['DISM', '/Online', '/Cleanup-Image', '/ScanHealth'],
                timeout=1200  # 20 minutes
            )
            
            if result and result.returncode == 0:
                messagebox.showinfo("Success", 
                    "Image scan completed!\n\n"
                    "If issues found, run 'Restore Health'.")
            else:
                messagebox.showwarning("Warning", 
                    "Issues detected!\n\n"
                    "Run 'Restore Health' to fix.")
                
            logger.info("DISM ScanHealth completed")
        except Exception as e:
            messagebox.showerror("Error", f"DISM scan failed: {e}")
            logger.error(f"DISM scan error: {e}")
    
    def dism_restore_health(self):
        """DISM restore health (repair)"""
        if messagebox.askyesno("Confirm", 
            "This will repair the Windows image.\n"
            "This may take 20-40 minutes.\n\n"
            "Requires internet connection.\n\nContinue?"):
            try:
                messagebox.showinfo("DISM", 
                    "Restoring image health...\n"
                    "This may take 20-40 minutes.\n\n"
                    "DO NOT close this window or restart your PC!")
                
                result = run_command(
                    ['DISM', '/Online', '/Cleanup-Image', '/RestoreHealth'],
                    timeout=2400  # 40 minutes
                )
                
                if result and result.returncode == 0:
                    messagebox.showinfo("Success", 
                        "Image restored successfully!\n\n"
                        "Now run SFC /scannow to complete repair.\n"
                        "Restart may be required.")
                else:
                    messagebox.showwarning("Warning", 
                        "Restore completed with warnings.\n\n"
                        "Check DISM.log for details.")
                    
                logger.info("DISM RestoreHealth completed")
            except Exception as e:
                messagebox.showerror("Error", f"DISM restore failed: {e}")
                logger.error(f"DISM restore error: {e}")
    
    # Disk Tools
    def chkdsk_c(self):
        """Schedule chkdsk for next reboot"""
        if messagebox.askyesno("Confirm", 
            "This will schedule a disk check on next reboot.\n\n"
            "The check will run before Windows starts.\n"
            "This may take 30-60 minutes on first boot.\n\nContinue?"):
            try:
                result = run_command(['chkdsk', 'C:', '/F', '/R'])
                
                messagebox.showinfo("Success", 
                    "Disk check scheduled!\n\n"
                    "Restart your PC to run the check.\n"
                    "The check will run before Windows starts.")
                    
                logger.info("CHKDSK scheduled")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to schedule CHKDSK: {e}")
                logger.error(f"CHKDSK error: {e}")
    
    def scan_drive_health(self):
        """Scan drive health with WMIC"""
        try:
            messagebox.showinfo("Scanning", "Checking drive health...")
            
            result = run_command(
                ['wmic', 'diskdrive', 'get', 'status'],
                timeout=30
            )
            
            if result and result.stdout and 'OK' in result.stdout:
                messagebox.showinfo("Success", "Drive health: OK\n\nNo issues detected.")
            else:
                messagebox.showwarning("Warning", 
                    "Drive may have issues.\n\n"
                    "Run full disk check (CHKDSK).")
                
            logger.info("Drive health scan completed")
        except Exception as e:
            messagebox.showerror("Error", f"Drive scan failed: {e}")
            logger.error(f"Drive scan error: {e}")
    
    # Network Repair
    def reset_tcpip(self):
        """Reset TCP/IP stack"""
        try:
            run_command(['netsh', 'int', 'ip', 'reset'])
            messagebox.showinfo("Success", "TCP/IP stack reset!\n\nRestart required.")
            logger.info("TCP/IP reset")
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {e}")
    
    def reset_winsock(self):
        """Reset Winsock"""
        try:
            run_command(['netsh', 'winsock', 'reset'])
            messagebox.showinfo("Success", "Winsock reset!\n\nRestart required.")
            logger.info("Winsock reset")
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {e}")
    
    def reset_network_full(self):
        """Full network reset"""
        if messagebox.askyesno("Confirm", 
            "This will reset all network settings.\n\n"
            "Restart required after completion.\n\nContinue?"):
            try:
                run_command(['netsh', 'winsock', 'reset'])
                run_command(['netsh', 'int', 'ip', 'reset'])
                run_command(['ipconfig', '/flushdns'])
                run_command(['netsh', 'int', 'tcp', 'reset'])
                
                messagebox.showinfo("Success", 
                    "Network fully reset!\n\n"
                    "Restart your PC to apply changes.")
                logger.info("Full network reset")
            except Exception as e:
                messagebox.showerror("Error", f"Failed: {e}")
    
    # Windows Update
    def reset_windows_update(self):
        """Reset Windows Update components"""
        if messagebox.askyesno("Confirm", 
            "This will reset Windows Update components.\n\nContinue?"):
            try:
                messagebox.showinfo("Resetting", "Resetting Windows Update...")
                
                # Stop services
                run_command(['net', 'stop', 'wuauserv'])
                run_command(['net', 'stop', 'cryptSvc'])
                run_command(['net', 'stop', 'bits'])
                run_command(['net', 'stop', 'msiserver'])
                
                # Rename folders
                run_command(['ren', 'C:\\Windows\\SoftwareDistribution', 'SoftwareDistribution.old'])
                run_command(['ren', 'C:\\Windows\\System32\\catroot2', 'catroot2.old'])
                
                # Restart services
                run_command(['net', 'start', 'wuauserv'])
                run_command(['net', 'start', 'cryptSvc'])
                run_command(['net', 'start', 'bits'])
                run_command(['net', 'start', 'msiserver'])
                
                messagebox.showinfo("Success", "Windows Update reset!\n\nTry updating again.")
                logger.info("Windows Update reset")
            except Exception as e:
                messagebox.showerror("Error", f"Failed: {e}")
    
    def clear_update_cache(self):
        """Clear Windows Update cache"""
        try:
            run_command(['net', 'stop', 'wuauserv'])
            run_command(['del', 'C:\\Windows\\SoftwareDistribution\\Download\\*.*', '/s', '/q'])
            run_command(['net', 'start', 'wuauserv'])
            
            messagebox.showinfo("Success", "Update cache cleared!")
            logger.info("Update cache cleared")
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {e}")
    
    # Registry Tools
    def scan_registry(self):
        """Scan registry for issues"""
        messagebox.showinfo("Registry", 
            "Registry scanning requires third-party tools.\n\n"
            "Recommended: CCleaner or similar tools.\n\n"
            "Windows built-in tools don't scan registry issues.")
    
    def rebuild_icon_cache(self):
        """Rebuild icon cache"""
        try:
            messagebox.showinfo("Rebuilding", "Rebuilding icon cache...")
            
            run_command(['taskkill', '/F', '/IM', 'explorer.exe'])
            run_command(['del', '/A', '/Q', '%localappdata%\\IconCache.db'])
            run_command(['start', 'explorer.exe'])
            
            messagebox.showinfo("Success", "Icon cache rebuilt!")
            logger.info("Icon cache rebuilt")
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {e}")
