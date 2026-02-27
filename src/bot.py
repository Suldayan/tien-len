from src.player import Player

class Bot(Player):
    def __init__(self, name, hand=None, points=0):
        super().__init__(name, hand, points)

    def make_move(self, game):
        """
        The bot strategy: Find the lowest playable card.
        Returns a list of CARD objects or None to pass.
        """
        hand_cards = self.get_hand().get_cards()
        
        # We sort the cards so the bot plays the weakest possible valid card first.
        hand_cards.sort() 

        # Case 1: The table is empty (New Round)
        # The bot must play something. We choose the lowest card.
        if game.current_combo is None:
            return [hand_cards[0]]

        # Case 2: There are cards on the table.
        # The bot looks for the first single card that can beat the current combo.
        for card in hand_cards:
            # We use the player's own hand logic to identify the combo type
            temp_combo = self.hand.make_combo([card])
            
            # Check if this card is strong enough to play
            if temp_combo and game.can_play(temp_combo):
                return [card]

        # Case 3: No playable cards found.
        # Returning None tells the Game/UI that the bot passes.
        return None