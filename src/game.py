class Game:
    def __init__(self, players):
        self.players = players
        self.current_index = 0

        self.round_number = 1
        self.current_combo = None      # last played combo on the table
        self.passed = set()            # player indices who passed this round
        self.last_player_index = None

        # TODO: may be removed as the Player class by default already sets turn to False.
        #set first player's turn
        for p in self.players:
            p.set_turn(False)
        self.players[self.current_index].set_turn(True)

    #turn helpers 
    def current_player(self):
        return self.players[self.current_index]

    def next_turn(self):
        #switch turn to the next player who hasn't already won.
        self.current_player().set_turn(False)

        n = len(self.players)
        for _ in range(n):
            #get index of current player
            self.current_index = (self.current_index + 1) % n
            #skip players who have no cards (they already finished)
            if len(self.players[self.current_index].hand.get_cards()) > 0:
                break

        self.players[self.current_index].set_turn(True)

    #round helpers
    def start_new_round(self, starter_index=None):
        #Clears the table and resets passes.
        #The last player who successfully played starts the new round.
    
        self.round_number += 1
        self.current_combo = None
        self.passed.clear()

        # If no starter given, use last player
        if starter_index is None:
            starter_index = self.last_player_index

        # Safety check
        if starter_index is None:
            return

        # switch turn
        self.players[self.current_index].set_turn(False)
        self.current_index = starter_index
        self.players[self.current_index].set_turn(True)

    def pass_turn(self):
        """Current player passes. If everyone else passed, new round starts."""
        self.passed.add(self.current_index)

        # If all *active* players (with cards) have passed except the last player who played,
        # we reset the table.
        active = [i for i, p in enumerate(self.players) if len(p.hand.get_cards()) > 0]

        #fixed : The round ends when all bots passed except the player 
        if len(self.passed) >= len(active) - 1:
            self.start_new_round(starter_index=self.last_player_index)
        else:
            self.next_turn()

    # --- play logic ---
    def can_play(self, combo):
        """
        Very basic rule:
        - If table is empty: any valid combo can be played
        - Otherwise: must match type and (for straight) length, and have higher top rank
        expand this later for Tien Len rules (bombs, 2, etc.).
        """
        if combo is None:
            return False

        if self.current_combo is None:
            return True

        if combo.combo_type != self.current_combo.combo_type:
            return False

        if combo.combo_type in ["STRAIGHT"] and combo.length != self.current_combo.length:
            return False
        
        #fixed: 
        def card_strength(c):
            return (c.rank.value, c.suit.SuitRank)

        # Find the strongest card in the new combo and the old combo
        new_strongest_card = max(combo.cards, key=card_strength)
        old_strongest_card = max(self.current_combo.cards, key=card_strength)

        # Compare their tuple values directly
        return card_strength(new_strongest_card) > card_strength(old_strongest_card)

    def play_cards(self, selected_cards):
        """
        selected_cards: list of CARD objects that current player wants to play

        Returns (True, message) if played, else (False, reason)
        """
        player = self.current_player()

        combo = player.hand.make_combo(selected_cards)  # use Hand.make_combo -> Combo.make_combo
        if combo is None:
            return False, "Invalid combo"

        if not self.can_play(combo):
            return False, "Combo does not beat the current table"

        # remove cards from player's hand
        for c in selected_cards:
            player.hand.remove(c)

        # update table + reset passes (new action happened)
        self.current_combo = combo
        self.passed.clear()

        #fixed: records the player that own the current table
        self.last_player_index = self.current_index

        # if player finished, game might be over
        if len(player.hand.get_cards()) == 0:
            return True, f"{player.get_name()} finished!"

        self.next_turn()
        return True, "Played successfully"

    def is_game_over(self):
        """Game ends when only 0 or 1 players still have cards."""
        active = sum(1 for p in self.players if len(p.hand.get_cards()) > 0)
        return active <= 1