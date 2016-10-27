import urllib2
import json
import time

HOST = "localhost"
PORT = 5000
BOARD_NAME = "myboard"

STATUS_COOLDOWN_S = 1.0

def main():
    board_id = register_board(BOARD_NAME)

class PhysicalBoard(object):
    def __init__(self, name):
        self.name = name
        self.status = Registering()

    def run(self):
        end_types = {Broken}
        while type(self.status) not in end_types:
            next_status = self.status.run()
            self.status = next_status

class BoardStatus(object):
    def run(self):
        raise NotImplementedError()

class Registering(BoardStatus):
    def __init__(self, physical_board):
        self.physical_board = physical_board

    def run(self):
        board_id = self.register_board()
        return Unused(self.physical_board, board_id)

    def register_board(self):
        name = self.physical_board.name
        json_response = json_from_endpoint('/register/physical_board/{}'.format(name))
        return json_response['board_id']


class Unused(BoardStatus):
    def __init__(self, physical_board, board_id):
        self.physical_board = physical_board
        self.board_id = board_id

    def run(self):
        endpoint = '/physical_board/status/{}'.format(self.board_id)
        response_json = json_from_endpoint(endpoint)
        data_json = response_json["data"]
        board_status = data_json["board_status"]
        if board_status == "unused":
            time.sleep(STATUS_COOLDOWN_S)
            return self
        elif board_status == "is_player":
            return IsPlayer(self.physical_board, data_json["player_id"])
        elif board_status == "is_view":
            return IsView(self.physical_board, data_json["game_id"])
        else:
            return Broken(self.physical_board)


class IsView(BoardStatus):
    def __init__(self, physical_board, game_id):
        self.physical_board = physical_board
        self.game_id = game_id

    def run(self):
        endpoint = '/game/view/{}'.format(game_id)
        response_json = json_from_endpoint(endpoint)
        data_json = response_json["data"]
        game_status = data_json["game_status"]
        if game_status != "waiting_for_players":
            board_json = data_json["board"]
            moves = board_json["moves"]
            self.physical_board.update(moves)

        if game_status == "game_over":
            return Registering(self.physical_board)
        else:
            time.sleep(STATUS_COOLDOWN_S)
            return self


class Broken(BoardStatus):
    def __init__(self, physical_board, reason):
        self.physical_board = physical_board
        self.reason = reason

    def run(self):
        exit(1)


class IsPlayer(BoardStatus):
    def __init__(self, board, player_id):
        self.board = board
        self.player_id = player_id

    def run(self):
        end_types = {Broken}
        status = PlayerWaitForGame(self.board)
        return Registering(self.board)

class PlayerStatus(object):
    pass

class PlayerWaitForGame(PlayerStatus):
    def run(self):
        endpoint = '/player/status/{}'.format(self.player_id) # TODO hmm
        response_json = json_from_endpoint(endpoint)
        data_json = response_json['data']
        player_status = data_json['player_status']
        if player_status == "waiting_for_game":
            time.sleep(STATUS_COOLDOWN_S)
            return self
        elif player_status == "starting_game":
            board = data_json['board']
            moves = board['moves']
            self.board.update(moves) #TODO check board
            return PlayerStartingGame()
        else:
            return PlayerBroken()

class PlayerStartingGame(PlayerStatus):
    def run(self):
        endpoint = '/player/status/{}'.format(self.player_id)
        response_json = json_from_endpoint(endpoint)
        data_json = response_json['data']
        player_status = data_json['player_status']
        

class PlayerWaitForTurn(PlayerStatus):
    pass

class PlayerTakeTurn(PlayerStatus):
    pass

class PlayerGameOver(PlayerStatus):
    pass

class PlayerBroken(PlayerStatus):


def json_from_endpoint(endpoint):
    url = url_for_endpoint(endpoint)
    response = urllib2.urlopen(url)
    try:
        return json.load(response)
    except ValueError:
        return None


def url_for_endpoint(endpoint):
    return '{}:{}{}'.format(HOST, PORT, endpoint)