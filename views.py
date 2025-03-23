from flask import Flask, render_template, redirect, url_for, request, jsonify, session
import jeu 

app = Flask(__name__)
app.secret_key = "ENAC-RAMI"
app.template_folder = "template"
app.static_folder = "static"


# 🔹 Page d'accueil
@app.route("/")
def index():
    return render_template("index.html")


# 🔹 Page des règles du jeu
@app.route("/rules")
def rules():
    return render_template("rules.html")


# 🔹 Page du jeu local (humain seul ou deux humains)
@app.route("/game<string:d>[<int:id>,<string:Id>]", methods=["GET", "POST"])
def game(d, id, Id):
    if id == 3:
        jeu.init(['J1', 'J2'])  # Initialisation pour jeu local
        return redirect(url_for("game", d=d, id=0, Id=Id))

    action = request.form.get("action")
    selected_cards = request.form.getlist("selected_cards")

    if action:
        if action[:4] == "take":
            jeu.take(Id, action)
        elif action == "pose":
            print(selected_cards,type(selected_cards))
            jeu.pose(selected_cards, Id)
        elif action == "give":
            if len(selected_cards) > 1:
                id -= 1
            else:
                try:
                    jeu.give(Id, int(selected_cards[0]))
                except:
                    id -= 1

        if jeu.scores.get(Id, 0) >= 51:
            return redirect(url_for("win", winner=Id))
    return render_template(
        "game.html",
        player=Id,
        other_player='J2' if Id == 'J1' else 'J1',
        cartesPosees=jeu.cartesPosees,
        Joueurs=jeu.Joueurs,
        scores=jeu.scores,
        cartes=jeu.cartes,
        R=jeu.R,
        K=jeu.K,
        word=d,
        id=id,
    )


# 🔹 API pour mise à jour dynamique
@app.route("/update", methods=["GET"])
def update():
    return jsonify(jeu.get_game_state())


# 🔹 Page de victoire
@app.route("/win/<winner>")
def win(winner):
    return render_template("win.html", winner=winner)


# 🔹 Page du menu multijoueur
@app.route("/multiplayer")
def multiplayer():
    return render_template("multiplayer.html")


# 🔹 Création d'une nouvelle partie multijoueur
@app.route("/create_game", methods=["POST"])
def create_game_route():
    player_name = request.form.get("player_name")
    game_id = jeu.create_game([player_name])
    session['player_name'] = player_name
    return redirect(url_for("game_online", game_id=game_id, player=player_name))


# 🔹 Rejoindre une partie existante
@app.route("/join_game", methods=["POST"])
def join_game_route():
    game_id = request.form.get("game_id")
    player_name = request.form.get("player_name")
    success = jeu.join_game(game_id, player_name)
    if success:
        session['player_name'] = player_name
        return redirect(url_for("game_online", game_id=game_id, player=player_name))
    return "Partie introuvable", 404


# 🔹 Affichage de la partie multijoueur
@app.route("/online/<game_id>/<player>", methods=["GET", "POST"])
def game_online(game_id, player):
    state = jeu.get_game_state(game_id)
    if not state:
        return "Partie introuvable", 404

    if request.method == "POST":
        action = request.form.get("action")
        selected_cards = request.form.getlist("selected_cards")

        if state["current_turn"] == player:
            if action in ["takeRandom", "takeKnown"]:
                jeu.multiplayer_take(game_id, player, action)
            elif action == "pose":
                jeu.multiplayer_pose(game_id, player, selected_cards)
            elif action == "give":
                try:
                    index = int(selected_cards[0])
                    jeu.multiplayer_give(game_id, player, index)
                    jeu.next_turn(game_id)
                except:
                    pass

    return render_template("game.html",
        player=player,
        other_player=[p for p in state["joueurs_list"] if p != player][0] if len(state["joueurs_list"]) > 1 else "",
        cartesPosees=state["cartesPosees"],
        Joueurs=state["Joueurs"],
        scores=state["scores"],
        cartes=jeu.cartes,
        R=state["R"],
        K=state["K"],
        word="M",  # Multijoueur
        id=0
    )


# 🔹 Lancement de l'application
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
