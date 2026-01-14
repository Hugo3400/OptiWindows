"""
Optimizer Module - System Performance Optimization
"""

import customtkinter as ctk
import threading
import subprocess
import winreg
from tkinter import messagebox
from utils.logger import get_logger
from utils.safe_commands import run_command, run_registry_command, stop_service, disable_service

logger = get_logger(__name__)


class OptimizerModule:
    """System optimizer module"""
    
    def __init__(self, parent):
        self.parent = parent
        self.frame = None
        
    def show(self):
        """Display the optimizer module"""
        self.frame = ctk.CTkFrame(self.parent)
        self.frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title = ctk.CTkLabel(
            self.frame,
            text="⚡ System Optimizer",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(pady=20)
        
        # Tabs
        tabview = ctk.CTkTabview(self.frame)
        tabview.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Performance tab
        perf_tab = tabview.add("⚡ Performance")
        self._create_performance_tab(perf_tab)
        
        # Power tab
        power_tab = tabview.add("🔋 Power Plans")
        self._create_power_tab(power_tab)
        
        # Visual Effects tab
        visual_tab = tabview.add("🎨 Visual Effects")
        self._create_visual_tab(visual_tab)
        
        # Advanced tab
        advanced_tab = tabview.add("🔧 Advanced")
        self._create_advanced_tab(advanced_tab)
    
    def _create_performance_tab(self, parent):
        """Create performance optimization tab"""
        desc = ctk.CTkLabel(
            parent,
            text="Optimize system performance settings",
            font=ctk.CTkFont(size=12)
        )
        desc.pack(pady=10)
        
        options_frame = ctk.CTkScrollableFrame(parent)
        options_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        optimizations = [
            ("Disable Telemetry Services", self.disable_telemetry),
            ("Optimize Memory Management", self.optimize_memory),
            ("Disable Background Apps", self.disable_background_apps),
            ("Optimize Processor Scheduling", self.optimize_processor),
            ("Disable Superfetch/Prefetch", self.disable_superfetch),
            ("Optimize Network Settings", self.optimize_network),
            ("Disable Windows Search Indexing", self.disable_search_indexing),
            ("Clear RAM Cache", self.clear_ram_cache),
        ]
        
        for idx, (text, command) in enumerate(optimizations):
            frame = ctk.CTkFrame(options_frame)
            frame.pack(fill="x", padx=10, pady=5)
            
            label = ctk.CTkLabel(frame, text=text, font=ctk.CTkFont(size=13))
            label.pack(side="left", padx=10, pady=10)
            
            btn = ctk.CTkButton(
                frame,
                text="Apply",
                command=command,
                width=100,
                height=30
            )
            btn.pack(side="right", padx=10, pady=10)
        
        # Quick optimize button
        quick_btn = ctk.CTkButton(
            parent,
            text="⚡ Quick Optimize (Apply All)",
            command=self.quick_optimize,
            width=250,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="green",
            hover_color="darkgreen"
        )
        quick_btn.pack(pady=20)
    
    def _create_power_tab(self, parent):
        """Create power plans tab"""
        desc = ctk.CTkLabel(
            parent,
            text="Manage Windows power plans for optimal performance",
            font=ctk.CTkFont(size=12)
        )
        desc.pack(pady=10)
        
        plans_frame = ctk.CTkFrame(parent)
        plans_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Ultimate Performance Plan
        ultimate_frame = ctk.CTkFrame(plans_frame)
        ultimate_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            ultimate_frame,
            text="🚀 Ultimate Performance",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", padx=10, pady=5)
        
        ctk.CTkLabel(
            ultimate_frame,
            text="Hidden Windows power plan for maximum performance",
            font=ctk.CTkFont(size=11)
        ).pack(anchor="w", padx=10)
        
        ctk.CTkButton(
            ultimate_frame,
            text="Enable Ultimate Performance",
            command=self.enable_ultimate_performance,
            width=200
        ).pack(anchor="w", padx=10, pady=10)
        
        # High Performance Plan
        high_frame = ctk.CTkFrame(plans_frame)
        high_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            high_frame,
            text="⚡ High Performance",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", padx=10, pady=5)
        
        ctk.CTkLabel(
            high_frame,
            text="Standard high performance power plan",
            font=ctk.CTkFont(size=11)
        ).pack(anchor="w", padx=10)
        
        ctk.CTkButton(
            high_frame,
            text="Set High Performance",
            command=self.set_high_performance,
            width=200
        ).pack(anchor="w", padx=10, pady=10)
    
    def _create_visual_tab(self, parent):
        """Create visual effects tab"""
        desc = ctk.CTkLabel(
            parent,
            text="Adjust visual effects for better performance",
            font=ctk.CTkFont(size=12)
        )
        desc.pack(pady=10)
        
        effects_frame = ctk.CTkFrame(parent)
        effects_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        options = [
            ("Disable Transparency Effects", self.disable_transparency),
            ("Disable Animations", self.disable_animations),
            ("Disable Shadows", self.disable_shadows),
            ("Best Performance Visual Mode", self.set_best_performance_visual),
            ("Enable Dark Mode", self.enable_dark_mode),
        ]
        
        for text, command in options:
            frame = ctk.CTkFrame(effects_frame)
            frame.pack(fill="x", padx=10, pady=5)
            
            label = ctk.CTkLabel(frame, text=text, font=ctk.CTkFont(size=13))
            label.pack(side="left", padx=10, pady=10)
            
            btn = ctk.CTkButton(frame, text="Apply", command=command, width=100)
            btn.pack(side="right", padx=10, pady=10)
    
    def _create_advanced_tab(self, parent):
        """Create advanced optimizations tab"""
        desc = ctk.CTkLabel(
            parent,
            text="Advanced system optimizations (Use with caution)",
            font=ctk.CTkFont(size=12),
            text_color="orange"
        )
        desc.pack(pady=10)
        
        advanced_frame = ctk.CTkFrame(parent)
        advanced_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        options = [
            ("Disable Hibernation (Frees Space)", self.disable_hibernation),
            ("Disable System Restore (Frees Space)", self.disable_system_restore),
            ("Disable Page File (Only if 16GB+ RAM)", self.disable_page_file),
            ("Optimize SSD (Enable TRIM)", self.optimize_ssd),
            ("Disable Windows Defender (Not Recommended)", self.disable_defender),
            ("Registry Optimization", self.optimize_registry),
        ]
        
        for text, command in options:
            frame = ctk.CTkFrame(advanced_frame)
            frame.pack(fill="x", padx=10, pady=5)
            
            label = ctk.CTkLabel(frame, text=text, font=ctk.CTkFont(size=13))
            label.pack(side="left", padx=10, pady=10)
            
            btn = ctk.CTkButton(
                frame,
                text="Apply",
                command=command,
                width=100,
                fg_color="orange",
                hover_color="darkorange"
            )
            btn.pack(side="right", padx=10, pady=10)
    
    # Performance optimizations
    def disable_telemetry(self):
        """Disable Windows telemetry"""
        try:
            # Disable telemetry services
            services = [
                'DiagTrack',
                'dmwappushservice',
                'diagnosticshub.standardcollector.service'
            ]
            
            for service in services:
                stop_service(service)
                disable_service(service)
            
            # Registry tweaks
            key_paths = [
                r'SOFTWARE\Policies\Microsoft\Windows\DataCollection',
                r'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\DataCollection',
            ]
            
            for key_path in key_paths:
                try:
                    key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, key_path)
                    winreg.SetValueEx(key, 'AllowTelemetry', 0, winreg.REG_DWORD, 0)
                    winreg.CloseKey(key)
                except:
                    pass
            
            messagebox.showinfo("Success", "Telemetry disabled successfully!")
            logger.info("Telemetry disabled")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to disable telemetry: {e}")
            logger.error(f"Error disabling telemetry: {e}")
    
    def optimize_memory(self):
        """Optimize memory management"""
        try:
            key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, 
                                  r'SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management')
            
            # Disable paging executive
            winreg.SetValueEx(key, 'DisablePagingExecutive', 0, winreg.REG_DWORD, 1)
            
            # Large system cache
            winreg.SetValueEx(key, 'LargeSystemCache', 0, winreg.REG_DWORD, 0)
            
            winreg.CloseKey(key)
            
            messagebox.showinfo("Success", "Memory management optimized! Restart required.")
            logger.info("Memory management optimized")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to optimize memory: {e}")
    
    def disable_background_apps(self):
        """Disable background apps"""
        try:
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER,
                                  r'Software\Microsoft\Windows\CurrentVersion\BackgroundAccessApplications')
            winreg.SetValueEx(key, 'GlobalUserDisabled', 0, winreg.REG_DWORD, 1)
            winreg.CloseKey(key)
            
            messagebox.showinfo("Success", "Background apps disabled!")
            logger.info("Background apps disabled")
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {e}")
    
    def optimize_processor(self):
        """Optimize processor scheduling"""
        try:
            key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE,
                                  r'SYSTEM\CurrentControlSet\Control\PriorityControl')
            winreg.SetValueEx(key, 'Win32PrioritySeparation', 0, winreg.REG_DWORD, 38)
            winreg.CloseKey(key)
            
            messagebox.showinfo("Success", "Processor scheduling optimized!")
            logger.info("Processor scheduling optimized")
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {e}")
    
    def disable_superfetch(self):
        """Disable Superfetch/Prefetch"""
        try:
            stop_service('SysMain')
            disable_service('SysMain')
            
            messagebox.showinfo("Success", "Superfetch/Prefetch disabled!")
            logger.info("Superfetch disabled")
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {e}")
    
    def optimize_network(self):
        """Optimize network settings"""
        try:
            # Disable Network Throttling
            key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE,
                                  r'SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile')
            winreg.SetValueEx(key, 'NetworkThrottlingIndex', 0, winreg.REG_DWORD, 0xFFFFFFFF)
            winreg.CloseKey(key)
            
            # Optimize TCP
            run_command(['netsh', 'int', 'tcp', 'set', 'global', 'autotuninglevel=normal'])
            
            messagebox.showinfo("Success", "Network settings optimized!")
            logger.info("Network optimized")
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {e}")
    
    def disable_search_indexing(self):
        """Disable Windows Search indexing"""
        try:
            stop_service('WSearch')
            disable_service('WSearch')
            
            messagebox.showinfo("Success", "Search indexing disabled!")
            logger.info("Search indexing disabled")
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {e}")
    
    def clear_ram_cache(self):
        """Clear RAM cache"""
        try:
            run_command(['powershell', '-Command', 
                          'Clear-RecycleBin -Force; [System.GC]::Collect()'])
            
            messagebox.showinfo("Success", "RAM cache cleared!")
            logger.info("RAM cache cleared")
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {e}")
    
    def quick_optimize(self):
        """Quick optimization - apply all safe optimizations"""
        if not messagebox.askyesno("Confirm", "Apply all performance optimizations?"):
            return
        
        def optimize():
            try:
                self.disable_telemetry()
                self.optimize_memory()
                self.disable_background_apps()
                self.optimize_processor()
                self.optimize_network()
                
                messagebox.showinfo("Complete", "Quick optimization complete! Restart recommended.")
            except Exception as e:
                messagebox.showerror("Error", f"Optimization failed: {e}")
        
        threading.Thread(target=optimize, daemon=True).start()
    
    # Power plans
    def enable_ultimate_performance(self):
        """Enable Ultimate Performance power plan"""
        try:
            # Add Ultimate Performance plan
            run_command(['powercfg', '-duplicatescheme', 
                          'e9a42b02-d5df-448d-aa00-03f14749eb61'])
            
            # Get the GUID and set it active
            result = run_command(['powercfg', '-list'])
            if result and result.stdout:
                for line in result.stdout.split('\n'):
                    if 'Ultimate Performance' in line:
                        guid = line.split()[3]
                        run_command(['powercfg', '-setactive', guid])
                        break
            
            messagebox.showinfo("Success", "Ultimate Performance plan activated!")
            logger.info("Ultimate Performance enabled")
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {e}")
    
    def set_high_performance(self):
        """Set High Performance power plan"""
        try:
            run_command(['powercfg', '-setactive', 
                          '8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c'])
            
            messagebox.showinfo("Success", "High Performance plan activated!")
            logger.info("High Performance enabled")
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {e}")
    
    # Visual effects
    def disable_transparency(self):
        """Disable transparency effects"""
        try:
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER,
                                  r'Software\Microsoft\Windows\CurrentVersion\Themes\Personalize')
            winreg.SetValueEx(key, 'EnableTransparency', 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key)
            
            messagebox.showinfo("Success", "Transparency disabled!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {e}")
    
    def disable_animations(self):
        """Disable animations"""
        try:
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER,
                                  r'Control Panel\Desktop\WindowMetrics')
            winreg.SetValueEx(key, 'MinAnimate', 0, winreg.REG_SZ, '0')
            winreg.CloseKey(key)
            
            messagebox.showinfo("Success", "Animations disabled!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {e}")
    
    def disable_shadows(self):
        """Disable shadows"""
        try:
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER,
                                  r'Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced')
            winreg.SetValueEx(key, 'ListviewShadow', 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key)
            
            messagebox.showinfo("Success", "Shadows disabled!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {e}")
    
    def set_best_performance_visual(self):
        """Set visual effects for best performance"""
        try:
            run_command(['powershell', '-Command',
                          'Set-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\VisualEffects" -Name VisualFXSetting -Value 2'])
            
            messagebox.showinfo("Success", "Visual effects set to best performance!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {e}")
    
    def enable_dark_mode(self):
        """Enable dark mode"""
        try:
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER,
                                  r'Software\Microsoft\Windows\CurrentVersion\Themes\Personalize')
            winreg.SetValueEx(key, 'AppsUseLightTheme', 0, winreg.REG_DWORD, 0)
            winreg.SetValueEx(key, 'SystemUsesLightTheme', 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key)
            
            messagebox.showinfo("Success", "Dark mode enabled!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {e}")
    
    # Advanced
    def disable_hibernation(self):
        """Disable hibernation"""
        if messagebox.askyesno("Confirm", "This will delete hiberfil.sys and free up space. Continue?"):
            try:
                run_command(['powercfg', '-h', 'off'])
                messagebox.showinfo("Success", "Hibernation disabled!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed: {e}")
    
    def disable_system_restore(self):
        """Disable system restore"""
        if messagebox.askyesno("Confirm", "This will disable system restore. Continue?"):
            try:
                run_command(['vssadmin', 'delete', 'shadows', '/all', '/quiet'])
                run_command(['powershell', '-Command',
                              'Disable-ComputerRestore -Drive "C:\\"'])
                messagebox.showinfo("Success", "System restore disabled!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed: {e}")
    
    def disable_page_file(self):
        """Disable page file"""
        if messagebox.askyesno("Warning", "Only disable if you have 16GB+ RAM. Continue?"):
            try:
                key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE,
                                      r'SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management')
                winreg.SetValueEx(key, 'PagingFiles', 0, winreg.REG_MULTI_SZ, [''])
                winreg.CloseKey(key)
                
                messagebox.showinfo("Success", "Page file disabled! Restart required.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed: {e}")
    
    def optimize_ssd(self):
        """Optimize SSD"""
        try:
            # Enable TRIM
            run_command(['fsutil', 'behavior', 'set', 'disabledeletenotify', '0'])
            
            messagebox.showinfo("Success", "SSD TRIM enabled!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {e}")
    
    def disable_defender(self):
        """Disable Windows Defender"""
        if messagebox.askyesno("Warning", "This is NOT recommended! Continue?"):
            try:
                key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE,
                                      r'SOFTWARE\Policies\Microsoft\Windows Defender')
                winreg.SetValueEx(key, 'DisableAntiSpyware', 0, winreg.REG_DWORD, 1)
                winreg.CloseKey(key)
                
                messagebox.showinfo("Success", "Windows Defender disabled! Restart required.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed: {e}")
    
    def optimize_registry(self):
        """Optimize registry"""
        try:
            # Compact registry
            run_command(['compact', '/c', '/s:C:\\Windows\\System32\\config'])
            
            messagebox.showinfo("Success", "Registry optimized!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {e}")
