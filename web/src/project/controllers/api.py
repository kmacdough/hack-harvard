import uuid
from flask import render_template, jsonify

from .. import app
from ..models.api import ApiChessGame, ApiExternalChessPlayer, ApiObjectManager, ApiPhysicalBoard

player_manager = ApiObjectManager(ApiExternalChessPlayer)
game_manager = ApiObjectManager(ApiChessGame)
physical_board_manager = ApiObjectManager(ApiPhysicalBoard)


@app.route('/register/web_player', methods=['GET'])
def register_player():
    player_id = player_manager.add_new_object()
    return success_response(data={"player_id": player_id})


@app.route('/register/physical_board/<name>', methods=['GET'])
def register_physical_board(name):
    physical_board_manager.add_new_object(name)
    return success_response(data={"board_id": name})


@app.route('/register/physical_player/<board_id>', methods=['GET'])
def register_physical_player(board_id):
    physical_board = physical_board_manager.get_object(board_id)
    if physical_board is None:
        return does_not_exist_response("Physical Board")
    player_id = player_manager.add_new_object()
    physical_board.set_is_player(player_id)
    return success_response()


@app.route('/register/physical_view/<game_id>/<board_id>', methods=['GET'])
def register_physical_view(game_id, board_id):
    physical_board = physical_board_manager.get_object(board_id)
    if physical_board is None:
        return does_not_exist_response("Physical Board")
    game = game_manager.get_object(game_id)
    if game is None:
        return does_not_exist_response("Game")
    physical_board.set_is_view(game_id)
    return success_response()


@app.route('/game/create', methods=['GET'])
def create_game():
    game_id = game_manager.add_new_object()
    return success_response(data={"game_id": game_id})


@app.route('/game/add_player/<game_id>/<player_id>', methods=['GET'])
def add_player_to_game(game_id, player_id):
    game = game_manager.get_object(game_id)
    if game is None:
        return does_not_exist_response("Game")
    player = player_manager.get_object(player_id)
    if player is None:
        return does_not_exist_response("Player")
    did_add = game.add_api_external_player(player)
    if did_add:
        return success_response()
    else:
        return fail_response(message="Could not add player to game")


@app.route('/game/view/<game_id>', methods=['GET'])
def view_game(game_id):
    game = game_manager.get_object(game_id)
    if game is None:
        return does_not_exist_response("Game")
    game_status = game.get_status()
    if game_status == ApiChessGame.Status.WAITING_FOR_PLAYERS:
        return success_response(data={"game_status": game_status})
    return success_response(
        data={
            "board": game.get_api_board.as_json(),
            "game_status": game.get_status()
        })


@app.route('/player/status/<player_id>')
def player_status(player_id):
    player = player_manager.get_object(player_id)
    if player is None:
        return does_not_exist_response("Player")
    status = player.get_status()

    if status == ApiExternalChessPlayer.Status.MAKE_MOVE or \
            status == ApiExternalChessPlayer.Status.STARTING_GAME:
        return success_response(data={
            "player_status": status,
            "board": player.get_board().as_json()
        })
    else:
        return success_response(data={"player_status": status})


@app.route('/player/start_game/<player_id>')
def player_start_game(player_id):
    player = player_manager.get_object(player_id)
    if player is None:
        return does_not_exist_response("Player")
    status = player.get_status()
    if status is not ApiExternalChessPlayer.Status.STARTING_GAME:
        return fail_response(message="Game not currently starting")
    player.start_game()
    game = game_manager.get_object(player.get_game_id())
    game.try_start_game()
    return success_response()


@app.route('/player/make_move/<player_id>/<uci_move>')
def player_make_move(player_id, uci_move):
    player = player_manager.get_object(player_id)
    if player is None:
        return does_not_exist_response("Player")
    if player.get_status() != ApiExternalChessPlayer.Status.MAKE_MOVE:
        return fail_response(message="Not your turn!")
    player.set_move_uci(uci_move)
    return success_response()


@app.route('/physical_board/status/<board_id>')
def physical_board_status(board_id):
    physical_board = physical_board_manager.get_object(board_id)
    if physical_board is None:
        return does_not_exist_response("Physical Board")
    return success_response(data=physical_board.get_status().as_json())


@app.route('/preview_all_objects')
def preview_all_objects():
    players = player_manager.get_object_dict()
    player_descriptions = {id_: player.get_status() for id_, player in players.items()}
    games = game_manager.get_object_dict()
    game_descriptions = {id_: game.get_status() for id_, game in games.items()}
    boards = physical_board_manager.get_object_dict()
    board_descriptions = {id_: board.get_status() for id_, board in boards.items()}

    return success_response(data={
        "players": player_descriptions,
        "games": game_descriptions,
        "physical_boards": board_descriptions,
    })

class Empty:
    pass


def response_with_status(status, data=Empty, message=Empty):
    response_dict = {"status": status}
    if data is not Empty:
        response_dict["data"] = data
    if message is not Empty:
        response_dict["message"] = message
    return jsonify(response_dict)


def success_response(data=Empty, message=Empty):
    return response_with_status("success", data, message)


def fail_response(data=Empty, message=Empty):
    return response_with_status("success", data, message)


def error_response(data=Empty, message=Empty):
    return response_with_status("success", data, message)


def does_not_exist_response(object_label):
    return fail_response(message="{} does not exist.".format(object_label))