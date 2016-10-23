
class ApiPhysicalBoard:
    def __init__(self):
        self._status = ApiPhysicalBoard.Status.Unused()

    def get_status(self):
        return self._status

    def set_unused(self):
        self._status = ApiPhysicalBoard.Status.Unused()

    def set_is_player(self, player_id):
        self._status = ApiPhysicalBoard.Status.IsPlayer(player_id)

    def set_is_view(self, game_id):
        self._status = ApiPhysicalBoard.Status.IsView(game_id)

    class Status:

        class Unused:
            def as_json(self):
                return {"board_status": "unused"}

        class IsPlayer:
            def __init__(self, player_id):
                self.player_id = player_id

            def as_json(self):
                return {
                    "board_status": "is_player",
                    "player_id": self.player_id
                }

        class IsView:
            def __init__(self, game_id):
                self.game_id = game_id

            def as_json(self):
                return {
                    "board_status": "is_view",
                    "game_id": self.game_id
                }