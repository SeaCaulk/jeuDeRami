
# 🎴 Jeu de cartes Rami en Flask

Bienvenue, ce jeu de cartes de type Rami, développé en Python avec le framework **Flask**.  
Ce projet a été réalisé dans le cadre d’un module de développement par des **étudiants de l’ENAC** (École Nationale de l’Aviation Civile).

Le jeu prend en charge :
- 👤 Un joueur contre lui-même (solo)
- 👥 Deux joueurs en local (même machine)
- 🌐 Mode multijoueur en ligne (sur le même réseau ou via Internet)

---

## 🛠️ Prérequis

- Python 3.10+
- `pip` pour installer les dépendances
- Un terminal / invite de commande

---

## 📦 Installation

1. Clone le projet ou télécharge les fichiers :
   ```bash
   git clone https://github.com/ton-projet/kam-fin.git
   cd kam-fin
   ```

2. (Facultatif) Crée un environnement virtuel :
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate   # Windows
   ```

3. Installe Flask :
   ```bash
   pip install flask
   ```

---

## 🚀 Lancement du jeu

Lance le jeu avec :
```bash
python3 run.py
```

Par défaut, l’application s’exécute sur :
```
http://localhost:5000
```

---

## 🎮 Modes de jeu disponibles

### 🔹 1. Mode Solo
- Cliquez sur `Jouer > Tout seul ;-;`
- Le joueur J1 joue seul avec les règles classiques du Rami.

### 🔹 2. Mode Deux Joueurs Local
- Cliquez sur `Jouer > Contre humain`
- Deux joueurs jouent à tour de rôle sur le même écran.

### 🔹 3. Mode Multijoueur en ligne
- Cliquez sur `Jouer > Multijoueur`
- Remplissez :
  - Un **nom de joueur**
  - Créez une partie ou rejoignez une partie avec un identifiant
- Chaque joueur peut jouer depuis son propre appareil sur le **même réseau local**.

> ⚠️ Pour utiliser le mode multijoueur à distance, pensez à **ouvrir le port 5000** ou hébergez le jeu sur un serveur distant.

---

## 📁 Arborescence

```
kam-fin/
├── run.py               # Point d'entrée de l'app
├── views.py             # Routes Flask
├── jeu.py               # Logique du jeu
├── template/            # Fichiers HTML (pages)
│   ├── game.html
│   ├── rules.html
│   ├── multiplayer.html
│   └── layout/
├── static/              # Images, CSS, cartes
│   ├── img/Cartes/
│   └── css/
├── jeu.txt              # Sauvegarde de l'état du jeu local
└── README.md            # Fichier d'explication
```

---

## ✨ À venir

- Intelligence artificielle pour jouer contre l’ordinateur (mode "Mistral")
- Chat entre joueurs en multijoueur
- Système de leaderboard

---

## 👨‍💻 Auteurs

Projet développé dans le cadre d’un module pédagogique à l’**ENAC**  
Encadré par des enseignants du département informatique  
Réalisé par un groupe d'étudiants passionnés 👨‍🎓👩‍🎓

---

## 🧠 Licence

Ce projet est open-source. Vous pouvez l’adapter et le réutiliser librement à des fins pédagogiques.
