import random
import tkinter as tk
from src.deck import DECK

def main():
    deck = DECK()

    root = tk.Tk()
    root.title("Card Demo")

    canvas = tk.Canvas(root, width=800, height=600, bg="green")
    canvas.pack()

    # Draw 13 randoms cards
    sample_cards = random.sample(deck.cards, 13)

    x_position = 100
    for card in sample_cards:
        card.render(canvas, x_position, 500)
        x_position += 50

    root.mainloop()


main()
