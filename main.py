import random
import tkinter as tk
from src.hands import USER_HAND
from src.hands import BOT1_HAND
from src.deck import DECK
#removed the distCards because dealing cards is now using deal() in class DECK

def main():
    deck = DECK()
    deck.shuffle()

    root = tk.Tk()
    root.title("Card Demo")

    canvas = tk.Canvas(root, width=1200, height=1000, bg="green")
    canvas.pack()

     # Distributes 13 cards using the deal() from class DECK 
    user_cards = USER_HAND(deck.deal(13))
    bot1_cards = BOT1_HAND(deck.deal(13))

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

if __name__ == "__main__":
    main()
