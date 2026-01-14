# 🚀 OptiWindows - Ultimate Windows Optimization Suite

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

**OptiWindows** est le logiciel d'optimisation Windows le plus complet avec **150+ fonctionnalités** ! Inspiré des meilleurs outils comme ChrisTitus WinUtil, avec des améliorations et innovations uniques.

## ✨ Fonctionnalités Principales

### 🧹 **Nettoyage Avancé**
- ✅ Fichiers temporaires (Windows Temp, User Temp, Prefetch)
- ✅ Cache navigateurs (Chrome, Firefox, Edge, Opera)
- ✅ Cache système (DNS, Thumbnails, Windows Update)
- ✅ Corbeille complète
- ✅ Fichiers journaux anciens
- ✅ Windows.old (anciennes installations)
- ✅ Crash dumps et rapports d'erreurs
- ✅ Windows Defender logs
- ✅ Delivery Optimization

### ⚡ **Optimisation Performance**
- ✅ Désactivation télémétrie Windows
- ✅ Optimisation mémoire (RAM)
- ✅ Désactivation applications en arrière-plan
- ✅ Optimisation planification processeur
- ✅ Optimisation paramètres réseau
- ✅ Désactivation Windows Search indexing
- ✅ Libération cache RAM
- ✅ Plans d'alimentation (Ultimate Performance)
- ✅ Optimisation SSD (TRIM)
- ✅ Optimisation registre

### 🎮 **Mode Gaming**
- ✅ Activation/Désactivation en un clic
- ✅ Arrêt services non essentiels
- ✅ Désactivation GameDVR/Game Bar
- ✅ Optimisation priorité CPU pour jeux
- ✅ Hardware Accelerated GPU Scheduling
- ✅ Désactivation algorithme de Nagle (latence réduite)
- ✅ Optimisations NVIDIA/AMD
- ✅ Optimisation TCP/IP pour gaming
- ✅ DNS gaming (Cloudflare)

### 🛡️ **Confidentialité & Sécurité**
- ✅ **Score de confidentialité** (0-100)
- ✅ Désactivation TOUTE la télémétrie
- ✅ Désactivation Cortana & Copilot
- ✅ Désactivation ID publicitaire
- ✅ Désactivation suivi localisation
- ✅ Désactivation historique d'activité
- ✅ Désactivation feedback Windows
- ✅ Suppression bloatware préinstallé
- ✅ Blocage domaines télémétrie (HOSTS)
- ✅ **MODE PARANOÏA** (confidentialité maximale)

### 🎨 **Effets Visuels**
- ✅ Désactivation transparence
- ✅ Désactivation animations
- ✅ Désactivation ombres
- ✅ Mode "Performances optimales"
- ✅ Dark Mode

### 💾 **Gestion Disque** (À venir)
- 🚧 Analyse utilisation disque
- 🚧 Détection fichiers volumineux
- 🚧 Recherche doublons
- 🚧 Défragmentation HDD

### 🚀 **Gestionnaire Démarrage** (À venir)
- 🚧 Visualisation programmes au démarrage
- 🚧 Activation/Désactivation
- 🚧 Score d'impact performance

### 📦 **Installateur Applications** (À venir)
- 🚧 Installation via Winget
- 🚧 Apps essentielles curées
- 🚧 Installation batch

### 🔧 **Tweaks Système** (À venir)
- 🚧 Personnalisations avancées
- 🚧 Import/Export configurations

### 🔨 **Outils Réparation** (À venir)
- 🚧 SFC (System File Checker)
- 🚧 DISM
- 🚧 Réparation Windows Update
- 🚧 Reset réseau

### 🎯 **Windows Features** (À venir)
- 🚧 WSL2, HyperV, .NET Framework
- 🚧 Windows Sandbox
- 🚧 Legacy Media

## 🖥️ Configuration Requise

- **OS**: Windows 10 / Windows 11
- **Python**: 3.8 ou supérieur
- **Privilèges**: Administrateur (requis)
- **RAM**: 2 GB minimum
- **Disque**: 100 MB

## 📦 Installation

### 1. Cloner le dépôt
```bash
git clone https://github.com/votre-repo/optiwindows.git
cd optiwindows
```

### 2. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 3. Lancer OptiWindows
```bash
python main.py
```

**Important**: Clic droit sur `main.py` > "Exécuter en tant qu'administrateur"

## 🎯 Utilisation

1. **Lancer le programme** en tant qu'administrateur
2. **Naviguer** entre les différents modules via le menu latéral
3. **Sélectionner** les optimisations souhaitées
4. **Cliquer** sur "Apply" ou "Start"
5. **Profiter** d'un Windows optimisé !

### 📌 Modules Disponibles

| Module | Description | Status |
|--------|-------------|--------|
| 🏠 Dashboard | Vue d'ensemble et actions rapides | ✅ |
| 🧹 Cleaner | Nettoyage système complet | ✅ |
| ⚡ Optimizer | Optimisations performance | ✅ |
| 🛡️ Privacy | Confidentialité et télémétrie | ✅ |
| 🎮 Gaming Mode | Optimisations gaming | ✅ |
| 💾 Disk Manager | Gestion disque | 🚧 |
| 🚀 Startup Manager | Gestion démarrage | 🚧 |
| 📦 Apps Installer | Installation apps | 🚧 |
| 🔧 Tweaks | Tweaks système | 🚧 |
| 🔨 Repair Tools | Outils réparation | 🚧 |
| 🎯 Features | Windows Features | 🚧 |

## 🛡️ Sécurité

- ✅ **Backup automatique** avant modifications critiques
- ✅ **Logging complet** de toutes les actions
- ✅ **Confirmations** pour actions irréversibles
- ✅ **Open source** - code entièrement vérifiable

## ⚠️ Avertissements

- Certaines optimisations nécessitent un **redémarrage**
- Les modifications avancées peuvent **affecter la stabilité**
- Toujours créer un **point de restauration** avant
- Utiliser le **MODE PARANOÏA** avec précaution

## 📊 Score Santé Système

OptiWindows calcule un **Health Score** (0-100) basé sur :
- Utilisation RAM
- Utilisation disque
- Utilisation CPU
- État général du système

## 🎨 Interface

Interface moderne avec **CustomTkinter** :
- 🌙 Dark Mode par défaut
- 📱 Design épuré et professionnel
- ⚡ Navigation rapide
- 📊 Visualisations en temps réel

## 🔍 Logs

Tous les événements sont enregistrés dans :
```
logs/optiwindows_YYYYMMDD.log
```

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- 🐛 Signaler des bugs
- 💡 Proposer des fonctionnalités
- 🔧 Soumettre des Pull Requests

## 📝 Roadmap

### Version 1.1 (Prochaine)
- [ ] Module Disk Manager complet
- [ ] Module Startup Manager
- [ ] Module Apps Installer avec Winget
- [ ] Export/Import configurations
- [ ] Thèmes personnalisables

### Version 1.2
- [ ] Monitoring temps réel avancé
- [ ] Benchmarks automatiques
- [ ] Détection drivers obsolètes
- [ ] Analyse SMART disques

### Version 2.0
- [ ] IA pour suggestions personnalisées
- [ ] Comparaison avec communauté
- [ ] Mode automatique intelligent
- [ ] API REST pour automation

## 📜 Licence

MIT License - Voir le fichier `LICENSE` pour plus de détails.

## 🙏 Remerciements

Inspiré par :
- **ChrisTitus WinUtil** - Pour l'inspiration et les idées
- **Microsoft** - Pour Windows... et ses possibilités d'optimisation 😄

## 📧 Support

- 🐛 **Issues**: [GitHub Issues](https://github.com/votre-repo/optiwindows/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/votre-repo/optiwindows/discussions)

## ⭐ Star History

Si OptiWindows vous aide, n'oubliez pas de mettre une ⭐ sur GitHub !

---

**Fait avec ❤️ pour la communauté Windows**

*OptiWindows - Rendez Windows aussi rapide que possible!* 🚀
