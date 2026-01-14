# 🚀 Guide de Démarrage Rapide - OptiWindows

## Installation en 3 étapes

### 1️⃣ Installer Python (si pas déjà installé)

1. Téléchargez Python depuis [python.org](https://www.python.org/downloads/)
2. **IMPORTANT** : Cochez "Add Python to PATH" lors de l'installation
3. Installez avec les paramètres par défaut

### 2️⃣ Installer les dépendances

**Option A - Automatique (recommandé)**
```cmd
Lancez install.bat (double-clic)
```

**Option B - Manuel**
```cmd
python -m pip install -r requirements.txt
```

### 3️⃣ Lancer OptiWindows

**Option A - Via launcher automatique (recommandé)**
```cmd
Lancez launcher.bat (double-clic)
```

**Option B - Via PowerShell**
```powershell
.\launcher.ps1
```

**Option C - Direct**
```cmd
python main.py
```

> ⚠️ **Important** : OptiWindows doit être exécuté en tant qu'administrateur !

---

## 📋 Utilisation Rapide

### Premier lancement

1. **Dashboard** : Vue d'ensemble de votre système
2. **Choisir un profil** : 
   - 🎮 Gaming : Pour joueurs
   - 🛡️ Confidentialité : Protection maximale
   - ⚡ Performance : Vitesse maximale
   - 💻 Par défaut : Équilibré

### Fonctions principales

#### 🧹 Nettoyage
- Fichiers temporaires
- Cache navigateurs
- Windows.old
- Cache système

#### 🚀 Optimisation
- Démarrage Windows
- Services inutiles
- Registre
- RAM

#### 🎮 Gaming
- Mode Gaming
- Ultimate Performance
- Optimisation GPU

#### 🔒 Confidentialité
- Télémétrie Windows
- Cortana/Copilot
- Publicités
- Tracking

#### 💾 Gestion Disque
- Analyse d'espace
- Fichiers volumineux
- Doublons
- Défragmentation

#### 🛠️ Réparation
- SFC (fichiers système)
- DISM (image Windows)
- Windows Update
- Réseau

---

## ⚙️ Configuration

### Fichiers de configuration

- `config/settings.json` : Paramètres généraux
- `config/profiles.json` : Profils d'optimisation

### Backup automatique

OptiWindows crée automatiquement :
- Points de restauration Windows
- Backup du registre avant modifications
- Logs de toutes les actions

Les backups sont dans `backups/`

### Logs

Les journaux sont dans `logs/optiwindows.log`

---

## 🆘 Résolution de problèmes

### Erreur "Droits administrateur requis"
➜ Lancez via `launcher.bat` ou clic-droit → "Exécuter en tant qu'administrateur"

### Erreur "Python introuvable"
➜ Réinstallez Python en cochant "Add Python to PATH"

### Erreur "Module introuvable"
➜ Lancez `install.bat` ou `pip install -r requirements.txt`

### L'interface ne s'affiche pas
➜ Vérifiez que customtkinter est installé : `pip install customtkinter`

### Erreur lors du nettoyage
➜ Vérifiez les logs dans `logs/optiwindows.log`

---

## 🎯 Conseils d'utilisation

### ✅ À faire

- Créer un point de restauration avant les grosses modifications
- Vérifier les logs après chaque action
- Utiliser les profils prédéfinis pour débuter
- Exporter votre configuration (Paramètres → Export)

### ❌ À éviter

- Ne pas désactiver trop de services sans savoir
- Ne pas supprimer Windows.old si Windows est récent
- Ne pas nettoyer en mode agressif sans backup

---

## 📊 Fonctionnalités avancées

### Export/Import de configuration

1. Paramètres → Export Config
2. Sauvegardez le fichier .json
3. Sur un autre PC : Paramètres → Import Config

### Planification automatique

1. Paramètres → Tâches planifiées
2. Activez et choisissez fréquence
3. OptiWindows s'exécutera automatiquement

### Mode Expert

1. Paramètres → Mode avancé
2. Accès à toutes les options détaillées

---

## 🔗 Liens utiles

- 📖 Documentation complète : `README.md`
- 📝 Changelog : `CHANGELOG.md`
- 🐛 Signaler un bug : Créez une issue
- 💡 Suggestions : Ouvrez une discussion

---

## 📞 Support

Pour toute question ou problème :

1. Consultez `README.md` pour plus de détails
2. Vérifiez les logs dans `logs/`
3. Créez une issue avec :
   - Description du problème
   - Logs pertinents
   - Version de Windows
   - Étapes pour reproduire

---

**Bon nettoyage ! 🚀**
