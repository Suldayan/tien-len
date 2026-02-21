class Combo:
    def __init__(self, combo_type, cards, length):
        self.combo_type = combo_type
        self.cards = cards
        self.length = length
        
def sortByRankValue(Cards): #I used ChatGPT for this, idk how to sort stuff in python
    return sorted(Cards, key=lambda c: c.rank.value)

def is_pair(Cards): #pass in a vector/array
    return len(Cards) == 2 and Cards[0].rank.value == Cards[1].rank.value

def is_triple(Cards):
    return len(Cards) == 3 and Cards[0].rank.value == Cards[1].rank.value == Cards[2].rank.value

def is_four_of_a_kind(Cards):
    return len(Cards) == 4 and Cards[0].rank.value == Cards[1].rank.value == Cards[2].rank.value == Cards[3].rank.value

def is_straight(Cards):
    Cards = sortByRankValue(Cards)
    if len(Cards) < 3:
        return False
    if len(Cards) > 12:
        return False
    for i in range(len(Cards)):
        if Cards[i].rank.value == 13: #2 can't be in a straight
            return False
    for i in range(len(Cards) - 1): #check for duplicate
        if Cards[i].rank.value == Cards[i + 1].rank.value:
            return False
    counter = Cards[0].rank.value
    for i in range(len(Cards)): #Check if this hand is a straight or not
        if Cards[i].rank.value != counter:
            return False
        counter+=1
    return True

def make_combo(Cards):
    Cards = sortByRankValue(Cards)
    
    if len(Cards) == 1:
        return Combo("SINGLE", Cards, 1)

    if is_pair(Cards):
        return Combo("PAIR", Cards, 2)

    if is_triple(Cards):
        return Combo("TRIPLE", Cards, 3)

    if is_four_of_a_kind(Cards):
        return Combo("FOUR_OF_A_KIND", Cards, 4)

    if is_straight(Cards):
        return Combo("STRAIGHT", Cards, len(Cards))
    
    return None