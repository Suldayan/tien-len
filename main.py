import tkinter as tk
from src.deck import DECK
from src.user import User
from src.bot import Bot
from src.hand import Hand
from src.ui import UI

def main():
    deck = DECK()
    deck.shuffle()

    user = User("Demo User", Hand(deck.deal(13)))
    bot = Bot("Bot", Hand(deck.deal(13)))

    root = tk.Tk()
    root.title("Card Demo")

    ui = UI(root, user, bot)

    # Start game by drawing everything
    ui.draw()

    root.mainloop()

if __name__ == "__main__":
    main()
