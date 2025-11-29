# 🖥️ Micro:bit PC Monitoring

Un système de monitoring PC interactif utilisant un **micro:bit** pour afficher en temps réel diverses informations système sur sa matrice LED 5x5.

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![MicroPython](https://img.shields.io/badge/MicroPython-micro%3Abit-green.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 📋 Table des matières

- [À propos](#-à-propos)
- [Fonctionnalités](#-fonctionnalités)
- [Architecture](#-architecture)
- [Prérequis](#-prérequis)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Utilisation](#-utilisation)
- [Structure du projet](#-structure-du-projet)
- [Pages disponibles](#-pages-disponibles)

## 🎯 À propos

Ce projet permet de transformer votre **micro:bit** en un moniteur système compact. Le micro:bit communique avec votre PC via connexion série (USB) et affiche différentes métriques système sur sa matrice LED 5x5. L'application PC fonctionne en arrière-plan avec une icône dans la barre des tâches.

## ✨ Fonctionnalités

### Monitoring système
- 📊 **CPU** : Affichage de l'utilisation du processeur
- 💾 **RAM** : Utilisation de la mémoire vive  
- 🎮 **GPU** : Utilisation et température du GPU (NVIDIA)
- 🌡️ **Température** : Monitoring de la température GPU
- 💨 **Ventilateurs** : Vitesse des ventilateurs GPU
- 🗄️ **VRAM** : Utilisation de la mémoire vidéo

### Fonctionnalités supplémentaires
- 💡 **Contrôle WLED** : Intégration pour contrôler des LED WLED (en développement)
- 🌡️ **Température ambiante** : Affichage de la température de la pièce
- 🖱️ **Contrôle d'écran** : Gestion de l'affichage
- 🎨 **Pages multiples** : Navigation entre différentes vues sur le micro:bit
- 📱 **Icône système** : Application en arrière-plan avec icône dans la barre des tâches

## 🏗️ Architecture

Le projet est divisé en deux parties principales :

### 1. **Code Micro:bit** (`microbit/`)
Écrit en **MicroPython**, ce code s'exécute sur le micro:bit et :
- Reçoit les données du PC via UART (série)
- Transforme les pourcentages en barres LED visuelles
- Affiche les informations sur la matrice LED 5x5
- Gère différentes pages d'affichage

### 2. **Application PC** (`pc_side/`)
Écrite en **Python**, cette application :
- Collecte les métriques système (CPU, RAM, GPU, etc.)
- Envoie les données au micro:bit via connexion série
- Gère la connexion et la reconnexion automatique
- Fournit une interface système tray pour contrôler l'application

## 🔧 Prérequis

### Matériel
- 1x **micro:bit** (v1 ou v2)
- 1x **Câble USB** pour connecter le micro:bit au PC

### Logiciels
- **Python 3.x** installé sur votre PC
- **Pilotes micro:bit** (généralement installés automatiquement)

### Dépendances Python
```bash
pip install pyserial psutil pynvml pystray pillow pyyaml
```

| Package | Description |
|---------|-------------|
| `pyserial` | Communication série avec le micro:bit |
| `psutil` | Récupération des métriques système (CPU, RAM) |
| `pynvml` | Monitoring GPU NVIDIA |
| `pystray` | Icône dans la barre des tâches |
| `pillow` | Gestion des images pour l'icône système |
| `pyyaml` | Lecture des fichiers de configuration |

## 📥 Installation

### 1. Cloner le projet
```bash
git clone https://github.com/votre-utilisateur/Micro-bit-PC-monitoring.git
cd Micro-bit-PC-monitoring
```

### 2. Installer les dépendances
```bash
pip install -r requirements.txt
```

> **Note** : Si le fichier `requirements.txt` n'existe pas, installez manuellement les packages listés dans la section [Prérequis](#-prérequis).

### 3. Flasher le micro:bit
1. Connectez votre micro:bit au PC
2. Copiez le fichier `microbit/micro_bit_code.py` sur le micro:bit :
   - Option A : Utilisez l'éditeur **Mu Editor** (recommandé pour débutants)
   - Option B : Utilisez **Thonny** ou un autre IDE MicroPython
   - Option C : Utilisez l'outil en ligne de commande `uflash`

```bash
# Avec uflash
uflash microbit/micro_bit_code.py
```

### 4. Identifier le port série
Sur **Windows**, ouvrez le Gestionnaire de périphériques et notez le port COM du micro:bit (ex: `COM14`).

Sur **macOS/Linux** :
```bash
ls /dev/tty.*
# Recherchez quelque chose comme /dev/ttyACM0
```

## ⚙️ Configuration

### Fichier `config/config.yml`
```yaml
# Configuration du port série
microbit_port: 'COM14'  # Windows : COMx ; macOS/Linux : /dev/ttyACMx
baud_rate: 115200  # Doit correspondre au réglage du micro:bit
UPDATE_INTERVAL: 0.25  # Intervalle de mise à jour (en secondes)
Retray_timeout: 2  # Délai avant nouvelle tentative de connexion (en secondes)
```

### Fichier `config/wled_config.yml`
Configuration pour l'intégration WLED (en développement).

## 🚀 Utilisation

### Lancer l'application

#### Méthode 1 : Avec fenêtre console
```bash
python -m pc_side.main
```

#### Méthode 2 : En arrière-plan (sans console)
Double-cliquez sur le fichier `Run.pyw` ou exécutez :
```bash
pythonw Run.pyw
```

L'application se lancera en arrière-plan avec une icône dans la barre des tâches.

### Arrêter l'application
- Clic droit sur l'icône dans la barre des tâches → **Quitter**
- Ou fermez la console si vous avez utilisé la méthode 1

## 📁 Structure du projet

```
Micro-bit-PC-monitoring/
│
├── microbit/                   # Code MicroPython pour le micro:bit
│   └── micro_bit_code.py       # Programme principal du micro:bit
│
├── pc_side/                    # Application Python côté PC
│   ├── core/                   # Modules principaux
│   │   ├── connection_manager.py   # Gestion de la connexion série
│   │   ├── system_monitor.py      # Collecte des métriques système
│   │   └── Main_RAM_PC_usage.pyw  # (Legacy)
│   │
│   ├── features/               # Fonctionnalités supplémentaires
│   │   ├── screen_control.py      # Contrôle de l'écran
│   │   └── wled_control.py        # Contrôle WLED
│   │
│   ├── ui/                     # Interface utilisateur
│   │   └── system_tray.py         # Icône barre des tâches
│   │
│   ├── other/                  # Utilitaires
│   │   └── All_basic_function.py  # Fonctions génériques
│   │
│   ├── image/                  # Ressources graphiques
│   │   ├── Color/              # Indicateurs de statut
│   │   │   ├── green.jpg       # Statut : connecté
│   │   │   ├── red.jpg         # Statut : déconnecté
│   │   │   └── yelow.jpg       # Statut : en attente
│   │   └── logo.png            # Logo de l'application
│   │
│   └── main.py                 # Point d'entrée principal
│
├── config/                     # Fichiers de configuration
│   ├── config.yml              # Configuration principale
│   └── wled_config.yml         # Configuration WLED
│
├── Run.pyw                     # Lanceur sans console
├── .gitignore                  # Fichiers ignorés par Git
└── README.md                   # Ce fichier
```

## 📱 Pages disponibles

Le micro:bit peut afficher plusieurs pages différentes. Vous pouvez naviguer entre elles (fonctionnalité à implémenter selon vos besoins).

### 1. **Page Monitoring** (principale)
Affiche les métriques système :
- Barres LED pour CPU, RAM, GPU
- Animations pour indiquer l'activité
- Indicateurs visuels de température

### 2. **Page WLED** (en développement)
Contrôle des LED WLED connectées :
- États on/off
- Couleurs
- Effets

### 3. **Page Température** (en développement)
Affiche la température ambiante de la pièce

## 🔧 Comment ça marche ?

### Communication PC ↔ micro:bit

1. **L'application PC** collecte les métriques système
2. Les données sont formatées en chaîne : `"Page:Données"`
3. Envoi via **UART** (série) au **micro:bit** à 115200 bauds
4. Le **micro:bit** reçoit les données et les décode
5. Les valeurs sont converties en barres LED visuelles
6. Affichage sur la **matrice LED 5x5**

### Exemple de données envoyées
```
Monitoring:CPU=45,RAM=62,GPU=30,TEMP=65
```

### Visualisation sur le micro:bit

La fonction `Pourcentage_to_liste()` convertit un pourcentage (0-100%) en une liste de 5 LEDs avec différents niveaux de luminosité :

- **0-20%** : 1 LED allumée
- **20-40%** : 2 LEDs allumées
- **40-60%** : 3 LEDs allumées
- **60-80%** : 4 LEDs allumées
- **80-100%** : 5 LEDs allumées

Les LEDs partiellement allumées permettent une granularité fine de l'affichage.

## 🛠️ Développement et personnalisation

### Ajouter une nouvelle page

1. **Modifiez** `pc_side/main.py` pour changer la variable `Page`
2. **Ajoutez** la logique d'envoi des données correspondantes
3. **Modifiez** `microbit/micro_bit_code.py` pour gérer la nouvelle page

### Ajouter une nouvelle métrique

1. **Étendez** `SystemMonitor` dans `pc_side/core/system_monitor.py`
2. **Ajoutez** une méthode pour collecter la métrique
3. **Envoyez** la donnée via `ConnectionManager`
4. **Traitez** et affichez sur le micro:bit

## 🐛 Dépannage

### Le micro:bit ne se connecte pas
- ✅ Vérifiez que le port COM est correct dans `config/config.yml`
- ✅ Assurez-vous que le micro:bit est bien connecté via USB
- ✅ Vérifiez qu'aucune autre application n'utilise le port série
- ✅ Redémarrez le micro:bit (débranchez/rebranchez)

### Pas de données affichées
- ✅ Vérifiez que le code MicroPython est bien flashé sur le micro:bit
- ✅ Vérifiez le baudrate (doit être 115200 des deux côtés)
- ✅ Consultez les messages d'erreur dans la console

### L'icône système ne s'affiche pas
- ✅ Vérifiez que les images sont présentes dans `pc_side/image/Color/`
- ✅ Installez correctement `pystray` et `Pillow`

## 📝 TODO / Améliorations futures

- [ ] Implémenter la navigation entre pages avec les boutons A/B du micro:bit
- [ ] Compléter l'intégration WLED
- [ ] Ajouter un capteur de température externe
- [ ] Créer une interface graphique de configuration
- [ ] Support multi-plateforme (Linux, macOS)
- [ ] Historique des métriques
- [ ] Alertes visuelles quand les seuils sont dépassés
- [ ] Mode économie d'énergie

## 📄 Licence

Ce projet est sous licence **MIT**. Vous êtes libre de l'utiliser, le modifier et le redistribuer.

## 👤 Auteur

**Jules**

---

⭐ Si ce projet vous plaît, n'hésitez pas à lui donner une étoile sur GitHub !
