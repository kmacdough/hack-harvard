import chess
import time

from . import ApiBoard
from ..core import ExternalChessPlayer

MOVE_CHECK_SLEEP_SEC = 1.0


class ApiExternalChessPlayer(ExternalChessPlayer):
    class Status:
        WAITING_FOR_GAME = "waiting_for_game"
        STARTING_GAME = "starting_game"
        WAITING_FOR_TURN = "waiting_for_turn"
        MAKE_MOVE = "make_move"
        GAME_OVER = "game_over"

    def __init__(self):
        self._status = ApiExternalChessPlayer.Status.WAITING_FOR_GAME
        self._game_id = None

        self._move_made = None
        self._api_board = None

    # API methods

    def get_status(self):
        return self._status

    def set_game(self, game_id):
        self._status = ApiExternalChessPlayer.Status.STARTING_GAME
        self._game_id = game_id

    def start_game(self):
        self._status = ApiExternalChessPlayer.Status.WAITING_FOR_TURN

    def set_move_uci(self, uci_move):
        self._move_made = uci_move
        self._status = ApiExternalChessPlayer.Status.WAITING_FOR_TURN

    def get_game_id(self):
        return self._game_id

    def get_api_board(self):
        return self._api_board

    # ExternalChessPlayer methods

    def end_game(self, board):
        self._api_board = ApiBoard(board)
        self._status = ApiExternalChessPlayer.Status.GAME_OVER

    def send_move_uci(self, uci_move):
        # allows us to know if move succeeded
        self._move_made = None

    def make_move_uci(self, board):
        self._status = ApiExternalChessPlayer.Status.MAKE_MOVE
        self._api_board = ApiBoard(board)
        self._move_made = None
        while self._move_made is None:
            time.sleep(MOVE_CHECK_SLEEP_SEC)
        return self._move_made
