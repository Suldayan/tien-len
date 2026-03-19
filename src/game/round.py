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

def pass_turn(game):
    """Current player passes. If everyone else passed, new round starts."""
    game.passed.add(game.current_index)

    # If all ative players have passed except the last player who played, we reset the table.
    active = [i for i, p in enumerate(game.players) if len(p.hand.get_cards()) > 0]

    #fixed : The round ends when all bots passed except the player 
    if len(game.passed) >= len(active) - 1:
        game.start_new_round(starter_index=game.last_player_index)
    else:
        game.next_turn()

def next_turn(game):
    #switch turn to the next player who hasn't already won.
    game.current_player().set_turn(False)

    n = len(game.players)
    for _ in range(n):
        #get index of current player
        game.current_index = (game.current_index + 1) % n
        #skip players who have no cards (they already finished)
        if len(game.players[game.current_index].hand.get_cards()) > 0:
            break

    game.players[game.current_index].set_turn(True)