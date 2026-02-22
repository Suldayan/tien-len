def main():

    c1 = CARD(SUIT("Spades", 1, "♠"), RANK("THREE", 1, "3"))
    c2 = CARD(SUIT("Spades", 1, "♠"), RANK("FOUR", 2, "4"))
    c3 = CARD(SUIT("Spades", 1, "♠"), RANK("FIVE", 3, "5"))
    cards1 = [c1, c2, c3]
    print("test is_straight cards1:", is_straight(cards1))
    c4 = CARD(SUIT("Hearts", 4, "♥"), RANK("QUEEN", 10, "Q"))
    c5 = CARD(SUIT("Spades", 1, "♠"), RANK("QUEEN", 10, "Q"))
    c6 = CARD(SUIT("Diamonds", 3, "♦"), RANK("QUEEN", 10, "Q"))
    cards2 = [c4, c5, c6]
    print("test is_triple cards2:", is_triple(cards2))
    c7 = CARD(SUIT("Clubs", 2, "♣"), RANK("QUEEN", 10, "Q"))
    c8 = CARD(SUIT("Diamonds", 3, "♦"), RANK("QUEEN", 10, "Q"))
    cards3 = [c7, c8]
    print("test is_pair cards3:",is_pair(cards3))
    c9 = CARD(SUIT("Diamonds", 3, "♦"), RANK("QUEEN", 10, "Q"))
    c10 = CARD(SUIT("Clubs", 2, "♣"), RANK("QUEEN", 10, "Q"))
    c11 = CARD(SUIT("Spades", 1, "♠"), RANK("QUEEN", 10, "Q"))
    c12 = CARD(SUIT("Hearts", 4, "♥"), RANK("QUEEN", 10, "Q"))
    cards4 = [c9, c10, c11, c12]
    print("test is_four_of_a_kind cards4:",is_four_of_a_kind(cards4))
    c13 = CARD(SUIT("Spades", 1, "♠"), RANK("THREE", 1, "3"))
    c14 = CARD(SUIT("Spades", 1, "♠"), RANK("THREE", 1, "3"))
    c15 = CARD(SUIT("Spades", 1, "♠"), RANK("FOUR", 2, "4"))
    c16 = CARD(SUIT("Spades", 1, "♠"), RANK("FIVE", 3, "5"))
    cards5 = [c13, c14, c15, c16]
    print("test is_straight cards5:",is_straight(cards5))
    #let a1 = c17
    a1 = CARD(SUIT("Spades", 1, "♠"), RANK("THREE", 1, "3"))
    a2 = CARD(SUIT("Diamonds", 3, "♦"), RANK("THREE", 1, "3"))
    a3 = CARD(SUIT("Spades", 1, "♠"), RANK("FOUR", 2, "4"))
    a4 = CARD(SUIT("Diamonds", 3, "♦"), RANK("FOUR", 2, "4"))
    a5 = CARD(SUIT("Spades", 1, "♠"), RANK("FIVE", 3, "5"))
    a6 = CARD(SUIT("Diamonds", 3, "♦"), RANK("FIVE", 3, "5"))
    cards6 = [a1, a2, a3, a4, a5, a6]
    print("test is_double_straight cards6:",is_double_straight(cards6))
    b1 = CARD(SUIT("Spades", 1, "♠"), RANK("QUEEN", 10, "Q"))
    b2 = CARD(SUIT("Diamonds", 3, "♦"), RANK("THREE", 1, "3"))
    b3 = CARD(SUIT("Spades", 1, "♠"), RANK("FOUR", 2, "4"))
    b4 = CARD(SUIT("Diamonds", 3, "♦"), RANK("FOUR", 2, "4"))
    b5 = CARD(SUIT("Spades", 1, "♠"), RANK("FIVE", 3, "5"))
    b6 = CARD(SUIT("Diamonds", 3, "♦"), RANK("FIVE", 3, "5"))
    cards7 = [b1, b2, b3, b4, b5, b6]
    print("test is_double_straight cards7:",is_double_straight(cards7))
    comboHand1 = make_combo(cards6)
    print("test combo type comboHand1",comboHand1.combo_type)
    print("test length comboHand1", comboHand1.length)
    comboHand2 = make_combo(cards4)
    print("test combo type comboHand2",comboHand2.combo_type)
    print("test length comboHand2",comboHand2.length)
    
# OUTPUT
# test is_straight cards1: True
# test is_triple cards2: True
# test is_pair cards3: True
# test is_four_of_a_kind cards4: True
# test is_straight cards5: False
# test is_double_straight cards6: True
# test is_double_straight cards7: False
# test combo type comboHand1 DOUBLE_STRAIGHT
# test length comboHand1 6
# test combo type comboHand2 FOUR_OF_A_KIND
# test length comboHand2 4