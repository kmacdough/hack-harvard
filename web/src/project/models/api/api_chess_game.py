import threading

from .api_board import ApiBoard
from .api_external_chess_player import ApiExternalChessPlayer
from ..core import ChessGame

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
        if len(self._players) == MAX_PLAYERS and \
            all(player.status == ApiExternalChessPlayer.Status.STARTING_GAME
                for player in self._players):
            self._game = ChessGame(self._players[0], self._players[1])
            self.run_game_in_separate_thread()

    def run_game_in_separate_thread(self):
        def start_game():
            self._game.run_game()

        thread = threading.Thread(target=start_game)
        thread.daemon = True
        thread.start()

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
