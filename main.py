import tkinter as tk
from src.deck import DECK
from src.user import User
from src.bot import Bot
from src.hand import Hand
from src.ui.ui import UI
from src.game.game import Game
from src.menu import MenuScreen

def start_game():
    # Remove menu
    menu_frame.pack_forget()

    # Create game
    deck = DECK()
    deck.shuffle()

    # Create players with dealt hands
    user = User("Demo User", Hand(deck.deal(13)))
    bot = Bot("Bot", Hand(deck.deal(13)))

    # game object
    game = Game([user, bot])

    game.set_first_turn()

    ui = UI(root, game, deck)
    ui.render_manager.draw()

def main():
    global root, menu_frame

    root = tk.Tk()
    root.title("13Game")
    root.geometry("1024x768")
    root.configure(bg="green")

    # Create menu screen
    menu_frame = MenuScreen(root, start_game)
    menu_frame.pack(fill="both", expand=True)

    root.mainloop()

if __name__ == "__main__":
    main()

