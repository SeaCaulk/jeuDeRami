from random import shuffle
import uuid
import os

# 🔹 Variables globales pour le mode local
R = []
K = []
scores = {}
cartesPosees = []
Joueurs = {}
current_turn = 0

# 🔹 Chemins des images des cartes
cartes = {
    f"{i}{k}": f"/static/img/Cartes/{j}_{k}.png"
    for i, j in [('H', 'Coeur'), ('C', 'Carreau'), ('P', 'Pique'), ('T', 'Trefle')]
    for k in range(7, 15)
}

# 🔹 Chargement de l’état du jeu local s’il existe
if os.path.exists("jeu.txt") and os.path.getsize("jeu.txt") > 0:
    with open("jeu.txt", "r") as file:
        R = eval(file.readline())
        scores = eval(file.readline())
        cartesPosees = eval(file.readline())
        Joueurs = eval(file.readline())
        K = eval(file.readline())
        current_turn = eval(file.readline())

# 🔹 Sauvegarde de l’état du jeu local
def save():
    with open("jeu.txt", "w") as file:
        file.write(f"{R}\n{scores}\n{cartesPosees}\n{Joueurs}\n{K}\n{current_turn}")

# 🔹 Initialisation du jeu local
def init(joueurs):
    global R, scores, cartesPosees, Joueurs, K, current_turn
    R = []
    scores = {}
    cartesPosees = []
    Joueurs = {}
    K = []
    current_turn = 0

    CartesC = list(cartes.keys()) * 2
    shuffle(CartesC)

    for i, joueur in enumerate(joueurs):
        Joueurs[joueur] = []
        scores[joueur] = 0
        for _ in range(14 + int(i == 0)):
            Joueurs[joueur].append(CartesC.pop())

    while CartesC:
        if len(CartesC) % 2 == 0:
            R.append(CartesC.pop())
        else:
            K.append(CartesC.pop())

    save()

# 🔹 Calcul du score (local)
def score(player, L):
    for i in L:
        valeur = Joueurs[player][int(i)][1:]
        if valeur in ['7', '8', '9', '10']:
            scores[player] += int(valeur)
        elif valeur in ['11', '12', '13']:
            scores[player] += 10
        elif valeur == '14':
            scores[player] += 11
    save()

# 🔹 Prendre une carte (local)
def take(joueur, action):
    if action == "takeRandom" and R:
        Joueurs[joueur].append(R.pop())
    elif action == "takeKnown" and K:
        Joueurs[joueur].append(K.pop())
    save()

# 🔹 Poser des cartes (local)
def pose(liste_index, joueur):
    liste_index = [int(i) for i in liste_index]
    print(liste_index,Joueurs[joueur])
    selected = [Joueurs[joueur][i] for i in sorted(liste_index, reverse=True)]
    selected.sort()

    if len(selected) < 3:
        return False

    if all(selected[0][1:] == c[1:] for c in selected):
        score(joueur, liste_index)
        for i in sorted(liste_index, reverse=True):
            del Joueurs[joueur][i]
        cartesPosees.append(selected)
        save()
        return True

    valeurs = [int(c[1:]) for c in selected]
    if all(selected[0][0] == c[0] for c in selected) and sorted(valeurs) == list(range(min(valeurs), max(valeurs) + 1)):
        score(joueur, liste_index)
        for i in sorted(liste_index, reverse=True):
            del Joueurs[joueur][i]
        cartesPosees.append(selected)
        save()
        return True

    return False

# 🔹 Donner une carte (local)
def give(joueur, index):
    K.append(Joueurs[joueur][index])
    del Joueurs[joueur][index]
    save()

# 🔹 État actuel du jeu local
def get_game_state():
    return {
        "R": R,
        "K": K,
        "scores": scores,
        "cartesPosees": cartesPosees,
        "Joueurs": Joueurs,
        "current_turn": current_turn,
    }

# 🔹 Tour suivant (local)
def next_turn():
    global current_turn
    current_turn = (current_turn + 1) % len(Joueurs)
    save()

# ===============================================
# 🔹 MODE MULTIJOUEUR EN LIGNE
# ===============================================
games = {}  # Dictionnaire global pour stocker les parties multijoueurs

def create_game(players):
    """Créer une partie multijoueur unique"""
    game_id = str(uuid.uuid4())[:8]
    game_data = {
        "R": [],
        "K": [],
        "scores": {},
        "cartesPosees": [],
        "Joueurs": {},
        "current_turn": players[0],
        "joueurs_list": players
    }

    CartesC = list(cartes.keys()) * 2
    shuffle(CartesC)

    for i, joueur in enumerate(players):
        game_data["Joueurs"][joueur] = []
        game_data["scores"][joueur] = 0
        for _ in range(14):
            game_data["Joueurs"][joueur].append(CartesC.pop())

    while CartesC:
        if len(CartesC) % 2 == 0:
            game_data["R"].append(CartesC.pop())
        else:
            game_data["K"].append(CartesC.pop())

    games[game_id] = game_data
    return game_id

def join_game(game_id, player_name):
    """Ajouter un joueur à une partie existante"""
    if game_id in games and player_name not in games[game_id]["Joueurs"]:
        deck = games[game_id]["R"] + games[game_id]["K"]
        shuffle(deck)
        games[game_id]["Joueurs"][player_name] = [deck.pop() for _ in range(14)]
        games[game_id]["scores"][player_name] = 0
        games[game_id]["R"] = deck[:len(deck)//2]
        games[game_id]["K"] = deck[len(deck)//2:]
        games[game_id]["joueurs_list"].append(player_name)
        return True
    return False

def get_game_state(game_id):
    return games.get(game_id, None)

def multiplayer_take(game_id, player, action):
    game = games[game_id]
    if action == "takeRandom" and game["R"]:
        game["Joueurs"][player].append(game["R"].pop())
    elif action == "takeKnown" and game["K"]:
        game["Joueurs"][player].append(game["K"].pop())

def multiplayer_pose(game_id, player, liste_index):
    game = games[game_id]
    liste_index = [int(i) for i in liste_index]
    selected = [game["Joueurs"][player][i] for i in sorted(liste_index, reverse=True)]
    selected.sort()

    if len(selected) < 3:
        return False

    valeurs = [int(c[1:]) for c in selected]

    if all(selected[0][1:] == c[1:] for c in selected):
        for i in sorted(liste_index, reverse=True):
            del game["Joueurs"][player][i]
        game["cartesPosees"].append(selected)
        return True

    if all(selected[0][0] == c[0] for c in selected) and sorted(valeurs) == list(range(min(valeurs), max(valeurs)+1)):
        for i in sorted(liste_index, reverse=True):
            del game["Joueurs"][player][i]
        game["cartesPosees"].append(selected)
        return True

    return False

def multiplayer_give(game_id, player, index):
    game = games[game_id]
    index = int(index)
    if 0 <= index < len(game["Joueurs"][player]):
        game["K"].append(game["Joueurs"][player][index])
        del game["Joueurs"][player][index]

def next_turn(game_id):
    game = games[game_id]
    joueurs = game["joueurs_list"]
    current = game["current_turn"]
    next_idx = (joueurs.index(current) + 1) % len(joueurs)
    game["current_turn"] = joueurs[next_idx]
