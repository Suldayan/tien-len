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

    # Draw 13 randoms cards
    def draw_hand():
        canvas.delete("all")
        x_position = 100
        for card in user_cards.cards:
            card.render(canvas, x_position, 500)
            x_position += 50

        canvas.create_window(700,400,window=arrange_button)
    
    # Arrange button function
    def arrange_card():
        user_cards.cards.sort(key=lambda card: (card.rank.value, card.suit.SuitRank))
        draw_hand()

    arrange_button = tk.Button(root, text="Arrange", command=arrange_card)
    draw_hand()

    root.mainloop()


main()
