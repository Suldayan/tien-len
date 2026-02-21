import random
import tkinter as tk
from src.hands import USER_HAND
from src.hands import BOT1_HAND
from src.deck import DECK
from src.distCards import DistCards

def main():
    deck = DECK()

    #amount of max cards per hand
    cardCount = 13
    usedList = []
    user_List = []
    bot1_List = []

    root = tk.Tk()
    root.title("Card Demo")

    canvas = tk.Canvas(root, width=1200, height=1000, bg="green")
    canvas.pack()

     # Distributes 13 cards from deck into user hand
    user_cards = USER_HAND(DistCards(user_List, cardCount, deck, usedList))
    bot1_cards = BOT1_HAND(DistCards(bot1_List, cardCount, deck, usedList))

    # Draw 13 randoms cards
    def draw_hand():
        canvas.delete("all")
        x_position = 300
        for card in user_cards.cards:
            card.render(canvas, x_position, 750)
            x_position += 50
        x2_position = 300
        for card in bot1_cards.cards:
            card.render(canvas, x2_position, 100)
            x2_position += 50
        canvas.create_window(900, 650 ,window=arrange_button)
    
    # Arrange button function
    def arrange_card():
        user_cards.cards.sort(key=lambda card: (card.rank.value, card.suit.SuitRank))
        draw_hand()

    arrange_button = tk.Button(root, text="Arrange", font=("Arial", 16),command=arrange_card)

    start_button = tk.Button(root, text="Start Game", font=("Arial", 16),command=draw_hand)
    canvas.create_window(600, 500, window=start_button)


    root.mainloop()



main()
