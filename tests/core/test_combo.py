from src.core.combo import (
    is_straight, is_double_straight, make_combo
)
from tests.conftest import make_card, make_cards, make_quad, SUITS, RANK_BY_VALUE

class TestIsStraight:
    def test_two_in_straight_is_invalid(self):
        assert is_straight(make_cards(11, 12, 13)) is False

    def test_thirteen_cards_too_long(self):
        assert is_straight(make_cards(*range(1, 14))) is False

class TestIsDoubleStraight:
    def _ds(self, rank_vals):
        return [make_card(RANK_BY_VALUE[v], s)
                for v in rank_vals for s in ["spades", "hearts"]]

    def test_odd_number_of_cards(self):
        cards = self._ds([1, 2, 3])
        cards.pop()
        assert is_double_straight(cards) is False

    def test_25_cards_too_long(self):
        cards = self._ds(range(1, 14))
        cards.pop()
        assert is_double_straight(cards) is False

class TestMakeCombo:
    def test_single_card(self):
        combo = make_combo(make_cards("FIVE"))
        assert combo.combo_type == "SINGLE"
        assert combo.length == 1

    def test_pair(self):
        combo = make_combo([make_card("QUEEN", "clubs"), make_card("QUEEN", "hearts")])
        assert combo.combo_type == "PAIR"
        assert combo.length == 2

    def test_triple(self):
        combo = make_combo([make_card("FIVE", s) for s in SUITS[:3]])
        assert combo.combo_type == "TRIPLE"
        assert combo.length == 3

    def test_four_of_a_kind(self):
        combo = make_combo(make_quad("SEVEN"))
        assert combo.combo_type == "FOUR_OF_A_KIND"
        assert combo.length == 4

    def test_straight(self):
        combo = make_combo(make_cards(1, 2, 3, 4, 5))
        assert combo.combo_type == "STRAIGHT"
        assert combo.length == 5

    def test_double_straight(self):
        cards = [make_card(r, s)
                 for r in ["THREE", "FOUR", "FIVE"]
                 for s in ["spades", "diamonds"]]
        combo = make_combo(cards)
        assert combo.combo_type == "DOUBLE_STRAIGHT"
        assert combo.length == 6

    def test_invalid_hand_returns_none(self):
        assert make_combo(make_cards(1, 3, 5)) is None