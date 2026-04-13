class UIActions:
    def __init__(self, ui):
        self.ui = ui

    def update_playable_hands(self):
        if self.ui.user.is_turn():
            self.ui.cached_playable_hands = self.ui.game.fetch_all_playable_hands(self.ui.user)
        else:
            self.ui.cached_playable_hands = []

    def arrange_cards(self):
        if self.ui.is_paused:
            return

        for card in self.ui.user.get_hand().get_cards():
            card.selected = False

        self.ui.user.get_hand().sort()
        self.update_playable_hands()
        self.ui.render_manager.draw()

    def play_selected(self):
        if self.ui.is_paused:
            return

        if not self.ui.user.is_turn():
            return

        selected = self.ui.user.get_hand().get_selected_cards()

        if not selected:
            return

        success, message = self.ui.game.play_cards(selected)

        if success:
            combo = self.ui.game.current_combo
            if combo:
                self.ui.show_turn_message(f"You played {combo.combo_type}", 1000)
            else:
                self.ui.show_turn_message("You played!", 1000)

        if not success:
            user_cards = self.ui.user.hand.get_cards()
            lowest_user_card = min(user_cards) if user_cards else None

            game_state = {
                "current_combo": self.ui.game.current_combo,
                "is_first_game_turn": len(self.ui.game.played_cards_history) == 0,
                "lowest_card": lowest_user_card
            }

            tutorial_msg = self.ui.tutorial_controller.get_contextual_message(
                game_state, "invalid_play"
            )

            if tutorial_msg:
                full_error_msg = f"Oops! {message}. {tutorial_msg}"
                self.ui.tutorial_overlay.show(full_error_msg, dismissible=False)

            return

        if message and "chopped" in message:
            self.ui.show_chop_message(message)

        self.update_playable_hands()
        self.ui.render_manager.draw()

        if self.ui.check_game_over():
            return

        self.ui.tutorial_overlay.hide()
        self.ui.root.after(1200, self.ui.turn_manager.advance_turn)