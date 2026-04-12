from src.game.validateplay import can_play
from tests.conftest import (
    MockGame, make_single, make_pair, make_triple,
    make_quad, make_straight, make_double_straight, make_combo
)

class TestEmptyPot:
    def test_any_single_allowed(self, empty_game):
        assert can_play(empty_game, make_single("THREE")) is True

    def test_any_pair_allowed(self, empty_game):
        assert can_play(empty_game, make_pair("QUEEN")) is True

    def test_any_straight_allowed(self, empty_game):
        assert can_play(empty_game, make_straight(["THREE","FOUR","FIVE"])) is True

class TestBombsAgainstTwos:
    def test_four_of_a_kind_beats_single_two(self):
        game = MockGame(make_single("TWO"))
        assert can_play(game, make_combo(make_quad("QUEEN"))) is True

    def test_double_straight_any_length_beats_single_two(self):
        game = MockGame(make_single("TWO"))
        assert can_play(game, make_double_straight(["THREE","FOUR","FIVE"])) is True

    def test_four_pair_double_straight_beats_pair_of_twos(self):
        game = MockGame(make_pair("TWO"))
        assert can_play(game, make_double_straight(["NINE","TEN","JACK","QUEEN"])) is True

    def test_five_pair_double_straight_beats_triple_twos(self):
        game = MockGame(make_triple("TWO"))
        assert can_play(game, make_double_straight(["NINE","TEN","JACK","QUEEN","KING"])) is True

class TestBombBoundaries:
    def test_three_pair_double_straight_cannot_beat_pair_of_twos(self):
        game = MockGame(make_pair("TWO"))
        assert can_play(game, make_combo(make_quad("QUEEN"))) is False

    def test_four_pair_double_straight_cannot_beat_triple_twos(self):
        game = MockGame(make_triple("TWO"))
        assert can_play(game, make_double_straight(["NINE","TEN","JACK","QUEEN"])) is False

    def test_four_of_a_kind_cannot_beat_pair_of_twos(self):
        game = MockGame(make_pair("TWO"))
        assert can_play(game, make_combo(make_quad("QUEEN"))) is False

    def test_four_of_a_kind_cannot_beat_single_non_two(self):
        game = MockGame(make_single("ACE"))
        assert can_play(game, make_combo(make_quad("QUEEN"))) is False

    def test_double_straight_cannot_beat_single_non_two(self):
        game = MockGame(make_single("ACE"))
        assert can_play(game, make_double_straight(["THREE","FOUR","FIVE"])) is False

class TestTypeMismatch:
    def test_pair_cannot_beat_single(self):
        game = MockGame(make_single("THREE"))
        assert can_play(game, make_pair("TEN")) is False

    def test_single_cannot_beat_pair(self):
        game = MockGame(make_pair("THREE"))
        assert can_play(game, make_single("ACE")) is False

    def test_triple_cannot_beat_pair(self):
        game = MockGame(make_pair("KING"))
        assert can_play(game, make_triple("ACE")) is False

    def test_straight_cannot_beat_pair(self):
        game = MockGame(make_pair("KING"))
        assert can_play(game, make_straight(["THREE","FOUR","FIVE"])) is False

class TestLengthMismatch:
    def test_longer_straight_rejected(self):
        game = MockGame(make_straight(["THREE","FOUR","FIVE"]))
        assert can_play(game, make_straight(["THREE","FOUR","FIVE","SIX"])) is False

    def test_shorter_straight_rejected(self):
        game = MockGame(make_straight(["THREE","FOUR","FIVE","SIX"]))
        assert can_play(game, make_straight(["FOUR","FIVE","SIX"])) is False

    def test_longer_double_straight_rejected(self):
        game = MockGame(make_double_straight(["THREE","FOUR","FIVE"]))
        assert can_play(game, make_double_straight(["THREE","FOUR","FIVE","SIX"])) is False

    def test_shorter_double_straight_rejected(self):
        game = MockGame(make_double_straight(["THREE","FOUR","FIVE","SIX"]))
        assert can_play(game, make_double_straight(["FOUR","FIVE","SIX"])) is False

class TestStrengthComparisons:
    def test_higher_single_beats_lower(self):
        game = MockGame(make_single("THREE"))
        assert can_play(game, make_single("FOUR")) is True

    def test_lower_single_cannot_beat_higher(self):
        game = MockGame(make_single("KING"))
        assert can_play(game, make_single("NINE")) is False

    def test_same_rank_higher_suit_beats_lower_suit(self):
        game = MockGame(make_single("QUEEN", "spades"))
        assert can_play(game, make_single("QUEEN", "hearts")) is True

    def test_same_rank_lower_suit_cannot_beat_higher_suit(self):
        game = MockGame(make_single("QUEEN", "hearts"))
        assert can_play(game, make_single("QUEEN", "spades")) is False

    def test_higher_pair_beats_lower(self):
        game = MockGame(make_pair("THREE"))
        assert can_play(game, make_pair("FOUR")) is True

    def test_lower_pair_cannot_beat_higher(self):
        game = MockGame(make_pair("KING"))
        assert can_play(game, make_pair("FOUR")) is False

    def test_higher_straight_beats_lower(self):
        game = MockGame(make_straight(["THREE","FOUR","FIVE"]))
        assert can_play(game, make_straight(["FOUR","FIVE","SIX"])) is True

    def test_lower_straight_cannot_beat_higher(self):
        game = MockGame(make_straight(["NINE","TEN","JACK"]))
        assert can_play(game, make_straight(["THREE","FOUR","FIVE"])) is False

    def test_higher_double_straight_beats_lower(self):
        game = MockGame(make_double_straight(["THREE","FOUR","FIVE"]))
        assert can_play(game, make_double_straight(["JACK","QUEEN","KING"])) is True

    def test_lower_double_straight_cannot_beat_higher(self):
        game = MockGame(make_double_straight(["JACK","QUEEN","KING"]))
        assert can_play(game, make_double_straight(["THREE","FOUR","FIVE"])) is False