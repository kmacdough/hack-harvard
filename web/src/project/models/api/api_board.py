class ApiBoard(object):
    def __init__(self, board):
        """
        :param board:
        :type board: chess.Board
        """
        self.board = board

    def as_json(self):
        return {
            "fen": self.board.fen(),
            "moves": [move.uci() for move in self.board.move_stack]}