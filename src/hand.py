from src.combo import make_combo

class Hand:
    def __init__(self, cards):
        self.cards = cards

    def sort(self):
        self.cards.sort(key=lambda c: (c.rank.value, c.suit.SuitRank))

    def remove(self, card):
        self.cards.remove(card)

    def add(self, card):
        self.cards.append(card)

    def make_combo(self, selected_cards):
        return make_combo(selected_cards)
    
    def get_cards(self):
        return self.cards
    
    def get_selected_cards(self):
        return [card for card in self.cards if card.selected]
