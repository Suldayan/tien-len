#the reason that game.py uses helper function is because game.py only do one thing
#in ui.py, using class is much more cleaner since each class has a specific job
from src.player import Player
from src.combo import Combo
from src.game.validateplay import can_play as can_play_impl
from src.game.round import start_new_round as start_new_round_impl
from src.game.round import pass_turn as pass_turn_impl
from src.game.round import next_turn as next_turn_impl

class Game:
    def __init__(self, players: list[Player]):
        self.players = players
        self.current_index = 0

        self.round_number = 1
        self.current_combo = None      # last played combo on the table
        self.played_cards_history = [] # A history of all played cards done by all active players.
        self.passed = set()            # player indices who passed this round
        self.last_player_index = None
        self.set_first_turn()

    def set_first_turn(self):
        # Initialize variables to track the absolute lowest card found across all players
        absolute_lowest_card = None
        player_with_lowest = None

        for i, player in enumerate(self.players):
            # Sort the player's hand to find their specific lowest card
            player_cards = player.hand.get_cards()
            if not player_cards:
                continue
                
            players_lowest = min(player_cards)

            if players_lowest.rank.label == "3" and players_lowest.suit.name == "Spades":
                self.current_index = i
                player.set_turn(True)
                print(f"Starter found: {player.get_name()} has the 3 of Spades!")
                return

            # If 3 of spades is not available, keep track of who has the overall lowest card
            if absolute_lowest_card is None or players_lowest < absolute_lowest_card:
                absolute_lowest_card = players_lowest
                player_with_lowest = i

        # If we get here, no one had the 3 of Spades
        self.current_index = player_with_lowest
        self.players[self.current_index].set_turn(True)
        print(f"No 3 of Spades. {self.players[self.current_index].get_name()} starts with {absolute_lowest_card}")

    #turn helpers 
    def current_player(self):
       #self.fetch_all_playable_hands(self.players[self.current_index]) is being called in draw function in ui.py
        return self.players[self.current_index]

    #def next_turn(self): is now in round.py
    def next_turn(self):
        return next_turn_impl(self)

    #round helpers
    #def start_new_round(self, starter_index=None): is now in round.py
    def start_new_round(self, starter_index=None):
        return start_new_round_impl(self, starter_index=None)

    #def pass_turn(self): is now in round.py
    def pass_turn(self):
        return pass_turn_impl(self)

    # --- play logic ---
    #def can_play(self, combo): is now in validateplay.py
    def can_play(self, combo):
        return can_play_impl(self, combo)

    def get_all_subsets(self, cards, current=[], start=0, results=[]):
        if len(current) > 0:
            results.append(list(current))
        for i in range(start, len(cards)):
            current.append(cards[i])
            self.get_all_subsets(cards, current, i + 1, results)
            current.pop()
        return results

    def fetch_all_playable_hands(self, player):  
        cards = player.hand.get_cards()
        playable_hands = []
        all_subsets = self.get_all_subsets(cards, [], 0, [])
        for subset in all_subsets:
            combo = player.hand.make_combo(subset)
            if combo is not None and self.can_play(combo):
                playable_hands.append(combo)
        return playable_hands

    def has_valid_move(self, player):
        #reuse function fetch_all_playable_hands since these 2 are very similar
        return len(self.fetch_all_playable_hands(player)) > 0

    def play_cards(self, selected_cards):
    
        #selected_cards: list of CARD objects that current player wants to play

        #Returns (True, message) if played, else (False, reason)
        player = self.current_player()

        combo = player.hand.make_combo(selected_cards)  # use Hand.make_combo -> Combo.make_combo
        if combo is None:
            return False, "Invalid combo"

        if not self.can_play(combo):
            return False, "Combo does not beat the current table"

        # Add hand to play into history
        self.played_cards_history.append(combo)
        print(f"Added combo: {combo} into history")

        #Check chop scoring before updating combo
        chop_message = self.handle_two_chop(combo, player)

        # remove cards from player's hand
        for c in selected_cards:
            c.selected = False
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

        if chop_message:
            return True, chop_message
        
        return True, "Played successfully"
    
    def handle_two_chop(self, new_combo, player):
        if not self.current_combo:
            return
        
        prev_cards = self.current_combo.cards

        #Check if previous combo contains 2s?
        twos = []
        for card in prev_cards:
            if card.rank.label == "2":
                twos.append(card)

        num_twos = len(twos)
        if num_twos == 0:
            return None
        if num_twos == 1:
            text = "a 2"
        elif num_twos == 2:
            text = "a pair of 2s"
        else:
            text = "triple 2s"

        #Only bomb can chop '2'
        if new_combo.combo_type not in ["FOUR_OF_A_KIND", "DOUBLE_STRAIGHT"]:
            return None

        #Find the one who played the 2 (called opponent)
        #Only work for 1 bot + player!!!
        opponent = None
        for p in self.players:
            if p != player:
                opponent = p
                break

        #Determine score change:
        penalty = num_twos * 20
        if penalty > 0:
            opponent.set_points(opponent.get_points() - penalty)
            player.set_points(player.get_points() + penalty)
            chop_message = f"{player.get_name()} chopped {text}! +{penalty} points"
        return chop_message

    def is_game_over(self):
        """Game ends when only 0 or 1 players still have cards."""
        active = sum(1 for p in self.players if len(p.hand.get_cards()) > 0)
        return active <= 1
    
    #Called when game's over. Updates points + returns winner
    def end_match(self):
        winner = None
        losers = []

        for player in self.players:
            if len(player.hand.get_cards()) == 0:
                winner = player
            else:
                losers.append(player)

        if winner:
            for loser in losers:
                remaining = len(loser.hand.get_cards())
                winner.points += remaining * 10
                loser.points -= remaining * 10

        return winner

    def round_results(self):
        winner = self.end_match()
        lines = []
        lines.append(f"Congratulations, {winner.get_name()}! You win :)" if winner else "Game Over")
        lines.append("")
        for player in self.players:
            lines.append(f"{player.get_name()}: {player.get_points()} pts")
        return "\n".join(lines)
    
    def reset(self, deck):
        deck.reset()
        deck.shuffle()

        for player in self.players:
            player.hand.set_cards(deck.deal(13))
            player.set_turn(False)
            player.set_points(0)

        self.current_combo = None
        self.passed.clear()
        self.played_cards_history = []
        self.last_player_index = None
        self.round_number = 1
        self.set_first_turn()