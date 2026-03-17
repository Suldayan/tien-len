from src.player import Player
from src.combo import Combo

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

        # If all ative players have passed except the last player who played, we reset the table.
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
        You can expand this later for Tien Len rules (bombs, 2, etc.).
        """
        #win instanly if you have 6 pair
        #win instanly if you have 12/13 cards that are all red/black

        #Win instanly if you play all 2s
        #if (combo.combo_type in ["FOUR_OF_A_KIND"] 
        #and combo.cards[0].rank.value == 13
        #):
        #    return True #and win the game

        if self.current_combo is None: #pot is empty
            return True

        #Any 4 of a kind beats 2 
        if (combo.combo_type in ["FOUR_OF_A_KIND"] 
        and self.current_combo.combo_type in ["SINGLE"] 
        and self.current_combo.cards[0].rank.value == 13
        ):
            return True

        #double straight beats 2
        if (combo.combo_type in ["DOUBLE_STRAIGHT"]
        and self.current_combo.combo_type in ["SINGLE"] 
        and self.current_combo.cards[0].rank.value == 13
        ):
            return True

        #4 pair of double straight can beat 2 2
        if (combo.combo_type in ["DOUBLE_STRAIGHT"] 
        and combo.length == 8 
        and self.current_combo.combo_type in ["PAIR"]
        and self.current_combo.cards[0].rank.value == 13 
        ):
            return True

        #5 pair of double straight can beat 2 2 2
        if (combo.combo_type in ["DOUBLE_STRAIGHT"] 
        and combo.length == 10 
        and self.current_combo.combo_type in ["TRIPLE"]
        and self.current_combo.cards[0].rank.value == 13
        ):
            return True

        #this condition has already been check in play_cards()
        #if combo is None: 
            #return False

        if combo.combo_type != self.current_combo.combo_type: #check if they are the same type
            return False

        if combo.combo_type in ["STRAIGHT", "DOUBLE_STRAIGHT"] and combo.length != self.current_combo.length:
            return False
            
        player_strongest_card = max(combo.cards, key=lambda c: c.strength())
        pot_strongest_card = max(self.current_combo.cards, key=lambda c: c.strength())

        return player_strongest_card.strength() > pot_strongest_card.strength()
    
    def get_all_subsets(self, cards, current=[], start=0, results=[]):
        if len(current) > 0:
            results.append(list(current))
        for i in range(start, len(cards)):
            current.append(cards[i])
            self.get_all_subsets(cards, current, i + 1, results)
            current.pop()
        return results

    """ Use this function for the UI Buzz """
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
        self.handle_two_chop(combo, player)

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
        return True, "Played successfully"
    
    def handle_two_chop(self, new_combo, player):
        if not self.current_combo:
            return
        
        prev_combo = self.current_combo
        prev_cards = prev_combo.cards

        #Check if previous combo contains 2s?
        twos = []
        for card in prev_cards:
            if card.rank.label == "2":
                twos.append(card)

        num_twos = len(twos)

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
            print(f"{player.get_name()} chopped {num_twos} two(s)! +{penalty} points")

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
                    
