from . import ApiBoard

MAX_PLAYERS = 2


class ApiChessGame(object):
    def __init__(self):
        self._game = None
        self._players = []
        self._status = ApiChessGame.Status.WAITING_FOR_PLAYERS

    def add_api_external_player(self, player):
        if len(self._players) >= 2:
            return False
        self._players.append(player)
        if len(self._players) == 2:
            self._status = ApiChessGame.Status.STARTING_GAME
        return True

    def try_start_game(self):
        pass

    def get_status(self):
        return self._status

    def get_board(self):
        if self._game is None:
            return None
        return ApiBoard(self._game.get_board_copy())

    class Status:
        WAITING_FOR_PLAYERS = "waiting_for_players"
        STARTING_GAME = "starting_game"
        IN_GAME = "in_game"
        GAME_OVER = "game_over"
