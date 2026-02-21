import random
import tkinter as tk
from src.hands import USER_HAND
from src.deck import DECK
from src.distCards import DistCards

def main():
    deck = DECK()

    #amount of max cards per hand
    cardCount = 13
    cardsList = []
    usedList = []

    root = tk.Tk()
    root.title("Card Demo")

    canvas = tk.Canvas(root, width=800, height=600, bg="green")
    canvas.pack()

     # Distributes 13 cards from deck into user hand
    user_cards = USER_HAND(DistCards(cardsList, cardCount, deck, usedList))

    x_position = 100
    for card in user_cards.cards:
        card.render(canvas, x_position, 500)
        x_position += 50

    root.mainloop()


main()
