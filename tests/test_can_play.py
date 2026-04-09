from src.core.card import CARD
from src.core.suit import SUIT
from src.core.rank import RANK
from src.core.combo import Combo
from src.core.combo import make_combo
def can_play(pot, combo: Combo):
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

        if pot is None: #pot is empty
            return True

        #Any 4 of a kind beats 2, check
        if (combo.combo_type in ["FOUR_OF_A_KIND"] 
        and pot.combo_type in ["SINGLE"] 
        and pot.cards[0].rank.value == 13
        ):
            print("Any 4 of a kind beats 2")
            return True

        #double straight beats 2, check
        if (combo.combo_type in ["DOUBLE_STRAIGHT"]
        and pot.combo_type in ["SINGLE"] 
        and pot.cards[0].rank.value == 13
        ):
            print("Any double straight beats 2")
            return True

        #4 pair of double straight can beat 2 2, check
        if (combo.combo_type in ["DOUBLE_STRAIGHT"] 
        and combo.length == 8 
        and pot.combo_type in ["PAIR"]
        and pot.cards[0].rank.value == 13 
        ):
            print("4 pair of double straight can beat 2 2")
            return True

        #5 pair of double straight can beat 2 2 2 check
        if (combo.combo_type in ["DOUBLE_STRAIGHT"] 
        and combo.length == 10 
        and pot.combo_type in ["TRIPLE"]
        and pot.cards[0].rank.value == 13
        ):
            print("5 pair of double straight can beat 2 2 2")
            return True

        #this condition has already been check in play_cards()
        #if combo is None: 
            #return False

        if combo.combo_type != pot.combo_type: #check if they are the same type
            return False

        if combo.combo_type in ["STRAIGHT", "DOUBLE_STRAIGHT"] and combo.length != pot.length:
            print("The length are not the same") #check
            return False

        
        def card_strength(c):
            return (c.rank.value, c.suit.SuitRank) #compare rank first, then compare suit

        #Find the strongest card that the player selected 
        player_strongest_card = max(combo.cards, key=card_strength) 
        #Find the strongest card in the pot
        pot_strongest_card = max(pot.cards, key=card_strength)

        # Compare their tuple values directly
        return card_strength(player_strongest_card) > card_strength(pot_strongest_card)
def main():
    """
    To run the test, make sure you are in the project root directory (TienLen).
    On Windows:
        python -m tests.test_can_play
    On macOS / Linux:
        python3 -m tests.test_can_play
    """


    #test pot = 2, player = four of a kind
    c2 = CARD(SUIT("Spades", 1, "♠"), RANK("TWO", 13, "2"))
    cards1 = [c2]
    SINGLE_TWO_POT = make_combo(cards1)
    c9 = CARD(SUIT("Diamonds", 3, "♦"), RANK("QUEEN", 10, "Q"))
    c10 = CARD(SUIT("Clubs", 2, "♣"), RANK("QUEEN", 10, "Q"))
    c11 = CARD(SUIT("Spades", 1, "♠"), RANK("QUEEN", 10, "Q"))
    c12 = CARD(SUIT("Hearts", 4, "♥"), RANK("QUEEN", 10, "Q"))
    cards4 = [c9, c10, c11, c12]
    FOUR_OF_A_KIND_PLAYER = make_combo(cards4)
    #can_play(pot, player)
    can_play(SINGLE_TWO_POT, FOUR_OF_A_KIND_PLAYER)

    #test pot = 2 2 2, player = 5 pairs of double straight
    e1 = CARD(SUIT("Spades", 1, "♠"), RANK("TWO", 13, "2"))
    e2 = CARD(SUIT("Clubs", 2, "♣"), RANK("TWO", 13, "2"))
    e3 = CARD(SUIT("Diamonds", 3, "♦"), RANK("TWO", 13, "2"))
    cards11 = [e1, e2, e3]
    f1 = CARD(SUIT("Spades", 1, "♠"), RANK("NINE", 7, "9"))
    f2 = CARD(SUIT("Diamonds", 3, "♦"), RANK("NINE", 7, "9"))
    f3 = CARD(SUIT("Spades", 1, "♠"), RANK("TEN", 8, "10"))
    f4 = CARD(SUIT("Diamonds", 3, "♦"), RANK("TEN", 8, "10"))
    f5 = CARD(SUIT("Spades", 1, "♠"), RANK("JACK", 9, "J"))
    f6 = CARD(SUIT("Diamonds", 3, "♦"), RANK("JACK", 9, "J"))
    f7 = CARD(SUIT("Spades", 1, "♠"), RANK("QUEEN", 10, "Q"))
    f8 = CARD(SUIT("Diamonds", 3, "♦"), RANK("QUEEN", 10, "Q"))
    f9 = CARD(SUIT("Spades", 1, "♠"), RANK("KING", 11, "K"))
    f10 = CARD(SUIT("Diamonds", 3, "♦"), RANK("KING", 11, "K"))
    cards12 = [f1, f2, f3, f4, f5, f6, f7, f8, f9, f10]
    THREE_OF_A_KIND_TWO_POT = make_combo(cards11)
    FIVE_PAIRS_OF_DOUBLE_STRAIGHT_PLAY = make_combo(cards12)
    can_play(THREE_OF_A_KIND_TWO_POT, FIVE_PAIRS_OF_DOUBLE_STRAIGHT_PLAY)
    
    #test pot = 2 2, player = 4 pair of double straight
    p1 = CARD(SUIT("Spades", 1, "♠"), RANK("TWO", 13, "2"))
    p2 = CARD(SUIT("Diamonds", 3, "♦"), RANK("TWO", 13, "2"))
    cards13 = [p1, p2]
    PAIR_OF_TWO_POT = make_combo(cards13)
    o1 = CARD(SUIT("Spades", 1, "♠"), RANK("NINE", 7, "9"))
    o2 = CARD(SUIT("Diamonds", 3, "♦"), RANK("NINE", 7, "9"))
    o3 = CARD(SUIT("Spades", 1, "♠"), RANK("TEN", 8, "10"))
    o4 = CARD(SUIT("Diamonds", 3, "♦"), RANK("TEN", 8, "10"))
    o5 = CARD(SUIT("Spades", 1, "♠"), RANK("JACK", 9, "J"))
    o6 = CARD(SUIT("Diamonds", 3, "♦"), RANK("JACK", 9, "J"))
    o7 = CARD(SUIT("Spades", 1, "♠"), RANK("QUEEN", 10, "Q"))
    o8 = CARD(SUIT("Diamonds", 3, "♦"), RANK("QUEEN", 10, "Q"))
    cards14 = [o1, o2, o3, o4, o5, o6, o7, o8]
    FOUR_PAIR_OF_DOUBLE_STRAIGHT_PLAYER = make_combo(cards14)
    can_play(PAIR_OF_TWO_POT, FOUR_PAIR_OF_DOUBLE_STRAIGHT_PLAYER)
    #test pot = 3 3, 4 4, 5 5, player = J J, Q Q, K K
    a1 = CARD(SUIT("Spades", 1, "♠"), RANK("THREE", 1, "3"))
    a2 = CARD(SUIT("Diamonds", 3, "♦"), RANK("THREE", 1, "3"))
    a3 = CARD(SUIT("Spades", 1, "♠"), RANK("FOUR", 2, "4"))
    a4 = CARD(SUIT("Diamonds", 3, "♦"), RANK("FOUR", 2, "4"))
    a5 = CARD(SUIT("Spades", 1, "♠"), RANK("FIVE", 3, "5"))
    a6 = CARD(SUIT("Diamonds", 3, "♦"), RANK("FIVE", 3, "5"))
    cards6 = [a1, a2, a3, a4, a5, a6]
    b1 = CARD(SUIT("Spades", 1, "♠"), RANK("JACK", 9, "J"))
    b2 = CARD(SUIT("Diamonds", 3, "♦"), RANK("JACK", 9, "J"))
    b3 = CARD(SUIT("Spades", 1, "♠"), RANK("QUEEN", 10, "Q"))
    b4 = CARD(SUIT("Diamonds", 3, "♦"), RANK("QUEEN", 10, "Q"))
    b5 = CARD(SUIT("Spades", 1, "♠"), RANK("KING", 11, "K"))
    b6 = CARD(SUIT("Diamonds", 3, "♦"), RANK("KING", 11, "K"))
    cards7 = [b1, b2, b3, b4, b5, b6]
    DOUBLE_STRAIGHT_POT = make_combo(cards6) #lower
    DOUBLE_STRAIGHT_PLAY = make_combo(cards7) #higher
    #can_play(pot, player)
    print(can_play(DOUBLE_STRAIGHT_POT, DOUBLE_STRAIGHT_PLAY))
    d1 = CARD(SUIT("Spades", 1, "♠"), RANK("JACK", 9, "J"))
    d2 = CARD(SUIT("Spades", 1, "♠"), RANK("QUEEN", 10, "Q"))
    d3 = CARD(SUIT("Diamonds", 3, "♦"), RANK("KING", 11, "K"))
    cards8 = [d1, d2, d3]
    d4 = CARD(SUIT("Spades", 1, "♠"), RANK("NINE", 7, "9"))
    d5 = CARD(SUIT("Spades", 1, "♠"), RANK("TEN", 8, "10"))
    d6 = CARD(SUIT("Spades", 1, "♠"), RANK("JACK", 9, "J"))
    d7 = CARD(SUIT("Spades", 1, "♠"), RANK("QUEEN", 10, "Q"))
    cards9 = [d4, d5, d6, d7]
    STRAIGHT_PLAYER = make_combo(cards8)
    STRAIGHT_POT = make_combo(cards9)
    can_play(STRAIGHT_POT, STRAIGHT_PLAYER)
if __name__ == "__main__":
    main()