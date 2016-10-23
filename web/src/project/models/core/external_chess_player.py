

class ExternalChessPlayer(object):
    def end_game(self, board):
        raise NotImplementedError("Method must be implemented on subclass")

    def send_move_uci(self, uci_move):
        raise NotImplementedError("Method must be implemented on subclass")

    def make_move_uci(self):
        raise NotImplementedError("Method must be implemented on subclass")