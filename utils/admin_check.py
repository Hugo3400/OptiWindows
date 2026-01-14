"""
Admin privileges checker and elevator
"""

import ctypes
import sys
import os


def is_admin() -> bool:
    """Check if script is running with administrator privileges"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def check_admin_privileges() -> bool:
    """Check if script is running with administrator privileges (alias)"""
    return is_admin()


def restart_as_admin():
    """Restart the script with administrator privileges"""
    try:
        if sys.argv[0].endswith('.py'):
            # Running as Python script
            ctypes.windll.shell32.ShellExecuteW(
                None,
                "runas",
                sys.executable,
                ' '.join(sys.argv),
                None,
                1
            )
        else:
            # Running as executable
            ctypes.windll.shell32.ShellExecuteW(
                None,
                "runas",
                sys.argv[0],
                ' '.join(sys.argv[1:]),
                None,
                1
            )
    except Exception as e:
        print(f"Failed to elevate privileges: {e}")
        sys.exit(1)
