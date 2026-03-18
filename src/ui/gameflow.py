class GameFlow:
    def __init__(self, ui):
        self.ui = ui

    def reset_game(self):
        self.ui.game.reset(self.ui.deck)
        self.ui.update_playable_hands()
        self.ui.render_manager.draw()
        if self.ui.bot.is_turn():
            self.ui.root.after(800, self.ui.turn_manager.bot_turn)

    def continue_match(self, popup):
        popup.destroy()

        #reset deck and deal new cards but still carry over prev points
        self.ui.deck.reset()
        self.ui.deck.shuffle()

        for player in self.ui.game.players:
            player.hand.set_cards(self.ui.deck.deal(13))
            player.set_turn(False)

        self.ui.game.current_combo = None
        self.ui.game.passed.clear()
        self.ui.game.played_cards_history = []
        self.ui.game.last_player_index = None
        self.ui.game.round_number += 1

        self.ui.game.set_first_turn()

        self.ui.render_manager.draw()

        if self.ui.bot.is_turn():
            self.ui.root.after(800, self.ui.turn_manager.bot_turn)

    def new_game(self, popup):
        popup.destroy()
        self.reset_game()
