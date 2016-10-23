import chess

from .external_chess_player import ExternalChessPlayer

MAX_RETRIES = 3

class ChessPlayer(object):
    def __init__(self, external_player):
        """

        :param external_player:
        :type external_player: ExternalChessPlayer
        """
        self.ext_player = external_player

    def end_game(self, board):
        self.ext_player.end_game(board)

    def send_move_uci(self, uci_move):
        self.ext_player.send_move_uci(uci_move)

    def make_move_uci(self, board):
        try:
            return True, self.try_get_uci_move()
        except Exception:
            return False, Exception

    def try_get_uci_move(self, board):
        tries = MAX_RETRIES
        while tries > 0:
            move = self.ext_player.make_move_uci(board)
            if move in board.legal_moves:
                return move
        raise RuntimeError("Too many bad moves")


