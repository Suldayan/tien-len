from src.card import CARD
from src.rank import RANK
from src.suit import SUIT
import random

#just added some shuffle functions and deal function to this deck class
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
        
        self.reset()
    
    def shuffle(self):
        random.shuffle(self.cards)
    
    def deal(self, num_cards): #num cards is number of cards want to take from the deck usually 13
        dealt_cards = self.cards[:num_cards] #use slicing to select num_cards from self.cards, does not remove yet just 
        #add cards to dealt_cards
        self.cards = self.cards[num_cards:] #remove dealt_cards from self.cards
        return dealt_cards

    def reset(self):
        self.cards = [CARD(suit, rank)
                      for rank in self.ranks
                      for suit in self.suits]