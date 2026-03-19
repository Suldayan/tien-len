def start_new_round(game, starter_index=None):
    #Clears the table and resets passes.
    #The last player who successfully played starts the new round.
    
    game.round_number += 1
    game.current_combo = None
    game.passed.clear()

    # If no starter given, use last player
    if starter_index is None:
        starter_index = game.last_player_index

    # Safety check
    if starter_index is None:
        return

    # switch turn
    game.players[game.current_index].set_turn(False)
    game.current_index = starter_index
    game.players[game.current_index].set_turn(True)