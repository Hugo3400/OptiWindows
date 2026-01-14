"""
Script de diagnostic système pour OptiWindows
Affiche des informations détaillées sur le système
"""

import sys
import platform
import os
from pathlib import Path

# Ajouter le répertoire parent au path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from utils.system_info import SystemInfo
    from utils.admin_check import is_admin
    import psutil
except ImportError as e:
    print(f"Erreur d'import: {e}")
    print("Installez les dépendances: pip install -r requirements.txt")
    sys.exit(1)


def print_section(title):
    """Affiche un titre de section"""
    print()
    print("=" * 70)
    print(f" {title}")
    print("=" * 70)


def format_bytes(bytes_value):
    """Formate une valeur en octets en unité lisible"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024.0


def main():
    print()
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "OptiWindows - Diagnostic Système" + " " * 21 + "║")
    print("╚" + "═" * 68 + "╝")
    
    # Informations Python
    print_section("Python & Environnement")
    print(f"  Version Python    : {platform.python_version()}")
    print(f"  Architecture      : {platform.architecture()[0]}")
    print(f"  Compilateur       : {platform.python_compiler()}")
    print(f"  Répertoire        : {sys.executable}")
    
    # Informations Windows
    print_section("Système d'exploitation")
    print(f"  OS                : {platform.system()}")
    print(f"  Version           : {platform.version()}")
    print(f"  Release           : {platform.release()}")
    print(f"  Machine           : {platform.machine()}")
    print(f"  Processeur        : {platform.processor()}")
    print(f"  Droits Admin      : {'✓ OUI' if is_admin() else '✗ NON (requis!)'}")
    
    # Informations CPU
    print_section("Processeur")
    sysinfo = SystemInfo()
    print(f"  Cœurs physiques   : {psutil.cpu_count(logical=False)}")
    print(f"  Cœurs logiques    : {psutil.cpu_count(logical=True)}")
    print(f"  Utilisation       : {sysinfo.get_cpu_usage():.1f}%")
    
    try:
        freq = psutil.cpu_freq()
        print(f"  Fréquence actuelle: {freq.current:.0f} MHz")
        print(f"  Fréquence max     : {freq.max:.0f} MHz")
    except:
        pass
    
    # Informations Mémoire
    print_section("Mémoire RAM")
    mem = sysinfo.get_memory_info()
    print(f"  Total             : {format_bytes(mem['total'])}")
    print(f"  Utilisée          : {format_bytes(mem['used'])} ({mem['percent']:.1f}%)")
    print(f"  Disponible        : {format_bytes(mem['available'])}")
    
    # Informations Disque
    print_section("Disques")
    partitions = psutil.disk_partitions()
    for partition in partitions:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            print(f"\n  {partition.device}")
            print(f"    Type            : {partition.fstype}")
            print(f"    Point de montage: {partition.mountpoint}")
            print(f"    Total           : {format_bytes(usage.total)}")
            print(f"    Utilisé         : {format_bytes(usage.used)} ({usage.percent}%)")
            print(f"    Libre           : {format_bytes(usage.free)}")
        except PermissionError:
            print(f"  {partition.device}: [Accès refusé]")
    
    # Informations Réseau
    print_section("Réseau")
    try:
        net_io = psutil.net_io_counters()
        print(f"  Octets envoyés    : {format_bytes(net_io.bytes_sent)}")
        print(f"  Octets reçus      : {format_bytes(net_io.bytes_recv)}")
        print(f"  Paquets envoyés   : {net_io.packets_sent:,}")
        print(f"  Paquets reçus     : {net_io.packets_recv:,}")
    except:
        print("  [Informations réseau non disponibles]")
    
    # Dépendances installées
    print_section("Dépendances Python")
    try:
        import customtkinter
        print(f"  ✓ CustomTkinter   : {customtkinter.__version__}")
    except:
        print("  ✗ CustomTkinter   : Non installé")
    
    try:
        import psutil
        print(f"  ✓ psutil          : {psutil.__version__}")
    except:
        print("  ✗ psutil          : Non installé")
    
    try:
        import winshell
        print("  ✓ winshell        : Installé")
    except:
        print("  ✗ winshell        : Non installé")
    
    # Processus en cours
    print_section("Processus système")
    processes = []
    for proc in psutil.process_iter(['name', 'cpu_percent', 'memory_percent']):
        try:
            pinfo = proc.info
            if pinfo['cpu_percent'] > 0 or pinfo['memory_percent'] > 0:
                processes.append(pinfo)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    # Trier par utilisation CPU
    processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
    
    print("\n  Top 5 processus (CPU):")
    for i, proc in enumerate(processes[:5], 1):
        print(f"    {i}. {proc['name']:30} CPU: {proc['cpu_percent']:5.1f}%  RAM: {proc['memory_percent']:5.1f}%")
    
    # Conclusion
    print()
    print("=" * 70)
    print()
    
    if not is_admin():
        print("⚠ ATTENTION: OptiWindows nécessite les droits administrateur!")
        print("   Relancez le script avec 'Exécuter en tant qu'administrateur'")
        print()
    else:
        print("✓ Le système est prêt pour OptiWindows")
        print()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrompu par l'utilisateur")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nErreur: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
