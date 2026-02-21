from src.combo import is_straight, is_triple, is_pair, is_four_of_a_kind
from src.card import CARD
from src.rank import RANK
from src.suit import SUIT

def make_card(suit, suit_val, suit_sym, rank, rank_val, rank_sym):
    return CARD(SUIT(suit, suit_val, suit_sym), RANK(rank, rank_val, rank_sym))

def test_straight():
    c1 = make_card("Spades", 1, "♠", "THREE", 1, "3")
    c2 = make_card("Spades", 1, "♠", "FOUR", 2, "4")
    c3 = make_card("Spades", 1, "♠", "FIVE", 3, "5")
    print("Straight test:", is_straight([c1, c2, c3]))

def test_triple():
    c1 = make_card("Hearts", 4, "♥", "QUEEN", 10, "Q")
    c2 = make_card("Spades", 1, "♠", "QUEEN", 10, "Q")
    c3 = make_card("Diamonds", 3, "♦", "QUEEN", 10, "Q")
    print("Triple test:", is_triple([c1, c2, c3]))

def test_pair():
    c1 = make_card("Clubs", 2, "♣", "QUEEN", 10, "Q")
    c2 = make_card("Diamonds", 3, "♦", "QUEEN", 10, "Q")
    print("Pair test:", is_pair([c1, c2]))

def test_four_of_a_kind():
    c1 = make_card("Diamonds", 3, "♦", "QUEEN", 10, "Q")
    c2 = make_card("Clubs", 2, "♣", "QUEEN", 10, "Q")
    c3 = make_card("Spades", 1, "♠", "QUEEN", 10, "Q")
    c4 = make_card("Hearts", 4, "♥", "QUEEN", 10, "Q")
    print("Four of a kind test:", is_four_of_a_kind([c1, c2, c3, c4]))

def main():
    # To run test, make sure to be in the root dir (TienLen) and run: 
    # python -m tests.test_combo in your terminal
    test_straight()
    test_triple()
    test_pair()
    test_four_of_a_kind()

if __name__ == "__main__":
    main()
