from src.card import CARD
from src.rank import RANK
from src.suit import SUIT


class DECK:
    def __init__(self):
        self.suits = [
            SUIT("Hearts", 4, "♥"),
            SUIT("Spades", 1, "♠"),
            SUIT("Clubs", 2, "♣"),
            SUIT("Diamonds", 3, "♦")
        ]

        self.ranks = [
            RANK("ACE", 12, "A"), RANK("TWO", 13, "2"),
            RANK("THREE", 1, "3"), RANK("FOUR", 2, "4"),
            RANK("FIVE", 3, "5"), RANK("SIX", 4, "6"),
            RANK("SEVEN", 5, "7"), RANK("EIGHT", 6, "8"),
            RANK("NINE", 7, "9"), RANK("TEN", 8, "10"),
            RANK("JACK", 9, "J"), RANK("QUEEN", 10, "Q"),
            RANK("KING", 11, "K")
        ]

        self.cards = [CARD(suit, rank)
                      for rank in self.ranks
                      for suit in self.suits]
