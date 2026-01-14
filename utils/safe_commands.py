"""
Safe command execution utilities
Provides secure wrappers for running system commands
"""

import subprocess
from typing import List, Optional, Tuple, Union
from utils.logger import get_logger

logger = get_logger(__name__)


def run_command(
    command: List[str],
    shell: bool = False,
    capture_output: bool = True,
    timeout: int = 60,
    check: bool = False
) -> Optional[subprocess.CompletedProcess]:
    """
    Safely run a system command with protections
    
    Args:
        command: List of command arguments
        shell: Whether to use shell (avoid if possible)
        capture_output: Capture stdout/stderr
        timeout: Command timeout in seconds
        check: Raise exception on non-zero exit
    
    Returns:
        CompletedProcess object or None if blocked/failed
    """
    # Security: Don't allow dangerous commands
    dangerous_commands = [
        'format',
        'del /f /s /q c:\\',
        'rd /s /q c:\\',
        'reg delete hklm',
        'diskpart',
        'bcdedit /delete',
    ]
    
    command_str = ' '.join(command).lower()
    for dangerous in dangerous_commands:
        if dangerous in command_str:
            logger.error(f"BLOCKED dangerous command: {command}")
            return None
    
    # Security: Validate command exists and is in safe locations
    if command and not shell:
        exe = command[0].lower()
        allowed_exes = [
            'powershell', 'cmd', 'powercfg', 'sc', 'schtasks',
            'netsh', 'reg', 'wmic', 'ipconfig', 'sfc', 'dism',
            'chkdsk', 'cleanmgr', 'defrag', 'taskkill', 'tasklist',
            'vssadmin', 'fsutil', 'compact', 'nvidia-settings', 
            'radeonsettings.exe', 'net', 'del', 'ren', 'start'
        ]
        
        # Check if it's an allowed executable
        exe_name = exe.split('\\')[-1].replace('.exe', '')
        if exe_name not in allowed_exes and '\\' not in exe:
            if not any(allowed in exe_name for allowed in allowed_exes):
                logger.warning(f"Potentially unsafe executable: {exe}")
    
    try:
        result = subprocess.run(
            command,
            shell=shell,
            capture_output=capture_output,
            text=True,
            timeout=timeout,
            check=check
        )
        
        if result.returncode != 0:
            logger.warning(f"Command failed (exit {result.returncode}): {' '.join(command)}")
            if result.stderr:
                logger.warning(f"Error output: {result.stderr}")
        
        return result
        
    except subprocess.TimeoutExpired:
        logger.error(f"Command timeout after {timeout}s: {' '.join(command)}")
        return None
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Command error: {e}")
        return None
        
    except Exception as e:
        logger.error(f"Unexpected error running command: {e}")
        return None


def run_powershell(
    script: str,
    timeout: int = 60
) -> Tuple[bool, str, str]:
    """
    Safely run a PowerShell script
    
    Args:
        script: PowerShell script to execute
        timeout: Timeout in seconds
    
    Returns:
        Tuple of (success, stdout, stderr)
    """
    # Security checks for PowerShell
    dangerous_patterns = [
        'remove-item -recurse c:\\',
        'format-volume',
        'clear-disk',
        'remove-partition',
    ]
    
    script_lower = script.lower()
    for dangerous in dangerous_patterns:
        if dangerous in script_lower:
            logger.error(f"BLOCKED dangerous PowerShell script")
            return False, "", "Script blocked for security"
    
    command = [
        'powershell',
        '-NoProfile',
        '-NonInteractive',
        '-ExecutionPolicy', 'Bypass',
        '-Command', script
    ]
    
    return run_command(command, timeout=timeout)


def run_registry_command(
    operation: str,
    key: str,
    value_name: Optional[str] = None,
    value_data: Optional[str] = None,
    value_type: str = "REG_DWORD"
) -> bool:
    """
    Safely run a registry command
    
    Args:
        operation: 'add', 'delete', or 'query'
        key: Registry key path
        value_name: Name of the value
        value_data: Data to set
        value_type: Type of registry value
    
    Returns:
        True if successful
    """
    # Security: Don't allow critical system keys to be deleted
    critical_keys = [
        'HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager',
        'HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip',
        'HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Winlogon',
    ]
    
    key_lower = key.lower()
    if operation == 'delete':
        for critical in critical_keys:
            if critical.lower() in key_lower:
                logger.error(f"BLOCKED deletion of critical registry key: {key}")
                return False
    
    # Build command
    command = ['reg', operation, key]
    
    if operation == 'add':
        if value_name:
            command.extend(['/v', value_name])
        if value_data:
            command.extend(['/d', value_data])
        command.extend(['/t', value_type, '/f'])
    elif operation == 'delete':
        if value_name:
            command.extend(['/v', value_name])
        command.append('/f')
    
    success, _, _ = run_command(command)
    return success


def is_service_running(service_name: str) -> bool:
    """Check if a Windows service is running"""
    try:
        success, stdout, _ = run_command(
            ['sc', 'query', service_name],
            timeout=10
        )
        return success and 'RUNNING' in stdout
    except:
        return False


def stop_service(service_name: str) -> bool:
    """Safely stop a Windows service"""
    # Don't allow stopping critical services
    critical_services = [
        'wuauserv',  # Windows Update (let user control this)
        'BITS',      # Background Intelligent Transfer
        'CryptSvc',  # Cryptographic Services
        'TrustedInstaller',  # Windows Modules Installer
        'Winmgmt',   # Windows Management Instrumentation
    ]
    
    if service_name in critical_services:
        logger.warning(f"Refusing to stop critical service: {service_name}")
        return False
    
    success, _, _ = run_command(['sc', 'stop', service_name])
    return success


def disable_service(service_name: str) -> bool:
    """Safely disable a Windows service"""
    # Same critical services protection
    critical_services = [
        'BITS', 'CryptSvc', 'TrustedInstaller', 'Winmgmt'
    ]
    
    if service_name in critical_services:
        logger.warning(f"Refusing to disable critical service: {service_name}")
        return False
    
    success, _, _ = run_command(
        ['sc', 'config', service_name, 'start=disabled']
    )
    return success


def start_service(service_name: str) -> bool:
    """Safely start a Windows service"""
    success, _, _ = run_command(['sc', 'start', service_name])
    return success
