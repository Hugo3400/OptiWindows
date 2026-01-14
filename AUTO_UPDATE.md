# 🔄 Auto-Update System - OptiWindows

## Vue d'ensemble

OptiWindows inclut maintenant un système de mise à jour automatique qui vérifie les nouvelles versions sur GitHub et les installe automatiquement.

## Fonctionnalités

### ✅ Détection Automatique
- Vérification au démarrage (après 2 secondes)
- Comparaison de version intelligente
- Vérification via GitHub API

### ✅ Notification Visuelle
- Bannière de notification en haut de l'interface
- Affichage de la nouvelle version disponible
- Boutons "Update Now" et "Later"

### ✅ Installation Automatique
- Téléchargement depuis GitHub
- Extraction et application automatique
- Préservation des données utilisateur (config, logs, backups)
- Barre de progression en temps réel
- Redémarrage automatique après installation

## Comment ça marche

### 1. Vérification des mises à jour

```python
from utils.auto_update import AutoUpdater

updater = AutoUpdater()
if updater.check_for_updates():
    print(f"Update available: {updater.latest_version}")
```

### 2. Information sur la mise à jour

```python
update_info = updater.get_update_info()
# {
#     'version': '1.1.0',
#     'name': 'Version 1.1.0',
#     'description': 'Release notes...',
#     'published_at': '2026-01-15T10:00:00Z',
#     'html_url': 'https://github.com/Hugo3400/OptiWindows/releases/tag/v1.1.0',
#     'download_url': 'https://github.com/...'
# }
```

### 3. Téléchargement

```python
def progress_callback(progress):
    print(f"Downloading: {progress:.1f}%")

updater.download_update(progress_callback)
```

### 4. Installation

```python
updater.apply_update()
updater.restart_application()
```

### 5. Processus complet (recommandé)

```python
def update_ui(message, progress):
    print(f"{message} - {progress}%")

if updater.full_update_process(update_ui):
    print("Update successful!")
```

## Architecture

### Fichiers concernés

```
utils/
  └── auto_update.py       # Module principal d'auto-update

main.py                    # Vérification au démarrage
ui/main_window.py          # UI notifications et installation
requirements.txt           # Dependencies (requests, packaging)
```

### Flux de mise à jour

```
1. Démarrage app
   ↓
2. Vérification GitHub API (background)
   ↓
3. Nouvelle version trouvée?
   ├─ Non → Continue normalement
   └─ Oui → Affiche notification
              ↓
4. Utilisateur clique "Update Now"
   ↓
5. Téléchargement release
   ↓
6. Extraction fichiers
   ↓
7. Backup config/logs/backups
   ↓
8. Copie nouveaux fichiers
   ↓
9. Restauration config/logs/backups
   ↓
10. Nettoyage fichiers temp
    ↓
11. Redémarrage automatique
```

## Configuration

### Version actuelle

Définie dans `utils/auto_update.py`:

```python
CURRENT_VERSION = "1.0.0"
```

⚠️ **Important:** Mettre à jour cette variable à chaque nouvelle version !

### Repository GitHub

```python
GITHUB_REPO = "Hugo3400/OptiWindows"
```

## Sécurité

### Fichiers préservés

Lors d'une mise à jour, ces dossiers sont **toujours préservés**:
- `config/` - Configuration utilisateur
- `logs/` - Fichiers de logs
- `backups/` - Sauvegardes système

### Fichiers exclus de la mise à jour

- `.git/` - Données Git
- `__pycache__/` - Cache Python
- `temp_update/` - Dossier temporaire
- `backup_before_update/` - Backup précédent

### Backup automatique

Avant chaque mise à jour, un backup complet est créé dans:
```
backup_before_update/
  ├── config/
  ├── logs/
  └── backups/
```

## Gestion des erreurs

### Timeout API

Si GitHub API ne répond pas:
- Timeout: 10 secondes
- Logging de l'erreur
- Continue sans mise à jour

### Échec du téléchargement

- Timeout: 30 secondes
- Retry automatique possible
- Message d'erreur à l'utilisateur

### Échec de l'installation

- Backup préservé
- Rollback possible manuel
- Logs détaillés dans `logs/`

## Utilisation Manuelle

### Via l'interface

1. Lancer l'application
2. Si mise à jour disponible → notification en haut
3. Cliquer "Update Now"
4. Attendre la progression
5. Application redémarre automatiquement

### Via le code

```python
from utils.auto_update import check_and_notify_update

# Vérification simple (non-bloquant)
update_info = check_and_notify_update()

if update_info:
    print(f"Version {update_info['version']} available!")
    print(f"Changes: {update_info['description']}")
```

## API GitHub

### Endpoints utilisés

```
GET /repos/Hugo3400/OptiWindows/releases/latest
```

**Réponse:**
```json
{
  "tag_name": "v1.1.0",
  "name": "OptiWindows v1.1.0",
  "body": "## Changes\n- New feature 1\n- Bug fix 2",
  "published_at": "2026-01-15T10:00:00Z",
  "html_url": "https://github.com/.../releases/tag/v1.1.0",
  "zipball_url": "https://api.github.com/.../zipball/v1.1.0"
}
```

### Rate Limiting

- GitHub API: 60 requêtes/heure (non authentifié)
- OptiWindows vérifie: 1 fois au démarrage
- Pas de risque de rate limit

## Tests

### Tester la vérification

```python
from utils.auto_update import AutoUpdater

updater = AutoUpdater()
print(f"Current: {updater.current_version}")

if updater.check_for_updates():
    info = updater.get_update_info()
    print(f"New version: {info['version']}")
    print(f"Download: {info['download_url']}")
else:
    print("Up to date!")
```

### Tester le téléchargement (sans installer)

```python
updater = AutoUpdater()
updater.download_url = "https://..."  # URL valide

if updater.download_update():
    print("Download OK, fichier dans: temp_update/update.zip")
```

## Rollback Manuel

Si problème après mise à jour:

1. **Vérifier le backup:**
   ```
   backup_before_update/
   ```

2. **Restaurer manuellement:**
   ```powershell
   # Copier config
   xcopy backup_before_update\config config\ /E /Y
   
   # Copier logs
   xcopy backup_before_update\logs logs\ /E /Y
   ```

3. **Réinstaller version précédente:**
   - Aller sur GitHub Releases
   - Télécharger version précédente
   - Extraire et remplacer

## Désactiver Auto-Update

### Temporairement

Commenter dans `main.py`:

```python
# threading.Thread(target=check_updates, daemon=True).start()
```

### Définitivement

Supprimer dans `ui/main_window.py`:

```python
# threading.Timer(2.0, self.check_for_updates).start()
```

## Logs

Tous les événements sont loggés:

```
logs/optiwindows.log

INFO: Checking for updates...
INFO: Update available: 1.0.0 -> 1.1.0
INFO: Downloading update from https://...
INFO: Update downloaded successfully
INFO: Applying update...
INFO: Updated: main.py
INFO: Updated: modules/cleaner.py
...
INFO: Update applied successfully
INFO: Restarting application...
```

## Dépendances

```txt
requests>=2.31.0   # HTTP requests pour GitHub API
packaging>=23.0    # Comparaison de versions
```

Installation:
```bash
pip install -r requirements.txt
```

## Roadmap

### Version Future

- [ ] **Delta updates** - Télécharger seulement les fichiers modifiés
- [ ] **Update channels** - Stable / Beta / Dev
- [ ] **Silent updates** - Installation en arrière-plan
- [ ] **Update schedule** - Vérifier quotidiennement/hebdomadaire
- [ ] **Changelog viewer** - Afficher les changements avant update
- [ ] **Rollback UI** - Bouton pour revenir à version précédente
- [ ] **Update notifications** - Toast non-bloquant au lieu de bannière

## FAQ

### Q: L'update écrase-t-il ma configuration?
**R:** Non, `config/`, `logs/` et `backups/` sont toujours préservés.

### Q: Que faire si l'update échoue?
**R:** Vérifiez `logs/optiwindows.log` et le dossier `backup_before_update/`. Vous pouvez restaurer manuellement.

### Q: Puis-je skip une version?
**R:** Oui, cliquez "Later". La notification réapparaîtra au prochain démarrage.

### Q: L'app fonctionne-t-elle sans internet?
**R:** Oui, mais vous ne recevrez pas de notifications de mise à jour.

### Q: Combien de temps prend une mise à jour?
**R:** Typiquement 30-60 secondes selon la taille et votre connexion.

---

## 🎉 Auto-Update Activé !

OptiWindows vérifie maintenant automatiquement les mises à jour à chaque démarrage. Vous serez toujours à jour avec les dernières fonctionnalités et correctifs de sécurité !
