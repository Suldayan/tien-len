from src.player import Player

class User(Player):
    def __init__(self, name, hand, points=0):
        super().__init__(name, hand, points)