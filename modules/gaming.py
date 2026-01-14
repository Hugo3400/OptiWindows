"""
Gaming Module - Gaming Performance Optimization
"""

import customtkinter as ctk
import subprocess
import winreg
from tkinter import messagebox
import threading
from utils.logger import get_logger
from utils.safe_commands import run_command, stop_service, start_service

logger = get_logger(__name__)


class GamingModule:
    """Gaming optimization module"""
    
    def __init__(self, parent):
        self.parent = parent
        self.frame = None
        self.gaming_mode_active = False
        
    def show(self):
        """Display the gaming module"""
        self.frame = ctk.CTkFrame(self.parent)
        self.frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title = ctk.CTkLabel(
            self.frame,
            text="🎮 Gaming Mode",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(pady=20)
        
        # Gaming mode status
        self.status_frame = ctk.CTkFrame(self.frame, height=100, fg_color=("gray85", "gray15"))
        self.status_frame.pack(fill="x", padx=20, pady=10)
        
        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="Gaming Mode: INACTIVE",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="red"
        )
        self.status_label.pack(pady=30)
        
        # Toggle button
        self.toggle_btn = ctk.CTkButton(
            self.frame,
            text="🎮 ACTIVATE GAMING MODE",
            command=self.toggle_gaming_mode,
            width=300,
            height=60,
            font=ctk.CTkFont(size=18, weight="bold"),
            fg_color="green",
            hover_color="darkgreen"
        )
        self.toggle_btn.pack(pady=20)
        
        # Tabs
        tabview = ctk.CTkTabview(self.frame)
        tabview.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Optimizations tab
        opt_tab = tabview.add("⚡ Optimizations")
        self._create_optimizations_tab(opt_tab)
        
        # GPU tab
        gpu_tab = tabview.add("🎨 GPU")
        self._create_gpu_tab(gpu_tab)
        
        # Network tab
        net_tab = tabview.add("🌐 Network")
        self._create_network_tab(net_tab)
    
    def _create_optimizations_tab(self, parent):
        """Create gaming optimizations tab"""
        desc = ctk.CTkLabel(
            parent,
            text="Gaming-specific performance optimizations",
            font=ctk.CTkFont(size=12)
        )
        desc.pack(pady=10)
        
        options_frame = ctk.CTkScrollableFrame(parent)
        options_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        optimizations = [
            ("Disable GameDVR/Game Bar", self.disable_game_dvr),
            ("Optimize CPU Priority for Games", self.optimize_cpu_priority),
            ("Disable Fullscreen Optimizations", self.disable_fullscreen_opt),
            ("Enable Hardware Accelerated GPU Scheduling", self.enable_hags),
            ("Disable Nagle's Algorithm (Lower Latency)", self.disable_nagle),
            ("Set High Performance Power Plan", self.set_high_performance),
            ("Disable Windows Game Mode (Paradoxically Better)", self.disable_game_mode),
            ("Optimize Timer Resolution", self.optimize_timer),
        ]
        
        for text, command in optimizations:
            frame = ctk.CTkFrame(options_frame)
            frame.pack(fill="x", padx=5, pady=3)
            
            label = ctk.CTkLabel(frame, text=text, font=ctk.CTkFont(size=13))
            label.pack(side="left", padx=10, pady=8)
            
            btn = ctk.CTkButton(frame, text="Apply", command=command, width=80)
            btn.pack(side="right", padx=10, pady=8)
    
    def _create_gpu_tab(self, parent):
        """Create GPU optimizations tab"""
        desc = ctk.CTkLabel(
            parent,
            text="GPU-specific optimizations",
            font=ctk.CTkFont(size=12)
        )
        desc.pack(pady=10)
        
        options_frame = ctk.CTkFrame(parent)
        options_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # NVIDIA optimizations
        nvidia_frame = ctk.CTkFrame(options_frame)
        nvidia_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(
            nvidia_frame,
            text="🟢 NVIDIA Optimizations",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", padx=10, pady=5)
        
        ctk.CTkButton(
            nvidia_frame,
            text="Optimize NVIDIA Settings",
            command=self.optimize_nvidia,
            width=200
        ).pack(anchor="w", padx=10, pady=10)
        
        # AMD optimizations
        amd_frame = ctk.CTkFrame(options_frame)
        amd_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(
            amd_frame,
            text="🔴 AMD Optimizations",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", padx=10, pady=5)
        
        ctk.CTkButton(
            amd_frame,
            text="Optimize AMD Settings",
            command=self.optimize_amd,
            width=200
        ).pack(anchor="w", padx=10, pady=10)
    
    def _create_network_tab(self, parent):
        """Create network optimizations tab"""
        desc = ctk.CTkLabel(
            parent,
            text="Network optimizations for online gaming",
            font=ctk.CTkFont(size=12)
        )
        desc.pack(pady=10)
        
        options_frame = ctk.CTkScrollableFrame(parent)
        options_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        optimizations = [
            ("Optimize TCP/IP Stack", self.optimize_tcp_ip),
            ("Flush DNS Cache", self.flush_dns),
            ("Reset Winsock", self.reset_winsock),
            ("Disable Network Throttling", self.disable_network_throttling),
            ("Set Best DNS Servers", self.set_gaming_dns),
        ]
        
        for text, command in optimizations:
            frame = ctk.CTkFrame(options_frame)
            frame.pack(fill="x", padx=5, pady=3)
            
            label = ctk.CTkLabel(frame, text=text, font=ctk.CTkFont(size=13))
            label.pack(side="left", padx=10, pady=8)
            
            btn = ctk.CTkButton(frame, text="Apply", command=command, width=80)
            btn.pack(side="right", padx=10, pady=8)
    
    def toggle_gaming_mode(self):
        """Toggle gaming mode on/off"""
        if not self.gaming_mode_active:
            self.activate_gaming_mode()
        else:
            self.deactivate_gaming_mode()
    
    def activate_gaming_mode(self):
        """Activate gaming mode"""
        try:
            # Stop unnecessary services
            services_to_stop = [
                'wuauserv',  # Windows Update
                'BITS',  # Background Intelligent Transfer
                'Spooler',  # Print Spooler
                'WSearch',  # Windows Search
                'SysMain',  # Superfetch
            ]
            
            for service in services_to_stop:
                try:
                    stop_service(service)
                except:
                    pass
            
            # Set high performance power plan
            run_command(['powercfg', '-setactive', 
                          '8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c'])
            
            # Update UI
            self.gaming_mode_active = True
            self.status_label.configure(
                text="Gaming Mode: ACTIVE",
                text_color="green"
            )
            self.toggle_btn.configure(
                text="🛑 DEACTIVATE GAMING MODE",
                fg_color="red",
                hover_color="darkred"
            )
            
            messagebox.showinfo("Success", "Gaming Mode Activated!\n\nNon-essential services stopped.")
            logger.info("Gaming mode activated")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to activate gaming mode: {e}")
            logger.error(f"Gaming mode activation error: {e}")
    
    def deactivate_gaming_mode(self):
        """Deactivate gaming mode"""
        try:
            # Restart services
            services_to_start = ['wuauserv', 'BITS', 'Spooler', 'WSearch']
            
            for service in services_to_start:
                try:
                    start_service(service)
                except:
                    pass
            
            # Update UI
            self.gaming_mode_active = False
            self.status_label.configure(
                text="Gaming Mode: INACTIVE",
                text_color="red"
            )
            self.toggle_btn.configure(
                text="🎮 ACTIVATE GAMING MODE",
                fg_color="green",
                hover_color="darkgreen"
            )
            
            messagebox.showinfo("Success", "Gaming Mode Deactivated!\n\nServices restored.")
            logger.info("Gaming mode deactivated")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to deactivate gaming mode: {e}")
    
    # Gaming optimizations
    def disable_game_dvr(self):
        """Disable GameDVR and Game Bar"""
        try:
            # Disable GameDVR
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER,
                                  r'System\GameConfigStore')
            winreg.SetValueEx(key, 'GameDVR_Enabled', 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key)
            
            # Disable Game Bar
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER,
                                  r'SOFTWARE\Microsoft\Windows\CurrentVersion\GameDVR')
            winreg.SetValueEx(key, 'AppCaptureEnabled', 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key)
            
            messagebox.showinfo("Success", "GameDVR and Game Bar disabled!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {e}")
    
    def optimize_cpu_priority(self):
        """Optimize CPU priority for games"""
        try:
            key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE,
                                  r'SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games')
            winreg.SetValueEx(key, 'GPU Priority', 0, winreg.REG_DWORD, 8)
            winreg.SetValueEx(key, 'Priority', 0, winreg.REG_DWORD, 6)
            winreg.SetValueEx(key, 'Scheduling Category', 0, winreg.REG_SZ, 'High')
            winreg.CloseKey(key)
            
            messagebox.showinfo("Success", "CPU priority optimized for games!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {e}")
    
    def disable_fullscreen_opt(self):
        """Disable fullscreen optimizations"""
        try:
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER,
                                  r'System\GameConfigStore')
            winreg.SetValueEx(key, 'GameDVR_DXGIHonorFSEWindowsCompatible', 0, winreg.REG_DWORD, 1)
            winreg.CloseKey(key)
            
            messagebox.showinfo("Success", "Fullscreen optimizations disabled!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {e}")
    
    def enable_hags(self):
        """Enable Hardware Accelerated GPU Scheduling"""
        try:
            key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE,
                                  r'SYSTEM\CurrentControlSet\Control\GraphicsDrivers')
            winreg.SetValueEx(key, 'HwSchMode', 0, winreg.REG_DWORD, 2)
            winreg.CloseKey(key)
            
            messagebox.showinfo("Success", 
                "Hardware Accelerated GPU Scheduling enabled!\n\nRestart required.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {e}")
    
    def disable_nagle(self):
        """Disable Nagle's algorithm for lower latency"""
        try:
            # Find network interfaces
            result = run_command(['powershell', '-Command',
                'Get-NetAdapter | Select-Object -ExpandProperty InterfaceGuid'])
            
            if result and result.stdout:
                for guid in result.stdout.split():
                    if guid.strip():
                        try:
                            key_path = f'SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters\\Interfaces\\{guid.strip()}'
                            key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, key_path)
                            winreg.SetValueEx(key, 'TcpAckFrequency', 0, winreg.REG_DWORD, 1)
                            winreg.SetValueEx(key, 'TCPNoDelay', 0, winreg.REG_DWORD, 1)
                            winreg.CloseKey(key)
                        except:
                            pass
            
            messagebox.showinfo("Success", "Nagle's algorithm disabled for lower latency!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {e}")
    
    def set_high_performance(self):
        """Set high performance power plan"""
        try:
            run_command(['powercfg', '-setactive',
                          '8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c'])
            
            messagebox.showinfo("Success", "High Performance power plan activated!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {e}")
    
    def disable_game_mode(self):
        """Disable Windows Game Mode"""
        try:
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER,
                                  r'Software\Microsoft\GameBar')
            winreg.SetValueEx(key, 'AutoGameModeEnabled', 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key)
            
            messagebox.showinfo("Success", "Windows Game Mode disabled!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {e}")
    
    def optimize_timer(self):
        """Optimize timer resolution"""
        try:
            key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE,
                                  r'SYSTEM\CurrentControlSet\Control\Session Manager\kernel')
            winreg.SetValueEx(key, 'GlobalTimerResolutionRequests', 0, winreg.REG_DWORD, 1)
            winreg.CloseKey(key)
            
            messagebox.showinfo("Success", "Timer resolution optimized!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {e}")
    
    # GPU optimizations
    def optimize_nvidia(self):
        """Optimize NVIDIA settings"""
        try:
            # Try to open NVIDIA Control Panel
            run_command(['nvidia-settings'])
            
            messagebox.showinfo("NVIDIA", 
                "NVIDIA Control Panel opened.\n\n"
                "Recommended settings:\n"
                "- Power Management: Prefer Maximum Performance\n"
                "- Texture Filtering: High Performance\n"
                "- Threaded Optimization: On\n"
                "- Vertical Sync: Off (use in-game)\n"
                "- Low Latency Mode: Ultra")
        except:
            messagebox.showwarning("NVIDIA", 
                "Could not open NVIDIA Control Panel.\n"
                "Please configure manually through:\n"
                "Right-click Desktop > NVIDIA Control Panel")
    
    def optimize_amd(self):
        """Optimize AMD settings"""
        try:
            # Try to open AMD Software
            run_command(['RadeonSettings.exe'])
            
            messagebox.showinfo("AMD", 
                "AMD Software opened.\n\n"
                "Recommended settings:\n"
                "- Anti-Lag: Enabled\n"
                "- Radeon Boost: Enabled\n"
                "- Image Sharpening: 80%\n"
                "- Wait for Vertical Refresh: Off\n"
                "- Surface Format Optimization: On")
        except:
            messagebox.showwarning("AMD", 
                "Could not open AMD Software.\n"
                "Please configure manually through:\n"
                "Right-click Desktop > AMD Software")
    
    # Network optimizations
    def optimize_tcp_ip(self):
        """Optimize TCP/IP settings"""
        try:
            commands = [
                ['netsh', 'int', 'tcp', 'set', 'global', 'autotuninglevel=normal'],
                ['netsh', 'int', 'tcp', 'set', 'global', 'congestionprovider=ctcp'],
                ['netsh', 'int', 'tcp', 'set', 'global', 'ecncapability=enabled'],
                ['netsh', 'int', 'tcp', 'set', 'global', 'timestamps=disabled'],
            ]
            
            for cmd in commands:
                run_command(cmd)
            
            messagebox.showinfo("Success", "TCP/IP stack optimized!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {e}")
    
    def flush_dns(self):
        """Flush DNS cache"""
        try:
            run_command(['ipconfig', '/flushdns'])
            messagebox.showinfo("Success", "DNS cache flushed!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {e}")
    
    def reset_winsock(self):
        """Reset Winsock"""
        try:
            run_command(['netsh', 'winsock', 'reset'])
            run_command(['netsh', 'int', 'ip', 'reset'])
            
            messagebox.showinfo("Success", "Winsock reset! Restart required.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {e}")
    
    def disable_network_throttling(self):
        """Disable network throttling"""
        try:
            key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE,
                                  r'SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile')
            winreg.SetValueEx(key, 'NetworkThrottlingIndex', 0, winreg.REG_DWORD, 0xFFFFFFFF)
            winreg.CloseKey(key)
            
            messagebox.showinfo("Success", "Network throttling disabled!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {e}")
    
    def set_gaming_dns(self):
        """Set best DNS servers for gaming"""
        try:
            # Cloudflare DNS (known for low latency)
            run_command(['netsh', 'interface', 'ip', 'set', 'dns', 
                          'name="Ethernet"', 'static', '1.1.1.1'])
            run_command(['netsh', 'interface', 'ip', 'add', 'dns',
                          'name="Ethernet"', '1.0.0.1', 'index=2'])
            
            messagebox.showinfo("Success", 
                "DNS servers set to Cloudflare (1.1.1.1)\n"
                "Low latency optimized!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {e}")
