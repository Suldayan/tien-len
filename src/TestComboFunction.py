def main():

    c1 = CARD(SUIT("Spades", 1, "♠"), RANK("THREE", 1, "3"))
    c2 = CARD(SUIT("Spades", 1, "♠"), RANK("FOUR", 2, "4"))
    c3 = CARD(SUIT("Spades", 1, "♠"), RANK("FIVE", 3, "5"))
    cards1 = [c1, c2, c3]
    print(is_straight(cards1))
    c4 = CARD(SUIT("Hearts", 4, "♥"), RANK("QUEEN", 10, "Q"))
    c5 = CARD(SUIT("Spades", 1, "♠"), RANK("QUEEN", 10, "Q"))
    c6 = CARD(SUIT("Diamonds", 3, "♦"), RANK("QUEEN", 10, "Q"))
    cards2 = [c4, c5, c6]
    print(is_triple(cards2))
    c7 = CARD(SUIT("Clubs", 2, "♣"), RANK("QUEEN", 10, "Q"))
    c8 = CARD(SUIT("Diamonds", 3, "♦"), RANK("QUEEN", 10, "Q"))
    cards3 = [c7, c8]
    print(is_pair(cards3))
    c9 = CARD(SUIT("Diamonds", 3, "♦"), RANK("QUEEN", 10, "Q"))
    c10 = CARD(SUIT("Clubs", 2, "♣"), RANK("QUEEN", 10, "Q"))
    c11 = CARD(SUIT("Spades", 1, "♠"), RANK("QUEEN", 10, "Q"))
    c12 = CARD(SUIT("Spades", 1, "♠"), RANK("QUEEN", 10, "Q"))
    cards4 = [c9, c10, c11, c12]
    print(is_four_of_a_kind(cards4))
    c13 = CARD(SUIT("Spades", 1, "♠"), RANK("THREE", 1, "2"))
    c14 = CARD(SUIT("Spades", 1, "♠"), RANK("THREE", 1, "3"))
    c15 = CARD(SUIT("Spades", 1, "♠"), RANK("FOUR", 2, "4"))
    c16 = CARD(SUIT("Spades", 1, "♠"), RANK("FIVE", 3, "5"))
    cards5 = [c13, c14, c15, c16]
    print(is_straight(cards5))