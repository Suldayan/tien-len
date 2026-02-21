import random
#function to distribute cards
def DistCards(cardsList, cardCount, Deck, usedList):
    while len(cardsList) < cardCount:
        x = random.choice(Deck.cards)
        if (x not in usedList):
            cardsList.append(x)
            #used list keeps track of which cards currently in someone's hand
            usedList.append(x)
        else:
            continue
    
    return cardsList