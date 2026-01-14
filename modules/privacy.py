"""
Privacy Module - Windows Privacy & Telemetry Control
"""

import customtkinter as ctk
import subprocess
import winreg
from tkinter import messagebox
import threading
from utils.logger import get_logger
from utils.safe_commands import run_command, run_registry_command, stop_service, disable_service

logger = get_logger(__name__)


class PrivacyModule:
    """Privacy settings module"""
    
    def __init__(self, parent):
        self.parent = parent
        self.frame = None
        self.privacy_score = 0
        
    def show(self):
        """Display the privacy module"""
        self.frame = ctk.CTkFrame(self.parent)
        self.frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title = ctk.CTkLabel(
            self.frame,
            text="🛡️ Privacy & Security",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(pady=20)
        
        # Privacy score
        self.score_frame = ctk.CTkFrame(self.frame, height=80)
        self.score_frame.pack(fill="x", padx=20, pady=10)
        
        self.score_label = ctk.CTkLabel(
            self.score_frame,
            text="Privacy Score: Calculating...",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.score_label.pack(pady=20)
        
        # Calculate score
        threading.Thread(target=self.calculate_privacy_score, daemon=True).start()
        
        # Tabs
        tabview = ctk.CTkTabview(self.frame)
        tabview.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Telemetry tab
        telemetry_tab = tabview.add("📡 Telemetry")
        self._create_telemetry_tab(telemetry_tab)
        
        # Privacy tab
        privacy_tab = tabview.add("🔒 Privacy")
        self._create_privacy_tab(privacy_tab)
        
        # Bloatware tab
        bloatware_tab = tabview.add("🗑️ Bloatware")
        self._create_bloatware_tab(bloatware_tab)
        
        # Advanced tab
        advanced_tab = tabview.add("⚙️ Advanced")
        self._create_advanced_tab(advanced_tab)
    
    def _create_telemetry_tab(self, parent):
        """Create telemetry settings tab"""
        desc = ctk.CTkLabel(
            parent,
            text="Disable Windows telemetry and data collection",
            font=ctk.CTkFont(size=12)
        )
        desc.pack(pady=10)
        
        options_frame = ctk.CTkScrollableFrame(parent)
        options_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        options = [
            ("Disable All Telemetry", self.disable_telemetry),
            ("Disable Diagnostic Data", self.disable_diagnostic_data),
            ("Disable Activity History", self.disable_activity_history),
            ("Disable Advertising ID", self.disable_advertising_id),
            ("Disable Location Tracking", self.disable_location_tracking),
            ("Disable Feedback", self.disable_feedback),
            ("Disable Suggestions", self.disable_suggestions),
            ("Disable Tailored Experiences", self.disable_tailored_experiences),
        ]
        
        for text, command in options:
            self._create_option_button(options_frame, text, command)
        
        # Apply all button
        apply_all_btn = ctk.CTkButton(
            parent,
            text="🛡️ Disable All Telemetry",
            command=self.disable_all_telemetry,
            width=250,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="green"
        )
        apply_all_btn.pack(pady=20)
    
    def _create_privacy_tab(self, parent):
        """Create privacy settings tab"""
        desc = ctk.CTkLabel(
            parent,
            text="Configure Windows privacy settings",
            font=ctk.CTkFont(size=12)
        )
        desc.pack(pady=10)
        
        options_frame = ctk.CTkScrollableFrame(parent)
        options_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        options = [
            ("Disable Cortana", self.disable_cortana),
            ("Disable Copilot", self.disable_copilot),
            ("Disable Windows Tips", self.disable_windows_tips),
            ("Disable Timeline", self.disable_timeline),
            ("Disable App Diagnostics", self.disable_app_diagnostics),
            ("Disable Camera Access", self.disable_camera_access),
            ("Disable Microphone Access", self.disable_microphone_access),
            ("Disable Microsoft Account Sync", self.disable_account_sync),
            ("Disable OneDrive", self.disable_onedrive),
        ]
        
        for text, command in options:
            self._create_option_button(options_frame, text, command)
    
    def _create_bloatware_tab(self, parent):
        """Create bloatware removal tab"""
        desc = ctk.CTkLabel(
            parent,
            text="Remove pre-installed Windows bloatware",
            font=ctk.CTkFont(size=12)
        )
        desc.pack(pady=10)
        
        warning = ctk.CTkLabel(
            parent,
            text="⚠️ Warning: Some apps may be required for certain features",
            font=ctk.CTkFont(size=11),
            text_color="orange"
        )
        warning.pack(pady=5)
        
        bloatware_frame = ctk.CTkScrollableFrame(parent)
        bloatware_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # List of common bloatware
        self.bloatware_list = [
            "Microsoft.BingWeather",
            "Microsoft.GetHelp",
            "Microsoft.Getstarted",
            "Microsoft.MicrosoftOfficeHub",
            "Microsoft.MicrosoftSolitaireCollection",
            "Microsoft.MixedReality.Portal",
            "Microsoft.People",
            "Microsoft.SkypeApp",
            "Microsoft.WindowsFeedbackHub",
            "Microsoft.Xbox.TCUI",
            "Microsoft.XboxApp",
            "Microsoft.XboxGameOverlay",
            "Microsoft.XboxGamingOverlay",
            "Microsoft.XboxIdentityProvider",
            "Microsoft.XboxSpeechToTextOverlay",
            "Microsoft.YourPhone",
            "Microsoft.ZuneMusic",
            "Microsoft.ZuneVideo",
        ]
        
        self.bloatware_vars = {}
        for app in self.bloatware_list:
            var = ctk.BooleanVar(value=True)
            checkbox = ctk.CTkCheckBox(
                bloatware_frame,
                text=app.replace("Microsoft.", ""),
                variable=var,
                font=ctk.CTkFont(size=12)
            )
            checkbox.pack(anchor="w", padx=10, pady=3)
            self.bloatware_vars[app] = var
        
        # Remove button
        remove_btn = ctk.CTkButton(
            parent,
            text="🗑️ Remove Selected Apps",
            command=self.remove_bloatware,
            width=250,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="red",
            hover_color="darkred"
        )
        remove_btn.pack(pady=20)
    
    def _create_advanced_tab(self, parent):
        """Create advanced privacy settings tab"""
        desc = ctk.CTkLabel(
            parent,
            text="Advanced privacy configurations",
            font=ctk.CTkFont(size=12)
        )
        desc.pack(pady=10)
        
        options_frame = ctk.CTkScrollableFrame(parent)
        options_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        options = [
            ("Block Microsoft Telemetry Domains (HOSTS)", self.block_telemetry_domains),
            ("Disable Windows Update P2P", self.disable_update_p2p),
            ("Disable Customer Experience Program", self.disable_ceip),
            ("Disable Error Reporting", self.disable_error_reporting),
            ("Disable HandwritingData Sharing", self.disable_handwriting_sharing),
            ("Disable App Auto-Install", self.disable_app_autoinstall),
            ("Disable Windows Spotlight", self.disable_spotlight),
        ]
        
        for text, command in options:
            self._create_option_button(options_frame, text, command)
        
        # Paranoia mode
        paranoia_btn = ctk.CTkButton(
            parent,
            text="🔒 PARANOIA MODE (Apply Everything)",
            command=self.paranoia_mode,
            width=300,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="purple",
            hover_color="darkviolet"
        )
        paranoia_btn.pack(pady=20)
    
    def _create_option_button(self, parent, text, command):
        """Create an option button"""
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="x", padx=5, pady=3)
        
        label = ctk.CTkLabel(frame, text=text, font=ctk.CTkFont(size=13))
        label.pack(side="left", padx=10, pady=8)
        
        btn = ctk.CTkButton(frame, text="Apply", command=command, width=80, height=28)
        btn.pack(side="right", padx=10, pady=8)
    
    def calculate_privacy_score(self):
        """Calculate privacy score based on settings"""
        score = 100
        
        try:
            # Check telemetry settings
            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                                    r'SOFTWARE\Policies\Microsoft\Windows\DataCollection')
                value, _ = winreg.QueryValueEx(key, 'AllowTelemetry')
                winreg.CloseKey(key)
                if value != 0:
                    score -= 15
            except:
                score -= 15
            
            # Check Cortana
            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                    r'SOFTWARE\Policies\Microsoft\Windows\Windows Search')
                value, _ = winreg.QueryValueEx(key, 'AllowCortana')
                winreg.CloseKey(key)
                if value != 0:
                    score -= 10
            except:
                score -= 10
            
            # Check advertising ID
            try:
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                    r'Software\Microsoft\Windows\CurrentVersion\AdvertisingInfo')
                value, _ = winreg.QueryValueEx(key, 'Enabled')
                winreg.CloseKey(key)
                if value != 0:
                    score -= 10
            except:
                score -= 10
            
            # Update UI
            color = "green" if score >= 80 else "orange" if score >= 60 else "red"
            self.score_label.configure(
                text=f"Privacy Score: {score}/100",
                text_color=color
            )
            self.privacy_score = score
            
        except Exception as e:
            logger.error(f"Error calculating privacy score: {e}")
            self.score_label.configure(text="Privacy Score: Error")
    
    # Telemetry functions
    def disable_telemetry(self):
        """Disable Windows telemetry"""
        try:
            # Registry settings
            key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE,
                                  r'SOFTWARE\Policies\Microsoft\Windows\DataCollection')
            winreg.SetValueEx(key, 'AllowTelemetry', 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key)
            
            # Disable services
            services = ['DiagTrack', 'dmwappushservice']
            for service in services:
                stop_service(service)
                disable_service(service)
            
            messagebox.showinfo("Success", "Telemetry disabled!")
            self.calculate_privacy_score()
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {e}")
    
    def disable_diagnostic_data(self):
        """Disable diagnostic data collection"""
        try:
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER,
                                  r'Software\Microsoft\Windows\CurrentVersion\Diagnostics\DiagTrack')
            winreg.SetValueEx(key, 'ShowedToastAtLevel', 0, winreg.REG_DWORD, 1)
            winreg.CloseKey(key)
            
            messagebox.showinfo("Success", "Diagnostic data disabled!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {e}")
    
    def disable_activity_history(self):
        """Disable activity history"""
        try:
            key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE,
                                  r'SOFTWARE\Policies\Microsoft\Windows\System')
            winreg.SetValueEx(key, 'EnableActivityFeed', 0, winreg.REG_DWORD, 0)
            winreg.SetValueEx(key, 'PublishUserActivities', 0, winreg.REG_DWORD, 0)
            winreg.SetValueEx(key, 'UploadUserActivities', 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key)
            
            messagebox.showinfo("Success", "Activity history disabled!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {e}")
    
    def disable_advertising_id(self):
        """Disable advertising ID"""
        try:
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER,
                                  r'Software\Microsoft\Windows\CurrentVersion\AdvertisingInfo')
            winreg.SetValueEx(key, 'Enabled', 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key)
            
            messagebox.showinfo("Success", "Advertising ID disabled!")
            self.calculate_privacy_score()
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {e}")
    
    def disable_location_tracking(self):
        """Disable location tracking"""
        try:
            key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE,
                                  r'SOFTWARE\Policies\Microsoft\Windows\LocationAndSensors')
            winreg.SetValueEx(key, 'DisableLocation', 0, winreg.REG_DWORD, 1)
            winreg.CloseKey(key)
            
            messagebox.showinfo("Success", "Location tracking disabled!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {e}")
    
    def disable_feedback(self):
        """Disable Windows feedback"""
        try:
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER,
                                  r'Software\Microsoft\Siuf\Rules')
            winreg.SetValueEx(key, 'NumberOfSIUFInPeriod', 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key)
            
            # Disable scheduled task
            run_command(['schtasks', '/Change', '/TN', 
                          r'Microsoft\Windows\Feedback\Siuf\DmClient', '/Disable'])
            
            messagebox.showinfo("Success", "Feedback disabled!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {e}")
    
    def disable_suggestions(self):
        """Disable Windows suggestions"""
        try:
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER,
                                  r'Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager')
            winreg.SetValueEx(key, 'SystemPaneSuggestionsEnabled', 0, winreg.REG_DWORD, 0)
            winreg.SetValueEx(key, 'SoftLandingEnabled', 0, winreg.REG_DWORD, 0)
            winreg.SetValueEx(key, 'SubscribedContent-338388Enabled', 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key)
            
            messagebox.showinfo("Success", "Suggestions disabled!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {e}")
    
    def disable_tailored_experiences(self):
        """Disable tailored experiences"""
        try:
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER,
                                  r'Software\Microsoft\Windows\CurrentVersion\Privacy')
            winreg.SetValueEx(key, 'TailoredExperiencesWithDiagnosticDataEnabled', 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key)
            
            messagebox.showinfo("Success", "Tailored experiences disabled!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {e}")
    
    def disable_all_telemetry(self):
        """Disable all telemetry options"""
        if not messagebox.askyesno("Confirm", "Disable all telemetry settings?"):
            return
        
        def apply_all():
            self.disable_telemetry()
            self.disable_diagnostic_data()
            self.disable_activity_history()
            self.disable_advertising_id()
            self.disable_location_tracking()
            self.disable_feedback()
            self.disable_suggestions()
            self.disable_tailored_experiences()
            messagebox.showinfo("Complete", "All telemetry disabled!")
        
        threading.Thread(target=apply_all, daemon=True).start()
    
    # Privacy functions
    def disable_cortana(self):
        """Disable Cortana"""
        try:
            key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE,
                                  r'SOFTWARE\Policies\Microsoft\Windows\Windows Search')
            winreg.SetValueEx(key, 'AllowCortana', 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key)
            
            messagebox.showinfo("Success", "Cortana disabled!")
            self.calculate_privacy_score()
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {e}")
    
    def disable_copilot(self):
        """Disable Windows Copilot"""
        try:
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER,
                                  r'Software\Policies\Microsoft\Windows\WindowsCopilot')
            winreg.SetValueEx(key, 'TurnOffWindowsCopilot', 0, winreg.REG_DWORD, 1)
            winreg.CloseKey(key)
            
            messagebox.showinfo("Success", "Copilot disabled!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {e}")
    
    def disable_windows_tips(self):
        """Disable Windows tips"""
        try:
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER,
                                  r'Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager')
            winreg.SetValueEx(key, 'SubscribedContent-338389Enabled', 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key)
            
            messagebox.showinfo("Success", "Windows tips disabled!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {e}")
    
    def disable_timeline(self):
        """Disable Timeline"""
        try:
            key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE,
                                  r'SOFTWARE\Policies\Microsoft\Windows\System')
            winreg.SetValueEx(key, 'EnableActivityFeed', 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key)
            
            messagebox.showinfo("Success", "Timeline disabled!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {e}")
    
    def disable_app_diagnostics(self):
        """Disable app diagnostics"""
        try:
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER,
                                  r'Software\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\appDiagnostics')
            winreg.SetValueEx(key, 'Value', 0, winreg.REG_SZ, 'Deny')
            winreg.CloseKey(key)
            
            messagebox.showinfo("Success", "App diagnostics disabled!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {e}")
    
    def disable_camera_access(self):
        """Disable camera access"""
        try:
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER,
                                  r'Software\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\webcam')
            winreg.SetValueEx(key, 'Value', 0, winreg.REG_SZ, 'Deny')
            winreg.CloseKey(key)
            
            messagebox.showinfo("Success", "Camera access disabled!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {e}")
    
    def disable_microphone_access(self):
        """Disable microphone access"""
        try:
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER,
                                  r'Software\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\microphone')
            winreg.SetValueEx(key, 'Value', 0, winreg.REG_SZ, 'Deny')
            winreg.CloseKey(key)
            
            messagebox.showinfo("Success", "Microphone access disabled!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {e}")
    
    def disable_account_sync(self):
        """Disable Microsoft account sync"""
        try:
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER,
                                  r'Software\Microsoft\Windows\CurrentVersion\SettingSync')
            winreg.SetValueEx(key, 'SyncPolicy', 0, winreg.REG_DWORD, 5)
            winreg.CloseKey(key)
            
            messagebox.showinfo("Success", "Account sync disabled!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {e}")
    
    def disable_onedrive(self):
        """Disable OneDrive"""
        try:
            key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE,
                                  r'SOFTWARE\Policies\Microsoft\Windows\OneDrive')
            winreg.SetValueEx(key, 'DisableFileSyncNGSC', 0, winreg.REG_DWORD, 1)
            winreg.CloseKey(key)
            
            messagebox.showinfo("Success", "OneDrive disabled!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {e}")
    
    # Bloatware removal
    def remove_bloatware(self):
        """Remove selected bloatware"""
        if not messagebox.askyesno("Confirm", "Remove selected apps? This cannot be undone."):
            return
        
        def remove():
            removed = 0
            failed = []
            
            for app, var in self.bloatware_vars.items():
                if var.get():
                    try:
                        result = run_command(
                            ['powershell', '-Command', 
                             f'Get-AppxPackage *{app}* | Remove-AppxPackage'],
                            timeout=30
                        )
                        if result.returncode == 0:
                            removed += 1
                        else:
                            failed.append(app)
                    except:
                        failed.append(app)
            
            if failed:
                messagebox.showinfo("Complete", 
                    f"Removed {removed} apps.\nFailed to remove: {', '.join(failed)}")
            else:
                messagebox.showinfo("Success", f"Successfully removed {removed} apps!")
        
        threading.Thread(target=remove, daemon=True).start()
    
    # Advanced functions
    def block_telemetry_domains(self):
        """Block Microsoft telemetry domains in HOSTS file"""
        try:
            hosts_file = r'C:\Windows\System32\drivers\etc\hosts'
            telemetry_domains = [
                'vortex.data.microsoft.com',
                'vortex-win.data.microsoft.com',
                'telemetry.microsoft.com',
                'telemetry.appex.bing.net',
                'telemetry.urs.microsoft.com',
                'telemetry.appex.bing.net',
                'settings-sandbox.data.microsoft.com',
                'vortex-sandbox.data.microsoft.com',
                'survey.watson.microsoft.com',
                'watson.live.com',
                'watson.microsoft.com',
                'statsfe2.ws.microsoft.com',
                'corpext.msitadfs.glbdns2.microsoft.com',
                'compatexchange.cloudapp.net',
                'cs1.wpc.v0cdn.net',
                'a-0001.a-msedge.net',
                'statsfe2.update.microsoft.com.akadns.net',
                'sls.update.microsoft.com.akadns.net',
                'fe2.update.microsoft.com.akadns.net',
                'diagnostics.support.microsoft.com',
                'corp.sts.microsoft.com',
                'statsfe1.ws.microsoft.com',
                'pre.footprintpredict.com',
                'i1.services.social.microsoft.com',
                'i1.services.social.microsoft.com.nsatc.net',
                'feedback.windows.com',
                'feedback.microsoft-hohm.com',
                'feedback.search.microsoft.com',
            ]
            
            with open(hosts_file, 'a') as f:
                f.write('\n# OptiWindows - Block Microsoft Telemetry\n')
                for domain in telemetry_domains:
                    f.write(f'0.0.0.0 {domain}\n')
            
            # Flush DNS
            run_command(['ipconfig', '/flushdns'])
            
            messagebox.showinfo("Success", "Telemetry domains blocked in HOSTS file!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {e}")
    
    def disable_update_p2p(self):
        """Disable Windows Update P2P"""
        try:
            key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE,
                                  r'SOFTWARE\Microsoft\Windows\CurrentVersion\DeliveryOptimization\Config')
            winreg.SetValueEx(key, 'DODownloadMode', 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key)
            
            messagebox.showinfo("Success", "Windows Update P2P disabled!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {e}")
    
    def disable_ceip(self):
        """Disable Customer Experience Improvement Program"""
        try:
            key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE,
                                  r'SOFTWARE\Policies\Microsoft\SQMClient\Windows')
            winreg.SetValueEx(key, 'CEIPEnable', 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key)
            
            messagebox.showinfo("Success", "CEIP disabled!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {e}")
    
    def disable_error_reporting(self):
        """Disable Windows Error Reporting"""
        try:
            key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE,
                                  r'SOFTWARE\Microsoft\Windows\Windows Error Reporting')
            winreg.SetValueEx(key, 'Disabled', 0, winreg.REG_DWORD, 1)
            winreg.CloseKey(key)
            
            disable_service('WerSvc')
            
            messagebox.showinfo("Success", "Error reporting disabled!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {e}")
    
    def disable_handwriting_sharing(self):
        """Disable handwriting data sharing"""
        try:
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER,
                                  r'Software\Microsoft\InputPersonalization')
            winreg.SetValueEx(key, 'RestrictImplicitInkCollection', 0, winreg.REG_DWORD, 1)
            winreg.SetValueEx(key, 'RestrictImplicitTextCollection', 0, winreg.REG_DWORD, 1)
            winreg.CloseKey(key)
            
            messagebox.showinfo("Success", "Handwriting data sharing disabled!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {e}")
    
    def disable_app_autoinstall(self):
        """Disable automatic app installation"""
        try:
            key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE,
                                  r'SOFTWARE\Policies\Microsoft\Windows\CloudContent')
            winreg.SetValueEx(key, 'DisableWindowsConsumerFeatures', 0, winreg.REG_DWORD, 1)
            winreg.CloseKey(key)
            
            messagebox.showinfo("Success", "App auto-install disabled!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {e}")
    
    def disable_spotlight(self):
        """Disable Windows Spotlight"""
        try:
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER,
                                  r'Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager')
            winreg.SetValueEx(key, 'RotatingLockScreenEnabled', 0, winreg.REG_DWORD, 0)
            winreg.SetValueEx(key, 'RotatingLockScreenOverlayEnabled', 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key)
            
            messagebox.showinfo("Success", "Windows Spotlight disabled!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {e}")
    
    def paranoia_mode(self):
        """Apply maximum privacy settings"""
        if not messagebox.askyesno("PARANOIA MODE", 
            "This will apply MAXIMUM privacy settings.\n\nSome Windows features may stop working.\n\nContinue?"):
            return
        
        def apply_paranoia():
            # Apply all telemetry settings
            self.disable_all_telemetry()
            
            # Apply all privacy settings
            self.disable_cortana()
            self.disable_copilot()
            self.disable_windows_tips()
            self.disable_timeline()
            self.disable_app_diagnostics()
            self.disable_camera_access()
            self.disable_microphone_access()
            self.disable_account_sync()
            self.disable_onedrive()
            
            # Apply all advanced settings
            self.block_telemetry_domains()
            self.disable_update_p2p()
            self.disable_ceip()
            self.disable_error_reporting()
            self.disable_handwriting_sharing()
            self.disable_app_autoinstall()
            self.disable_spotlight()
            
            messagebox.showinfo("Complete", 
                "PARANOIA MODE ACTIVATED!\n\nMaximum privacy settings applied.\nRestart recommended.")
            self.calculate_privacy_score()
        
        threading.Thread(target=apply_paranoia, daemon=True).start()
