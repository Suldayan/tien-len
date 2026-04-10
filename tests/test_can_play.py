import pytest
from src.core.card import CARD
from src.core.suit import SUIT
from src.core.rank import RANK
from src.core.combo import make_combo
from src.game.validateplay import can_play


class MockGame:
    def __init__(self, current_combo):
        self.current_combo = current_combo

@pytest.fixture
def spades():
    return SUIT("Spades", 1, "♠", "S")

@pytest.fixture
def diamonds():
    return SUIT("Diamonds", 3, "♦", "D")

@pytest.fixture
def clubs():
    return SUIT("Clubs", 2, "♣", "C")

@pytest.fixture
def hearts():
    return SUIT("Hearts", 4, "♥", "H")

@pytest.fixture
def empty_pot():
    return MockGame(None)

@pytest.fixture
def single_two_pot(spades):
    return MockGame(make_combo([CARD(spades, RANK("TWO", 13, "2"))]))

@pytest.fixture
def four_of_a_kind_queens(spades, clubs, diamonds, hearts):
    return make_combo([
        CARD(diamonds, RANK("QUEEN", 10, "Q")),
        CARD(clubs,    RANK("QUEEN", 10, "Q")),
        CARD(spades,   RANK("QUEEN", 10, "Q")),
        CARD(hearts,   RANK("QUEEN", 10, "Q")),
    ])

@pytest.fixture
def pair_of_twos(spades, diamonds):
    return MockGame(make_combo([
        CARD(spades,   RANK("TWO", 13, "2")),
        CARD(diamonds, RANK("TWO", 13, "2")),
    ]))

@pytest.fixture
def triple_twos(spades, clubs, diamonds):
    return MockGame(make_combo([
        CARD(spades,   RANK("TWO", 13, "2")),
        CARD(clubs,    RANK("TWO", 13, "2")),
        CARD(diamonds, RANK("TWO", 13, "2")),
    ]))

@pytest.fixture
def four_pair_double_straight(spades, diamonds):
    ranks = [
        RANK("NINE",  7,  "9"), RANK("TEN",   8,  "10"),
        RANK("JACK",  9,  "J"), RANK("QUEEN", 10, "Q"),
    ]
    return make_combo([
        card
        for rank in ranks
        for card in [CARD(spades, rank), CARD(diamonds, rank)]
    ])

@pytest.fixture
def five_pair_double_straight(spades, diamonds):
    ranks = [
        RANK("NINE",  7,  "9"), RANK("TEN",   8,  "10"),
        RANK("JACK",  9,  "J"), RANK("QUEEN", 10, "Q"),
        RANK("KING",  11, "K"),
    ]
    return make_combo([
        card
        for rank in ranks
        for card in [CARD(spades, rank), CARD(diamonds, rank)]
    ])


# --- Tests ---

class TestEmptyPot:
    def test_any_combo_allowed_when_pot_is_none(self, empty_pot, spades):
        any_combo = make_combo([CARD(spades, RANK("TWO", 13, "2"))])
        assert can_play(empty_pot, any_combo) is True


class TestBombsAgainstTwos:
    def test_four_of_a_kind_beats_single_two(self, single_two_pot, four_of_a_kind_queens):
        assert can_play(single_two_pot, four_of_a_kind_queens) is True

    def test_four_pair_double_straight_beats_pair_of_twos(self, pair_of_twos, four_pair_double_straight):
        assert can_play(pair_of_twos, four_pair_double_straight) is True

    def test_five_pair_double_straight_beats_triple_twos(self, triple_twos, five_pair_double_straight):
        assert can_play(triple_twos, five_pair_double_straight) is True


class TestComboTypeMatching:
    def test_mismatched_types_are_rejected(self, spades, diamonds):
        game = MockGame(make_combo([CARD(spades, RANK("NINE", 7, "9"))]))
        pair = make_combo([
            CARD(spades,   RANK("TEN", 8, "10")),
            CARD(diamonds, RANK("TEN", 8, "10")),
        ])
        assert can_play(game, pair) is False


class TestStraights:
    def test_straight_different_length_rejected(self, spades, diamonds):
        game = MockGame(make_combo([
            CARD(spades, RANK("NINE",  7,  "9")),
            CARD(spades, RANK("TEN",   8,  "10")),
            CARD(spades, RANK("JACK",  9,  "J")),
            CARD(spades, RANK("QUEEN", 10, "Q")),
        ]))
        shorter = make_combo([
            CARD(spades,   RANK("JACK",  9,  "J")),
            CARD(spades,   RANK("QUEEN", 10, "Q")),
            CARD(diamonds, RANK("KING",  11, "K")),
        ])
        assert can_play(game, shorter) is False

    def test_double_straight_higher_beats_lower(self, spades, diamonds):
        game = MockGame(make_combo([
            CARD(spades,   RANK("THREE", 1, "3")), CARD(diamonds, RANK("THREE", 1, "3")),
            CARD(spades,   RANK("FOUR",  2, "4")), CARD(diamonds, RANK("FOUR",  2, "4")),
            CARD(spades,   RANK("FIVE",  3, "5")), CARD(diamonds, RANK("FIVE",  3, "5")),
        ]))
        high = make_combo([
            CARD(spades,   RANK("JACK",  9,  "J")), CARD(diamonds, RANK("JACK",  9,  "J")),
            CARD(spades,   RANK("QUEEN", 10, "Q")), CARD(diamonds, RANK("QUEEN", 10, "Q")),
            CARD(spades,   RANK("KING",  11, "K")), CARD(diamonds, RANK("KING",  11, "K")),
        ])
        assert can_play(game, high) is True