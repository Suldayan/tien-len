import tkinter as tk
from src.deck import DECK
from src.user import User
from src.bot import Bot
from src.hand import Hand
from src.ui.ui import UI
from src.game import Game

def main():
    deck = DECK()
    deck.shuffle()

    user = User("Demo User", Hand(deck.deal(13)))
    bot = Bot("Bot", Hand(deck.deal(13)))

    game = Game([user, bot])

    root = tk.Tk()
    root.title("Card Demo")

    ui = UI(root, game, deck)

    # Start game by drawing everything
    ui.render_manager.draw()

    root.mainloop()

if __name__ == "__main__":
    main()
