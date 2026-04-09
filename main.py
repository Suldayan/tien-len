import tkinter as tk
from src.core.deck import DECK
from src.core.user import User
from src.core.bot import Bot
from src.core.hand import Hand
from src.ui.ui import UI
from src.game.game import Game
from src.core.menu import MenuScreen
from src.ui_helper.fontLoader import install_font


install_font("src/assets/Perfect DOS VGA 437.ttf")


def start_game():
    
    # Remove menu
    menu_frame.destroy()

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
    root.configure(bg = "#14532d")

    # Create menu screen
    menu_frame = MenuScreen(root, start_game)
    menu_frame.pack(fill="both", expand=True)

    root.mainloop()

if __name__ == "__main__":
    main()

