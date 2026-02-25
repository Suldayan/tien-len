from src.player import Player

class Bot(Player):
    def __init__(self, name, hand=None, points=0):
        super().__init__(name, hand, points)