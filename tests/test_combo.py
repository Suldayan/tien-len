from src.core.combo import is_straight, is_triple, is_pair, is_four_of_a_kind
from src.core.card import CARD
from src.core.rank import RANK
from src.core.suit import SUIT

def make_card(suit, suit_rank, suit_sym, suit_code, rank, rank_val, rank_sym):
    return CARD(SUIT(suit, suit_rank, suit_sym, suit_code), RANK(rank, rank_val, rank_sym))

class TestIsStraight:
    def test_three_card_straight(self):
        cards = [
            make_card("Spades", 1, "♠", "S", "THREE", 1, "3"),
            make_card("Spades", 1, "♠", "S", "FOUR",  2, "4"),
            make_card("Spades", 1, "♠", "S", "FIVE",  3, "5"),
        ]
        assert is_straight(cards) is True

    def test_non_consecutive_is_not_straight(self):
        cards = [
            make_card("Spades", 1, "♠", "S", "THREE", 1, "3"),
            make_card("Spades", 1, "♠", "S", "FOUR",  2, "4"),
            make_card("Spades", 1, "♠", "S", "SIX",   4, "6"),
        ]
        assert is_straight(cards) is False

class TestIsTriple:
    def test_three_queens_is_triple(self):
        cards = [
            make_card("Hearts",   4, "♥", "H", "QUEEN", 10, "Q"),
            make_card("Spades",   1, "♠", "S", "QUEEN", 10, "Q"),
            make_card("Diamonds", 3, "♦", "D", "QUEEN", 10, "Q"),
        ]
        assert is_triple(cards) is True

    def test_mixed_ranks_is_not_triple(self):
        cards = [
            make_card("Hearts",   4, "♥", "H", "QUEEN", 10, "Q"),
            make_card("Spades",   1, "♠", "S", "QUEEN", 10, "Q"),
            make_card("Diamonds", 3, "♦", "D", "KING",  11, "K"),
        ]
        assert is_triple(cards) is False

class TestIsPair:
    def test_two_queens_is_pair(self):
        cards = [
            make_card("Clubs",    2, "♣", "C", "QUEEN", 10, "Q"),
            make_card("Diamonds", 3, "♦", "D", "QUEEN", 10, "Q"),
        ]
        assert is_pair(cards) is True

    def test_different_ranks_is_not_pair(self):
        cards = [
            make_card("Clubs",    2, "♣", "C", "QUEEN", 10, "Q"),
            make_card("Diamonds", 3, "♦", "D", "KING",  11, "K"),
        ]
        assert is_pair(cards) is False

class TestIsFourOfAKind:
    def test_four_queens_is_four_of_a_kind(self):
        cards = [
            make_card("Diamonds", 3, "♦", "D", "QUEEN", 10, "Q"),
            make_card("Clubs",    2, "♣", "C", "QUEEN", 10, "Q"),
            make_card("Spades",   1, "♠", "S", "QUEEN", 10, "Q"),
            make_card("Hearts",   4, "♥", "H", "QUEEN", 10, "Q"),
        ]
        assert is_four_of_a_kind(cards) is True

    def test_three_of_a_kind_is_not_four_of_a_kind(self):
        cards = [
            make_card("Diamonds", 3, "♦", "D", "QUEEN", 10, "Q"),
            make_card("Clubs",    2, "♣", "C", "QUEEN", 10, "Q"),
            make_card("Spades",   1, "♠", "S", "QUEEN", 10, "Q"),
            make_card("Hearts",   4, "♥", "H", "KING",  11, "K"),
        ]
        assert is_four_of_a_kind(cards) is False