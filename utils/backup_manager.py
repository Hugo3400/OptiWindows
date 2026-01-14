"""
Gestionnaire de sauvegardes et points de restauration
Crée des backups avant les modifications importantes
"""

import os
import subprocess
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import shutil

class BackupManager:
    def __init__(self, backup_dir: str = "backups"):
        """
        Initialise le gestionnaire de sauvegardes
        
        Args:
            backup_dir: Répertoire pour stocker les backups
        """
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(exist_ok=True)
        self.backup_index_file = self.backup_dir / "index.json"
        self.backups = self.load_backup_index()
    
    def load_backup_index(self) -> List[Dict]:
        """Charge l'index des backups"""
        if self.backup_index_file.exists():
            try:
                with open(self.backup_index_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_backup_index(self):
        """Sauvegarde l'index des backups"""
        try:
            with open(self.backup_index_file, 'w', encoding='utf-8') as f:
                json.dump(self.backups, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Erreur sauvegarde index: {e}")
    
    def create_restore_point(self, description: str = "OptiWindows") -> bool:
        """
        Crée un point de restauration système Windows
        
        Args:
            description: Description du point de restauration
        
        Returns:
            True si succès, False sinon
        """
        try:
            # PowerShell command pour créer un point de restauration
            ps_command = f'''
            Checkpoint-Computer -Description "{description}" -RestorePointType "MODIFY_SETTINGS"
            '''
            
            result = subprocess.run(
                ["powershell", "-Command", ps_command],
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode == 0:
                print(f"✓ Point de restauration créé: {description}")
                
                # Enregistrer dans l'index
                backup_info = {
                    "type": "restore_point",
                    "description": description,
                    "timestamp": datetime.now().isoformat(),
                    "success": True
                }
                self.backups.append(backup_info)
                self.save_backup_index()
                
                return True
            else:
                print(f"✗ Erreur création point de restauration: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("✗ Timeout lors de la création du point de restauration")
            return False
        except Exception as e:
            print(f"✗ Erreur: {e}")
            return False
    
    def create_registry_backup(self, key: str, name: str = None) -> bool:
        """
        Crée un backup d'une clé de registre
        
        Args:
            key: Clé de registre à sauvegarder (ex: HKLM\\SOFTWARE\\...)
            name: Nom du backup (optionnel)
        
        Returns:
            True si succès
        """
        try:
            if name is None:
                name = f"registry_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            backup_file = self.backup_dir / f"{name}.reg"
            
            # Utiliser reg export
            result = subprocess.run(
                ["reg", "export", key, str(backup_file), "/y"],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print(f"✓ Backup registre créé: {backup_file}")
                
                backup_info = {
                    "type": "registry",
                    "name": name,
                    "key": key,
                    "file": str(backup_file),
                    "timestamp": datetime.now().isoformat()
                }
                self.backups.append(backup_info)
                self.save_backup_index()
                
                return True
            else:
                print(f"✗ Erreur backup registre: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"✗ Erreur: {e}")
            return False
    
    def create_file_backup(self, source: str, name: str = None) -> bool:
        """
        Crée un backup d'un fichier
        
        Args:
            source: Chemin du fichier source
            name: Nom du backup (optionnel)
        
        Returns:
            True si succès
        """
        try:
            source_path = Path(source)
            
            if not source_path.exists():
                print(f"✗ Fichier source introuvable: {source}")
                return False
            
            if name is None:
                name = f"{source_path.stem}_{datetime.now().strftime('%Y%m%d_%H%M%S')}{source_path.suffix}"
            
            backup_file = self.backup_dir / name
            
            # Copier le fichier
            shutil.copy2(source_path, backup_file)
            
            print(f"✓ Backup fichier créé: {backup_file}")
            
            backup_info = {
                "type": "file",
                "name": name,
                "source": str(source_path),
                "backup": str(backup_file),
                "timestamp": datetime.now().isoformat(),
                "size": source_path.stat().st_size
            }
            self.backups.append(backup_info)
            self.save_backup_index()
            
            return True
            
        except Exception as e:
            print(f"✗ Erreur backup fichier: {e}")
            return False
    
    def list_backups(self) -> List[Dict]:
        """Liste tous les backups disponibles"""
        return self.backups
    
    def restore_registry_backup(self, backup_name: str) -> bool:
        """
        Restaure un backup de registre
        
        Args:
            backup_name: Nom du backup à restaurer
        
        Returns:
            True si succès
        """
        try:
            # Trouver le backup
            backup = next((b for b in self.backups if b.get('name') == backup_name), None)
            
            if not backup or backup.get('type') != 'registry':
                print(f"✗ Backup registre introuvable: {backup_name}")
                return False
            
            backup_file = backup.get('file')
            
            if not Path(backup_file).exists():
                print(f"✗ Fichier backup introuvable: {backup_file}")
                return False
            
            # Importer le fichier .reg
            result = subprocess.run(
                ["reg", "import", backup_file],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print(f"✓ Registre restauré: {backup_name}")
                return True
            else:
                print(f"✗ Erreur restauration: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"✗ Erreur: {e}")
            return False
    
    def restore_file_backup(self, backup_name: str) -> bool:
        """
        Restaure un backup de fichier
        
        Args:
            backup_name: Nom du backup à restaurer
        
        Returns:
            True si succès
        """
        try:
            # Trouver le backup
            backup = next((b for b in self.backups if b.get('name') == backup_name), None)
            
            if not backup or backup.get('type') != 'file':
                print(f"✗ Backup fichier introuvable: {backup_name}")
                return False
            
            backup_file = Path(backup.get('backup'))
            source_file = Path(backup.get('source'))
            
            if not backup_file.exists():
                print(f"✗ Fichier backup introuvable: {backup_file}")
                return False
            
            # Restaurer le fichier
            shutil.copy2(backup_file, source_file)
            
            print(f"✓ Fichier restauré: {source_file}")
            return True
            
        except Exception as e:
            print(f"✗ Erreur: {e}")
            return False
    
    def clean_old_backups(self, days: int = 30) -> int:
        """
        Supprime les backups plus anciens que X jours
        
        Args:
            days: Nombre de jours de rétention
        
        Returns:
            Nombre de backups supprimés
        """
        from datetime import timedelta
        
        count = 0
        cutoff_date = datetime.now() - timedelta(days=days)
        new_backups = []
        
        for backup in self.backups:
            try:
                backup_date = datetime.fromisoformat(backup.get('timestamp', ''))
                
                if backup_date < cutoff_date:
                    # Supprimer les fichiers associés
                    if backup.get('type') in ['registry', 'file']:
                        file_path = Path(backup.get('backup', backup.get('file', '')))
                        if file_path.exists():
                            file_path.unlink()
                    count += 1
                else:
                    new_backups.append(backup)
                    
            except:
                new_backups.append(backup)
        
        self.backups = new_backups
        self.save_backup_index()
        
        print(f"✓ {count} ancien(s) backup(s) supprimé(s)")
        return count
