from tests.conftest import make_game, make_card, make_single
from src.core.combo import make_combo

class TestSetFirstTurn:
    def test_player_with_three_of_spades_goes_first(self):
        game = make_game([["FIVE"], ["THREE"]])
        game.set_first_turn()
        assert game.current_index == 1

    def test_required_card_is_set(self):
        game = make_game([["FIVE"], ["THREE"]])
        game.set_first_turn()
        assert game.required_card is not None

    def test_player_with_lowest_card_goes_first_if_no_three_of_spades(self):
        game = make_game([["QUEEN"], ["FOUR"]])
        game.set_first_turn()
        assert game.current_index == 1

class TestIsGameOver:
    def test_not_over_when_multiple_players_have_cards(self):
        game = make_game([["THREE"], ["FIVE"]])
        assert game.is_game_over() is False

    def test_over_when_one_player_has_no_cards(self):
        game = make_game([[], ["FIVE"]])
        assert game.is_game_over() is True

    def test_over_when_all_players_empty(self):
        game = make_game([[], []])
        assert game.is_game_over() is True

class TestPlayCards:
    def test_valid_play_removes_cards_from_hand(self):
        game = make_game([["THREE", "FOUR"], ["FIVE"]])
        game.first_move_of_match = False 
        card = game.players[0].hand.get_cards()[0]
        success, _ = game.play_cards([card])
        assert success is True
        assert card not in game.players[0].hand.get_cards()

    def test_invalid_combo_returns_false(self):
        game = make_game([["THREE", "FIVE"], ["SEVEN"]])
        cards = game.players[0].hand.get_cards()
        success, _ = game.play_cards(cards)
        assert success is False

    def test_play_advances_turn(self):
        game = make_game([["THREE", "FOUR"], ["FIVE"]])
        game.first_move_of_match = False 
        card = game.players[0].hand.get_cards()[0]
        game.play_cards([card])
        assert game.current_index == 1

    def test_first_move_must_include_required_card(self):
        game = make_game([["THREE", "FOUR"], ["FIVE"]])
        game.set_first_turn()
        wrong_card = next(
            c for c in game.players[game.current_index].hand.get_cards()
            if c != game.required_card
        )
        success, msg = game.play_cards([wrong_card])
        assert success is False
        assert "First move" in msg

    def test_returns_finished_message_when_hand_empty(self):
        game = make_game([["THREE"], ["FIVE"]])
        game.first_move_of_match = False 
        card = game.players[0].hand.get_cards()[0]
        success, msg = game.play_cards([card])
        assert success is True
        assert "finished" in msg

class TestHandleTwoChop:
    def test_chop_transfers_points(self):
        game = make_game([["THREE", "FOUR", "FIVE", "SIX"], ["TWO"]])
        game.current_combo = make_single("TWO")
        game.last_player_index = 1

        four_cards = [make_card("QUEEN", s) for s in ["spades", "clubs", "diamonds", "hearts"]]
        quad_combo = make_combo(four_cards)

        game.handle_two_chop(quad_combo, game.players[0])
        assert game.players[0].get_points() > 0
        assert game.players[1].get_points() < 0

    def test_no_chop_when_no_twos_in_pot(self):
        game = make_game([["THREE"], ["FIVE"]])
        game.current_combo = make_single("KING")
        game.last_player_index = 1

        quad_cards = [make_card("QUEEN", s) for s in ["spades", "clubs", "diamonds", "hearts"]]
        quad_combo = make_combo(quad_cards)

        result = game.handle_two_chop(quad_combo, game.players[0])
        assert result is None