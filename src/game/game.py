#the reason that game.py uses helper function is because game.py only do one thing
#in ui.py, using class is much more cleaner since each class has a specific job
import itertools
from src.core.player import Player
from src.core.combo import Combo
from src.game.validateplay import can_play as can_play_impl
from src.game.round import start_new_round as start_new_round_impl
from src.game.round import pass_turn as pass_turn_impl
from src.game.round import next_turn as next_turn_impl
from src.game.round import round_results as round_results_impl
from src.game.round import end_match as end_match_impl

class Game:
    def __init__(self, players: list[Player]):
        self.players = players
        self.current_index = 0

        self.round_number = 1
        self.current_combo = None      # last played combo on the table
        self.played_cards_history = [] # A history of all played cards done by all active players.
        self.passed = set()            # player indices who passed this round
        self.last_player_index = None
        self.first_move_of_match = True
        self.required_card = None

    def set_first_turn(self):

        # force everyone to false first:
        for player in self.players:
            player.set_turn(False)
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

                self.required_card = players_lowest
                self.first_move_of_match = True

                print(f"Starter found: {player.get_name()} has the 3 of Spades!")
                return

            # If 3 of spades is not available, keep track of who has the overall lowest card
            if absolute_lowest_card is None or players_lowest < absolute_lowest_card:
                absolute_lowest_card = players_lowest
                player_with_lowest = i

        # If we get here, no one had the 3 of Spades
        if player_with_lowest is not None:
            self.current_index = player_with_lowest
            self.players[self.current_index].set_turn(True)

            self.required_card = absolute_lowest_card
            self.first_move_of_match = True
            print(f"No 3 of Spades. {self.players[self.current_index].get_name()} starts with {absolute_lowest_card}")
        else:
            self.required_card = None
            self.first_move_of_match = False

        

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

    # def get_all_subsets(self, cards, current=[], start=0, results=[]):
    #     if len(current) > 0:
    #         results.append(list(current))
    #     for i in range(start, len(cards)):
    #         current.append(cards[i])
    #         self.get_all_subsets(cards, current, i + 1, results)
    #         current.pop()
    #     return results

    # def fetch_all_playable_hands(self, player):  
    #     cards = player.hand.get_cards()
    #     playable_hands = []
    #     all_subsets = self.get_all_subsets(cards, [], 0, [])
    #     for subset in all_subsets:
    #         combo = player.hand.make_combo(subset)
    #         if combo is not None and self.can_play(combo):
    #             playable_hands.append(combo)
    #     return playable_hands
     
    # to make this function more efficient I just combine them and use itertools
    def fetch_all_playable_hands(self, player):  
        cards = player.hand.get_cards()
        playable_hands = []
        
        # find out which subset sizes we actually need to check
        sizes_to_check = []
        if self.current_combo is None:
            # must check all possible sizes 
            sizes_to_check = range(1, len(cards) + 1)
        else:
            # must match the number of cards on the table
            table_size = len(self.current_combo.cards)
            sizes_to_check.append(table_size)
            
            # adding any sizes that could be a Chop: (Bombs/Consecutive Pairs)
            # 4 of a kind (4), 3pairs (6), 4pairs (8)
            for chop_size in [4, 6, 8]:
                if chop_size not in sizes_to_check and chop_size <= len(cards):
                    sizes_to_check.append(chop_size)

        # Use C optimized itertools to get only those specific sizes
        for size in sizes_to_check:
            for subset in itertools.combinations(cards, size):
                # itertools return a tuple => convert it to a list
                combo = player.hand.make_combo(list(subset))
                if combo is not None and self.can_play(combo):

                    #the combo must contain the lowest card
                    if self.first_move_of_match and self.required_card is not None:
                        if self.required_card in combo.cards:
                            playable_hands.append(combo)
                    else:
                        # If not first move OR no card required, all valid combos allowed
                        playable_hands.append(combo)
                                        
        return playable_hands

    def has_valid_move(self, player):
        #reuse function fetch_all_playable_hands since these 2 are very similar
        return len(self.fetch_all_playable_hands(player)) > 0

    def play_cards(self, selected_cards):
    
        #selected_cards: list of CARD objects that current player wants to play

        #Returns (True, message) if played, else (False, reason)
        player = self.current_player()

        # enforces player to start with a combination including the lowest card
        if self.first_move_of_match:
            if self.required_card not in selected_cards:
                return False, f"First move must include {self.required_card}"

        combo = player.hand.make_combo(selected_cards)  # use Hand.make_combo -> Combo.make_combo
        if combo is None:
            return False, "Invalid combo"

        if not self.can_play(combo):
            return False, "Combo does not beat the current table"
        
        self.first_move_of_match = False

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
        if self.last_player_index is not None:
            opponent = self.players[self.last_player_index]
        else:
            return None

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
    #def end_match(self): is now in round.py
    def end_match(self):
        return end_match_impl(self)

    #def round_results(self): is now in round.py
    def round_results(self):
        return round_results_impl(self)
    
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