from tests.conftest import make_game, make_single
from src.game.round import start_new_round, pass_turn, next_turn, end_match, round_results

class TestNextTurn:
    def test_advances_to_next_player(self):
        game = make_game([["THREE"], ["FIVE"], ["SEVEN"]])
        game.current_index = 0
        next_turn(game)
        assert game.current_index == 1

    def test_wraps_around_to_first(self):
        game = make_game([["THREE"], ["FIVE"], ["SEVEN"]])
        game.current_index = 2
        next_turn(game)
        assert game.current_index == 0

    def test_skips_player_with_empty_hand(self):
        game = make_game([["THREE"], [], ["SEVEN"]])
        game.current_index = 0
        next_turn(game)
        # P1 has no cards, should skip to P2
        assert game.current_index == 2

    def test_sets_turn_flag_on_new_player(self):
        game = make_game([["THREE"], ["FIVE"], ["SEVEN"]])
        game.current_index = 0
        next_turn(game)
        assert game.players[1].get_turn() is True

    def test_clears_turn_flag_on_old_player(self):
        game = make_game([["THREE"], ["FIVE"], ["SEVEN"]])
        game.players[0].set_turn(True)
        game.current_index = 0
        next_turn(game)
        assert game.players[0].get_turn() is False

class TestStartNewRound:
    def test_increments_round_number(self):
        game = make_game([["THREE"], ["FIVE"]])
        game.last_player_index = 1
        start_new_round(game)
        assert game.round_number == 2

    def test_clears_current_combo(self):
        game = make_game([["THREE"], ["FIVE"]])
        game.current_combo = make_single("QUEEN")
        game.last_player_index = 1
        start_new_round(game)
        assert game.current_combo is None

    def test_clears_passed_set(self):
        game = make_game([["THREE"], ["FIVE"]])
        game.passed = {0, 1}
        game.last_player_index = 1
        start_new_round(game)
        assert len(game.passed) == 0

    def test_starter_index_sets_current_index(self):
        game = make_game([["THREE"], ["FIVE"], ["SEVEN"]])
        start_new_round(game, starter_index=2)
        assert game.current_index == 2

    def test_falls_back_to_last_player_index(self):
        game = make_game([["THREE"], ["FIVE"], ["SEVEN"]])
        game.last_player_index = 1
        start_new_round(game)
        assert game.current_index == 1

    def test_does_nothing_if_no_starter_and_no_last_player(self):
        game = make_game([["THREE"], ["FIVE"]])
        game.last_player_index = None
        game.current_index = 0
        start_new_round(game)  # should not crash
        assert game.current_index == 0

class TestPassTurn:
    def test_adds_current_player_to_passed(self):
        game = make_game([["THREE"], ["FIVE"], ["SEVEN"]])
        game.current_index = 0
        game.last_player_index = 1
        pass_turn(game)
        assert 0 in game.passed

    def test_new_round_starts_when_all_but_one_passed(self):
        game = make_game([["THREE"], ["FIVE"], ["SEVEN"]])
        game.current_index = 0
        game.last_player_index = 1
        game.passed = {2}  # one already passed; adding current (0) = 2 passed out of 3 active
        pass_turn(game)
        # round should have restarted — combo cleared
        assert game.current_combo is None

    def test_turn_advances_when_not_everyone_passed(self):
        game = make_game([["THREE"], ["FIVE"], ["SEVEN"]])
        game.current_index = 0
        game.last_player_index = 2
        pass_turn(game)
        # only 1 of 3 passed, should just advance turn
        assert game.current_index == 1

class TestEndMatch:
    def test_returns_player_with_empty_hand_as_winner(self):
        game = make_game([[], ["FIVE", "SIX"]])
        winner = end_match(game)
        assert winner == game.players[0]

    def test_winner_gains_points_for_loser_remaining_cards(self):
        game = make_game([[], ["FIVE", "SIX"]])  # loser has 2 cards
        end_match(game)
        assert game.players[0].get_points() == 20  # 2 * 10

    def test_loser_loses_points_for_remaining_cards(self):
        game = make_game([[], ["FIVE", "SIX"]])
        end_match(game)
        assert game.players[1].get_points() == -20

    def test_returns_none_if_no_winner(self):
        game = make_game([["THREE"], ["FIVE"]])
        winner = end_match(game)
        assert winner is None

    def test_multiple_losers_all_penalised(self):
        game = make_game([[], ["FIVE"], ["SIX", "SEVEN"]])
        end_match(game)
        # loser 1: 1 card = -10, loser 2: 2 cards = -20, winner: +30
        assert game.players[0].get_points() == 30
        assert game.players[1].get_points() == -10
        assert game.players[2].get_points() == -20

class TestRoundResults:
    def test_contains_winner_name(self):
        game = make_game([[], ["FIVE"]])
        result = round_results(game)
        assert "P0" in result

    def test_no_winner_shows_game_over(self):
        game = make_game([["THREE"], ["FIVE"]])
        result = round_results(game)
        assert "Game Over" in result