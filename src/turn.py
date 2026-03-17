class TurnManager:
    def __init__(self, ui):
        self.ui = ui

    #since pass_turn was under ui class, we need to create a new class for pass_turn then we put it in turn.py

    def pass_turn(self):
        if not self.ui.user.is_turn():
            return

        self.ui.game.pass_turn()
        self.ui.draw()

        if self.ui.check_game_over():
            return

        self.ui.root.after(800, self.ui.turn_manager.advance_turn)

    def bot_turn(self):
        if not self.ui.bot.is_turn() or self.ui.game.is_game_over():
            return

        selected_cards = self.ui.bot.make_move(self.ui.game)

        if selected_cards:
            success, message = self.ui.game.play_cards(selected_cards)
            if message and "chopped" in message:
                self.ui.show_chop_message(message)
        else:
            self.ui.game.pass_turn()

        self.ui.update_playable_hands()
        self.ui.draw() 
        if self.ui.check_game_over():
            return
        self.ui.root.after(800, self.ui.turn_manager.advance_turn)

    def advance_turn(self):
        """Single choke point: decides what happens after any play or pass."""
        if self.ui.game.is_game_over():
            self.ui.handle_game_over()
            return

        current = self.ui.game.current_player()

        #refresh hint when turn changes
        self.ui.update_playable_hands()
        self.ui.draw()

        if current == self.ui.user:
            if len(self.ui.cached_playable_hands) == 0:
                self.ui.root.after(800, lambda: self.ui.auto_pass(current))
        elif current == self.ui.bot:
            self.ui.root.after(800, self.ui.turn_manager.bot_turn)

    def auto_pass(self, player):
        """Automatically passes for any player with no valid moves."""
        if not player.is_turn() or player == self.ui.user:
            return

        print(f"{player.get_name()} has no valid move. Auto pass.")
        self.ui.game.pass_turn()
        self.ui.update_playable_hands()
        self.ui.draw()
        self.ui.root.after(800, self.ui.turn_manager.advance_turn)