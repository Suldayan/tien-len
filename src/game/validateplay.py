#change from self to game obj
def can_play(game, combo):
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

    if game.current_combo is None: #pot is empty
        return True

    #Any 4 of a kind beats 2 
    if (combo.combo_type in ["FOUR_OF_A_KIND"] 
    and game.current_combo.combo_type in ["SINGLE"] 
    and game.current_combo.cards[0].rank.value == 13
    ):
        return True

    #double straight beats 2
    if (combo.combo_type in ["DOUBLE_STRAIGHT"]
    and game.current_combo.combo_type in ["SINGLE"] 
    and game.current_combo.cards[0].rank.value == 13
    ):
        return True

    #4 pair of double straight can beat 2 2
    if (combo.combo_type in ["DOUBLE_STRAIGHT"] 
    and combo.length == 8 
    and game.current_combo.combo_type in ["PAIR"]
    and game.current_combo.cards[0].rank.value == 13 
    ):
        return True

    #5 pair of double straight can beat 2 2 2
    if (combo.combo_type in ["DOUBLE_STRAIGHT"] 
    and combo.length == 10 
    and game.current_combo.combo_type in ["TRIPLE"]
    and game.current_combo.cards[0].rank.value == 13
    ):
        return True

    if combo.combo_type != game.current_combo.combo_type: #check if they are the same type
        return False

    if combo.combo_type in ["STRAIGHT", "DOUBLE_STRAIGHT"] and combo.length != game.current_combo.length:
        return False
            
    player_strongest_card = max(combo.cards, key=lambda c: c.strength())
    pot_strongest_card = max(game.current_combo.cards, key=lambda c: c.strength())

    return player_strongest_card.strength() > pot_strongest_card.strength()