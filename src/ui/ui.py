import tkinter as tk
from src.game.game import Game
from src.core.deck import DECK
from src.core.card import CARD
from src.ui_helper.turn import TurnManager
from src.ui.render import RenderManager
from src.ui_helper.gameflow import GameFlow
from src.ui_helper.tutorialOverlay import TutorialOverlay
from src.core.tutorialController import TutorialController
from src.ui_helper.buttonManager import BottomLeftButtonManager, RightSideButtonManager, LeftSideButtonManager
from src.ui.layout import Layout
from src.ui.actions import UIActions
from src.ui.pauseMenu import PauseMenu


class UI:
    def __init__(self, root, game: Game, deck: DECK):
        self.root = root
        self.game = game
        self.deck = deck
        self.user, self.bot = game.players[0], game.players[1]
        self.actions = UIActions(self)
        self.MainBG = "#14532d"
        self.pause = PauseMenu(self)

        # 1. Configurations
        self.CARD_WIDTH = CARD.WIDTH
        self.CARD_HEIGHT = CARD.HEIGHT
        self.CARD_GAP = -40
        #cache to avoid fetch_all_playable_hands called every second
        self.cached_playable_hands = []
        self.is_paused = False 


        # 2. Layout from layout.py
        theme = {"bg": self.MainBG}
        self.layout = Layout(self.root, theme, card_height=self.CARD_HEIGHT)

        # 3. Managers
        self.turn_manager = TurnManager(self) 
        self.render_manager = RenderManager(self)
        self.game_flow_manager = GameFlow(self)
        self.tutorial_overlay = TutorialOverlay(self.root)
        self.tutorial_controller = TutorialController()

        # 4. Setup UI components


        root.configure(bg = self.MainBG)
        root.minsize(1300 , 850 ) # Increased slightly to give the cards room to breathe

        #-------------------BUTTONS---------------------
        # Right side bar for Play/Pass buttons
        self.button_row = tk.Frame(self.layout.user_zone, bg = self.MainBG, height= 80)
        self.button_row.pack(fill="x", expand=True)
        self.button_row.pack_propagate(False)

        self.left_sidebar = tk.Frame(self.button_row, bg = self.MainBG)
        self.left_sidebar.pack(side="left", fill="both", expand= True)

        self.right_sidebar = tk.Frame(self.button_row, bg = self.MainBG)
        self.right_sidebar.pack(side="right",fill="both", expand= True)
        
        # bottom left: Pause
        self.controls = BottomLeftButtonManager(
            parent_frame=self.layout.bottom_frame,
            on_pause=self.toggle_pause
        )

        self.user_label = tk.Label(self.controls.frame, text="", font=("Perfect DOS VGA 437", 20), bg = self.MainBG, fg="white")
        self.user_label.place(relx=0.5, rely=0.5, anchor="center")

        # right sidebar: Play, Pass
        self.sidebar_controls = RightSideButtonManager(
            parent_frame=self.right_sidebar,
            on_play=self.actions.play_selected,
            on_pass=self.turn_manager.pass_turn
        )

        #left side bard: Arrange: 
        self.left_controls = LeftSideButtonManager(
            parent_frame=self.left_sidebar,
            on_arrange=self.actions.arrange_cards
        )

        #Show info when 2 is beaten
        self.chop_label = tk.Label(
            self.layout.table_canvas,
            text="",
            font=("Perfect DOS VGA 437", 20, "bold"),
            fg="yellow",
            bg="#003300",
            padx=20,
            pady=10)
        
        #Show turn label
        self.turn_message_after_id = None
        self.last_turn_message = None
        self.turn_label = tk.Label(
            self.layout.table_canvas,
            text="",
            font=("Perfect DOS VGA 437", 20, "bold"),
            fg="white",
            bg="#003300",
            padx=25,
            pady=12)

        # Redraw on resize
        root.bind("<Configure>", lambda e: self._on_configure())
        
        # THE KICKSTART 
        # Print to console so you know who the game picked to start
        print(f"Game Started! User turn: {self.user.is_turn()} | Bot turn: {self.bot.is_turn()}")

        self.actions.update_playable_hands()

        self.render_manager.draw()


        # ---------------------------------TUTORIAL OVERLAY SECTION--------------------------------- 
        # start the tutorial
        self.start_game_tutorial()
        # NEED FIX: The lowest card found in Game disappear after the game start, so I temporarily use this to find if user has lowest card/3 of Spade or not

    def check_turn_tutorial(self):
        if self.is_paused == True:
            return

        """Called whenever the turn switches back to the user."""
        if not self.user.is_turn():
            return 

        # forced pass
        # If the user has 0 valid moves, tell them to pass
        if len(self.cached_playable_hands) == 0 and self.game.current_combo is not None:
            pass_msg = self.tutorial_controller.get_contextual_message({}, "must_pass")

            if pass_msg:
                self.tutorial_overlay.show(pass_msg, dismissible=False)

            return
        
        # Game state
        user_cards = self.user.hand.get_cards()
        lowest_user_card = min(user_cards) if user_cards else None

        game_state = {
            "current_combo": self.game.current_combo,
            "is_first_game_turn": len(self.game.played_cards_history) == 0,
            "lowest_card": lowest_user_card 
        }

        # Ask the controller
        turn_msg = self.tutorial_controller.get_contextual_message(game_state, "user_turn")
        
        # If the table is completely empty, and it isn't the first turn of the game
        if self.game.current_combo is None and len(self.game.played_cards_history) > 0:
            turn_msg = self.tutorial_controller.get_contextual_message({}, "user_turn")

        if turn_msg:
            self.tutorial_overlay.show(turn_msg, dismissible=False)


    def start_game_tutorial(self): # showing the welcome message in the first turn of the game
        if self.is_paused == True:
            return
            
        user_cards = self.user.hand.get_cards()
        lowest_user_card = min(user_cards) if user_cards else None

        game_state = {
            "current_combo": self.game.current_combo,
            "is_first_game_turn": len(self.game.played_cards_history) == 0,
            "lowest_card": lowest_user_card
        }
        
        # ask for the welcome message
        welcome_msg = self.tutorial_controller.get_contextual_message(game_state, "game_start")

        # decide what happens after the welcome screen
        def begin_first_turn():
            if self.is_paused == True:
                return

            if self.user.is_turn():
                turn_msg = self.tutorial_controller.get_contextual_message(game_state, "user_turn")
                if turn_msg:
                    self.tutorial_overlay.show(turn_msg, dismissible=False) 
            else:
                self.root.after(500, self.turn_manager.bot_turn)

        # if the tutorialController gives a welcome message, show it
        if welcome_msg:
            self.tutorial_overlay.show(welcome_msg, on_dismiss=begin_first_turn, dismissible=True)
        else:
            # if no welcome message start the turn
            begin_first_turn()

    def update_player_info(self):
        self.layout.bot_label.config(text=f"{self.bot.get_name()}: {self.bot.get_points()} pts")
        self.user_label.config(text=f"{self.user.get_name()}: {self.user.get_points()} pts")

    def auto_scale_cards(self):
        try:
            if not self.layout.user_canvas.winfo_exists():
                return
        except tk.TclError:
            return
        
        canvas_width = self.layout.user_canvas.winfo_width()
        if canvas_width <= 1:  #not yet rendered
            return
        
        num_cards = len(self.user.get_hand().get_cards())
        if num_cards == 0:
          return
    # Minimum and maximum card sizes 
        MAX_W, MAX_H = 100, 150
        MIN_W, MIN_H = 50, 75

    # Compute ideal width so all cards fit, take 30% overlap
        ideal_width = canvas_width / (num_cards * 0.7)

        new_width = max(MIN_W, min(MAX_W, ideal_width))
        
        ratio = 80 / 56
        new_height = int(new_width * ratio)

    # Update UI card size
        self.CARD_WIDTH = int(new_width)
        self.CARD_HEIGHT = int(new_height)
    # Overlap gap (negative)
        self.CARD_GAP = int(-self.CARD_WIDTH * 0.4)

        CARD.WIDTH = self.CARD_WIDTH
        CARD.HEIGHT = self.CARD_HEIGHT

    def _on_configure(self):   
        try:
            if not self.layout.user_canvas.winfo_exists():
                return
            if not self.layout.bot_label.winfo_exists():
                return
            self.auto_scale_cards()
            self.render_manager.draw()
        except tk.TclError:
            return
    
    def handle_game_over(self): #do not move this to gameflow.py since tk is not defined there
        message = self.game.round_results()
        self.render_manager.draw()

        popup = tk.Toplevel(self.root)
        popup.title("Round Finished")
        popup.geometry("350x300")
        popup.configure( bg = "#14532d")

        label = tk.Label(
            popup,
            text=message,
            font=("Perfect DOS VGA 437", 14),
            bg = "#14532d",
            fg="white",
            justify="center")
        label.pack(pady=20)

        button_frame = tk.Frame(popup, bg = "#14532d")
        button_frame.pack(pady=10)

        continue_btn = tk.Button(
            button_frame,
            text="Continue match",
            font=("Perfect DOS VGA 437", 12),
            command=lambda: self.game_flow_manager.continue_match(popup)
        )
        continue_btn.pack(fill="x", pady=5)

        new_game_btn = tk.Button(
            button_frame,
            text="New game",
            font=("Perfect DOS VGA 437", 12),
            command=lambda: self.game_flow_manager.new_game(popup)
        )
        new_game_btn.pack(fill="x", pady=5)

        exit_btn = tk.Button(
            button_frame,
            text="Exit",
            font=("Perfect DOS VGA 437", 12),
            command=self.root.destroy
        )
        exit_btn.pack(fill="x", pady=5)

    def show_chop_message(self, text):
        #show messgae
        self.chop_label.config(text=text)
        self.chop_label.place(relx=0.5, rely=0.3, anchor="center")

        #hide message after 15s
        self.root.after(5000, self.hide_chop_message)

    def hide_chop_message(self):
        self.chop_label.config(text="")
        self.chop_label.place_forget()

    def show_turn_message(self, text, duration=1500):
        #Cancel prev timer if exists
        if self.turn_message_after_id:
            self.root.after_cancel(self.turn_message_after_id)

        #Prevent same message spam
        if text == self.last_turn_message:
            return
        self.last_turn_message = text

        self.turn_label.config(text=text)
        self.root.after(50, lambda: self.turn_label.place(relx=0.5, rely=0.1, anchor="center"))

        self.turn_message_after_id = self.root.after(duration, self.hide_turn_message)

    def hide_turn_message(self):
        self.turn_label.place_forget()

    def check_game_over(self): #don't move this to gameflow.py yet, it will break everything
        """Call after any play or pass. Returns True if game ended."""
        if self.game.is_game_over():
            self.handle_game_over()
            return True
        return False
    
#-------------------------PAUSE MENU--------------------------
    def toggle_pause(self):
        if self.is_paused:
            self.resume_game()
        else:
            self.open_pause_menu()

    def open_pause_menu(self):
        if self.is_paused:
            return

        self.is_paused = True
        self.controls.pause_btn.canvas.itemconfig(
            self.controls.pause_btn.text_id, text="Resume"
        )

        self.tutorial_overlay.hide()
        self.pause.show()  # Use self.pause.show() instead of self.pause_menu.place()

    def resume_game(self):
        if not self.is_paused:
            return

        self.is_paused = False
        self.controls.pause_btn.canvas.itemconfig(
            self.controls.pause_btn.text_id, text="Pause"
        )

        self.pause.hide()  # Use self.pause.hide() instead of self.pause_menu.place_forget()

        if self.bot.is_turn():
            self.root.after(100, self.turn_manager.bot_turn)

    def pause_menu_new_game(self):
        self.is_paused = False
        self.controls.pause_btn.canvas.itemconfig(
            self.controls.pause_btn.text_id, text="Pause"
        )
        self.pause.hide()  # Use self.pause.hide()
        self.game_flow_manager.reset_game()
        self.start_game_tutorial()

    def on_card_clicked(self, card):
        if self.is_paused:
            return

        if not self.user.is_turn():
            return

        card.toggle_selected()
        self.render_manager.draw()