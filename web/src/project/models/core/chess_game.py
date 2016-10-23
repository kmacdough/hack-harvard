import chess
from collections import deque

from .chess_player import ChessPlayer

class ChessGame(object):
    WHITE = "white"
    BLACK = "black"

    def __init__(self, white_player, black_player):
        """

        :param white_player:
        :type ChessPlayer
        :param black_player:
        :type ChessPlayer
        """
        self.board = chess.Board()
        self.white_player = ChessPlayer(white_player)
        self.black_player = ChessPlayer(black_player)
        self.play_order = [white_player, black_player]

    def run_game(self):
        while not self.is_game_over():
            self.play_turn()
        self.broadcast_to_players(ChessPlayer.end_game, self.get_board_copy())

    def play_turn(self):
        current_player = self.current_player()
        success, uci_move = current_player.make_move_uci(self.board)
        if not success:
            return False
        self.board.push_uci(uci_move)
        self.broadcast_to_players(ChessPlayer.send_move_uci, uci_move)
        self.progress_turn()
        return True

    def broadcast_to_players(self, method, *args):
        for player in self.play_order:
            method(player, *args)

    def current_player(self):
        return self.play_order[0]

    def progress_turn(self):
        self.play_order.append(self.play_order.pop(0))


    def is_game_over(self):
        """
        :return: (True, <reason>) or (False, None)
        """
        return self.board.is_game_over()

    def get_board_copy(self):
        board = chess.Board(self.board.fen())
        board.move_stack = deque(self.board.move_stack)
        return board
