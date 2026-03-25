class TutorialController:
    def __init__(self):
        # keep track of messages that we want to show ONCE
        self.seen_welcome = False
        self.seen_first_turn = False

    def get_contextual_message(self, game_state, event):
        # Game Start
        if event == "game_start" and not self.seen_welcome:
            self.seen_welcome = True
            return "Welcome to the game! You have 13 cards. Your goal is to be the first to play all of them."

        # User Turn 3 scenarios 
        elif event == "user_turn":
            is_first_game_turn = game_state.get("is_first_game_turn", False)
            current_combo = game_state.get("current_combo")
            
            # SCENARIO 1: User has 3 of Spade in the first turn
            if is_first_game_turn and not self.seen_first_turn:
                self.seen_first_turn = True
                lowest_card = game_state.get("lowest_card")
                return f"You get to go first! You must play a combination that includes your lowest card: the {lowest_card}."

            # SCENARIO 2: User won the last table has control on the turn
            if current_combo == None:
                return "It's your turn, you can play any combination :) "
            # SCENARIO 3: User must play the same combos to beat the table
            else:
                return "It's your turn, you must play the same kind of combination with higher value, you can look at some of the combos on the left"
        
        # User selecting an invalid play
        elif event == "invalid_play":
            return "You must play a different card."

        # Must Pass if user has no valid play
        elif event == "must_pass":
            return "It's your turn but you have no valid move, you have to pass :( "
        return None 