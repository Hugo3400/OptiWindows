"""
System Information Collector
"""

import platform
import psutil
from typing import Dict, Any
from utils.logger import get_logger

try:
    import wmi
    WMI_AVAILABLE = True
except ImportError:
    WMI_AVAILABLE = False
    print("Warning: WMI module not available. Install with: pip install wmi")

logger = get_logger(__name__)


class SystemInfo:
    """Collect and provide system information"""
    
    def __init__(self):
        self.wmi = None
        if WMI_AVAILABLE:
            try:
                self.wmi = wmi.WMI()
            except Exception as e:
                logger.warning(f"WMI initialization failed: {e}")
        self.info = self._collect_info()
    
    def _collect_info(self) -> Dict[str, Any]:
        """Collect system information"""
        try:
            # OS Info
            os_info = platform.uname()
            
            # CPU Info
            cpu_name = platform.processor()
            if self.wmi:
                try:
                    cpu_info = self.wmi.Win32_Processor()[0]
                    cpu_name = cpu_info.Name.strip()
                except Exception as e:
                    logger.debug(f"WMI CPU info failed, using fallback: {e}")
            
            # RAM Info
            mem = psutil.virtual_memory()
            
            # Disk Info
            disk = psutil.disk_usage('C:\\')
            
            return {
                'os': f"{os_info.system} {os_info.release}",
                'os_version': os_info.version,
                'os_build': os_info.version,
                'cpu': cpu_name,
                'cpu_cores': psutil.cpu_count(logical=False),
                'cpu_threads': psutil.cpu_count(logical=True),
                'ram_total': mem.total,
                'ram_available': mem.available,
                'ram_percent': mem.percent,
                'disk_total': disk.total,
                'disk_used': disk.used,
                'disk_free': disk.free,
                'disk_percent': disk.percent,
            }
        except Exception as e:
            logger.error(f"Error collecting system info: {e}")
            # Return minimal safe data
            return {
                'os': 'Windows',
                'cpu': 'Unknown CPU',
                'cpu_cores': 1,
                'cpu_threads': 1,
                'ram_total': 0,
                'ram_available': 0,
                'ram_percent': 0,
                'disk_total': 0,
                'disk_used': 0,
                'disk_free': 0,
                'disk_percent': 0,
            }
    
    def get_summary(self) -> Dict[str, str]:
        """Get formatted summary"""
        return {
            'os': self.info.get('os', 'Unknown'),
            'cpu': self.info.get('cpu', 'Unknown')[:40],
            'ram': f"{self.info.get('ram_total', 0) // (1024**3)}GB",
        }
    
    def calculate_health_score(self) -> int:
        """Calculate system health score (0-100)"""
        try:
            score = 100
            
            # RAM usage penalty
            ram_usage = self.info.get('ram_percent', 0)
            if ram_usage > 90:
                score -= 20
            elif ram_usage > 80:
                score -= 10
            elif ram_usage > 70:
                score -= 5
            
            # Disk usage penalty
            disk_usage = self.info.get('disk_percent', 0)
            if disk_usage > 95:
                score -= 20
            elif disk_usage > 90:
                score -= 10
            elif disk_usage > 85:
                score -= 5
            
            # CPU usage penalty (with timeout protection)
            try:
                cpu_usage = psutil.cpu_percent(interval=0.5)
                if cpu_usage > 90:
                    score -= 15
                elif cpu_usage > 80:
                    score -= 10
            except Exception as e:
                logger.debug(f"CPU check failed: {e}")
            
            return max(0, min(100, score))
        except Exception as e:
            logger.error(f"Error calculating health score: {e}")
            return 50  # Return neutral score on error
    
    def get_detailed_info(self) -> Dict[str, Any]:
        """Get all collected information"""
        return self.info.copy()
