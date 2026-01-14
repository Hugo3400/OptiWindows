"""
Script de test rapide pour OptiWindows
Vérifie que tous les modules sont correctement importables
"""

import sys
from pathlib import Path

print("=" * 60)
print("OptiWindows - Test d'intégrité des modules")
print("=" * 60)
print()

errors = []
success = []

# Test des imports principaux
modules_to_test = [
    ("utils.admin_check", "Vérification administrateur"),
    ("utils.logger", "Système de logging"),
    ("utils.system_info", "Informations système"),
    ("utils.config_manager", "Gestionnaire de configuration"),
    ("utils.backup_manager", "Gestionnaire de backups"),
    ("modules.cleaner", "Module de nettoyage"),
    ("modules.optimizer", "Module d'optimisation"),
    ("modules.privacy", "Module de confidentialité"),
    ("modules.gaming", "Module gaming"),
    ("modules.disk_manager", "Gestionnaire de disque"),
    ("modules.repair", "Module de réparation"),
    ("modules.startup_manager", "Gestionnaire de démarrage"),
    ("modules.tweaks", "Module de tweaks"),
    ("modules.features", "Module de features"),
    ("modules.apps_installer", "Installateur d'applications"),
    ("ui.main_window", "Interface graphique principale"),
]

print("Test des imports de modules...")
print()

for module_name, description in modules_to_test:
    try:
        __import__(module_name)
        print(f"✓ {description:40} [OK]")
        success.append(module_name)
    except Exception as e:
        print(f"✗ {description:40} [ERREUR]")
        print(f"  → {str(e)}")
        errors.append((module_name, str(e)))

print()
print("=" * 60)

# Test des dépendances externes
print()
print("Test des dépendances externes...")
print()

dependencies = [
    ("customtkinter", "Interface graphique moderne"),
    ("psutil", "Informations système"),
    ("winshell", "Opérations Windows"),
]

for dep_name, description in dependencies:
    try:
        __import__(dep_name)
        print(f"✓ {description:40} [OK]")
        success.append(dep_name)
    except Exception as e:
        print(f"✗ {description:40} [ERREUR]")
        print(f"  → {str(e)}")
        errors.append((dep_name, str(e)))

print()
print("=" * 60)

# Test de la structure des répertoires
print()
print("Vérification de la structure du projet...")
print()

required_dirs = [
    "modules",
    "ui",
    "utils",
    "config",
    "logs",
    "backups",
]

for dir_name in required_dirs:
    dir_path = Path(dir_name)
    if dir_path.exists():
        print(f"✓ Répertoire '{dir_name}':40 [OK]")
    else:
        print(f"✗ Répertoire '{dir_name}':40 [MANQUANT]")
        # Créer le répertoire s'il manque
        try:
            dir_path.mkdir(exist_ok=True)
            print(f"  → Créé automatiquement")
        except:
            errors.append((dir_name, "Impossible de créer le répertoire"))

print()
print("=" * 60)

# Résumé
print()
print("RÉSUMÉ DES TESTS")
print("=" * 60)
print(f"✓ Tests réussis : {len(success)}")
print(f"✗ Erreurs : {len(errors)}")
print()

if errors:
    print("DÉTAILS DES ERREURS:")
    print()
    for module, error in errors:
        print(f"  • {module}")
        print(f"    {error}")
        print()
    
    print("Pour corriger:")
    print("  1. Vérifiez que Python est correctement installé")
    print("  2. Installez les dépendances: pip install -r requirements.txt")
    print("  3. Vérifiez les droits d'accès aux répertoires")
    print()
    sys.exit(1)
else:
    print("✓ Tous les tests sont passés avec succès!")
    print()
    print("OptiWindows est prêt à être utilisé.")
    print("Lancez l'application avec: python main.py")
    print()
    sys.exit(0)
