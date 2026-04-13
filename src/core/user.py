from src.core.player import Player

class User(Player):
    def __init__(self, name, hand, points=0):
        super().__init__(name, hand, points)

    # No need to configure logic for the user because it's UI dependent on card selection
    def make_move(self, game):
        return "Waiting on user move..."