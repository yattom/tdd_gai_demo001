from flask import Flask, request, jsonify
from uuid import uuid4
from tcg import Game, GameSetting

app = Flask(__name__)
sessions = {}

@app.route('/game/start', methods=['POST'])
def start_game():
    data = request.json
    session_id = str(uuid4())
    game = Game(GameSetting(names=(data['player1'], data['player2'])))
    sessions[session_id] = game
    return jsonify({"session_id": session_id})

@app.route('/game/<session_id>/state', methods=['GET'])
def get_game_state(session_id):
    game = sessions.get(session_id)
    if not game:
        return jsonify({"error": "Invalid session ID"}), 404
    state = {
        "turn_no": game.current_turn_no,
        "current_player": game.get_turn()['player'],
        "life_points": game.life_points,
        "hand": game.cards(game.get_turn()['player'])
    }
    return jsonify(state)

@app.route('/game/<session_id>/play', methods=['POST'])
def play_card(session_id):
    data = request.json
    game = sessions.get(session_id)
    if not game:
        return jsonify({"error": "Invalid session ID"}), 404
    try:
        game.play(data['player'], data['card_index'])
        new_state = {
            "turn_no": game.current_turn_no,
            "current_player": game.get_turn()['player'],
            "life_points": game.life_points,
            "hand": game.cards(game.get_turn()['player'])
        }
        return jsonify({"success": True, "new_state": new_state})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/game/<session_id>/is_finished', methods=['GET'])
def is_game_finished(session_id):
    game = sessions.get(session_id)
    if not game:
        return jsonify({"error": "Invalid session ID"}), 404
    return jsonify({"is_finished": game.is_finished, "winner": game.get_turn()['opponent'] if game.is_finished else None})

if __name__ == '__main__':
    app.run(debug=True)