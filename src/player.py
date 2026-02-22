class Player:
    def __init__(self, name, hand, points=0):
        self.hand = hand
        self.name = name
        self.points = points
        self.turn = False

    def get_name(self):
        return self.name
    
    def get_hand(self):
        return self.hand
    
    def get_points(self):
        return self.points
    
    def set_turn(self, turn: bool):
        self.turn = turn
    
    def is_turn(self):
        return self.turn
    
    # TODO: Create more methods here when game logic is configured (point management, turn, etc...)
