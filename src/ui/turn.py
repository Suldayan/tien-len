class TurnManager:
    def __init__(self, ui):
        self.ui = ui

    def pass_turn(self):
        if self.ui.is_paused == True:
            return

        if not self.ui.user.is_turn():
            return

        self.ui.game.pass_turn()
        self.ui.show_turn_message("You passed!", 1000)
        self.ui.render_manager.draw()

        if self.ui.check_game_over():
            return
            
        self.ui.tutorial_overlay.hide()
        self.ui.root.after(300, self.advance_turn)

    def bot_turn(self):
        if self.ui.is_paused == True:
            return

        if not self.ui.bot.is_turn() or self.ui.game.is_game_over():
            return

        selected_cards = self.ui.bot.make_move(self.ui.game)

        if selected_cards:
            success, message = self.ui.game.play_cards(selected_cards)
            combo = self.ui.game.current_combo
            if message and "chopped" in message:
                self.ui.show_chop_message(message)
            if combo:
                msg = f"Bot played {combo.combo_type}"
            else:
                msg = "Bot played"
            self.ui.show_turn_message(msg, 1200)
        else:
            self.ui.game.pass_turn()
            self.ui.show_turn_message("Bot passed", 1200)

        self.ui.update_playable_hands()
        self.ui.render_manager.draw() 
        if self.ui.check_game_over():
            return
        self.ui.root.after(300, self.advance_turn)

    def advance_turn(self):
        if self.ui.is_paused == True:
            return
        """Single choke point: decides what happens after any play or pass."""
        if self.ui.game.is_game_over():
            self.ui.handle_game_over()
            return

        current = self.ui.game.current_player()

        def show_turn():
            # Show turn message
            if current == self.ui.user:
                self.ui.show_turn_message("Your turn")
            elif current == self.ui.bot:
                self.ui.show_turn_message("Bot's turn...")

        self.ui.root.after(800, show_turn)

        #refresh hint when turn changes
        self.ui.update_playable_hands()
        self.ui.render_manager.draw()

        if current == self.ui.user:
            self.ui.check_turn_tutorial()
        elif current == self.ui.bot:
            self.ui.root.after(1200, self.bot_turn)

    # def auto_pass(self, player):
    #     """Automatically passes for bots with no valid moves."""
    #     if not player.is_turn() or player == self.ui.user:
    #         return

    #     print(f"{player.get_name()} has no valid move. Auto pass.")
    #     self.ui.game.pass_turn()
    #     self.ui.update_playable_hands()
    #     self.ui.render_manager.draw()
    #     self.ui.root.after(800, self.advance_turn)