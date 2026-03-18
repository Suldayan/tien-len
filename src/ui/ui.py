import tkinter as tk
from src.game import Game
from src.deck import DECK
from tkinter import messagebox
from src.card import CARD
from src.ui.turn import TurnManager
from src.ui.render import RenderManager
from src.ui.gameflow import GameFlow

class UI:
    def __init__(self, root, game: Game, deck: DECK):
        self.root = root
        self.game = game
        self.deck = deck

        self.user = game.players[0]
        self.bot = game.players[1]

        #new member variable
        self.turn_manager = TurnManager(self) 
        self.render_manager = RenderManager(self)
        self.game_flow_manager = GameFlow(self)

        from src.card import CARD
        
        self.CARD_WIDTH = CARD.WIDTH
        self.CARD_HEIGHT = CARD.HEIGHT
        self.CARD_GAP = -40

        #cache playable hands to avoid fetch_all_playable_hands being called every second
        self.cached_playable_hands = []


        root.configure(bg="green")
        root.minsize(500, 700) # Increased slightly to give the cards room to breathe

        # TOP ZONE: Bot 
        self.top_frame = tk.Frame(root, bg="green")
        self.top_frame.pack(side="top", fill="x")
        
        self.bot_label = tk.Label(self.top_frame, text="", font=("Arial", 20), bg="green", fg="white")
        self.bot_label.pack(pady=10)

        self.bot_canvas = tk.Canvas(self.top_frame, bg="green", highlightthickness=0, bd=0,
                                    height=self.CARD_HEIGHT + 40)
        self.bot_canvas.pack(fill="both", expand=True, padx=10)

        # BOTTOM ZONE: User & Controls 
        # We pack this BEFORE the middle table so it claims its space at the bottom first!
        self.bottom_frame = tk.Frame(root, bg="green")
        self.bottom_frame.pack(side="bottom", fill="x", pady=10)


        # 1. Put buttons at the very bottom
        self.controls_frame = tk.Frame(self.bottom_frame, bg="green")
        self.controls_frame.pack(side="bottom", fill="x", pady=5)

        self.arrange_button = tk.Button(self.controls_frame, text="Arrange", font=("Arial", 16), command=self.arrange_cards)
        self.arrange_button.pack(side="left", expand=True, padx=5)

        self.play_button = tk.Button(self.controls_frame, text="Play", font=("Arial", 16), command=self.play_selected)
        self.play_button.pack(side="left", expand=True, padx=5)

        self.pass_button = tk.Button(self.controls_frame, text="Pass", font=("Arial", 16), command=self.turn_manager.pass_turn)
        self.pass_button.pack(side="left", expand=True, padx=5)

        # 2. Put user canvas right above the buttons
        self.user_canvas = tk.Canvas(self.bottom_frame, bg="green", highlightthickness=0, bd=0,
                                     height=self.CARD_HEIGHT + 40)
        self.user_canvas.pack(fill="both", expand=True, padx=10)

        # 3. Put user label right above their canvas
        self.user_label = tk.Label(self.bottom_frame, text="", font=("Arial", 20), bg="green", fg="white")
        self.user_label.pack(side="bottom", pady=10)

        # MIDDLE ZONE: The Table
        # Because this is packed last with expand=True, it fills the gap between Top and Bottom.
        # A middle container to hold both the Left side-bar and the Main table
        self.mid_frame = tk.Frame(root, bg="green")
        self.mid_frame.pack(fill="both", expand=True)

        # Left side bar for hint section
        self.hint_canvas = tk.Canvas(self.mid_frame, bg="green", highlightthickness=0)
        self.hint_canvas.place(relx=0, rely=0, relwidth=0.2, relheight=1.0)
        # Main table: cards being played here
        self.table_canvas = tk.Canvas(self.mid_frame, bg="green", highlightthickness=0)
        self.table_canvas.place(relx=0.2, rely=0, relwidth=0.6, relheight=1.0)

        #Show info when 2 is beaten
        self.chop_label = tk.Label(
            self.table_canvas,
            text="",
            font=("Arial", 22, "bold"),
            fg="yellow",
            bg="#003300",
            padx=20,
            pady=10)

        # Redraw on resize
        root.bind("<Configure>", lambda e: (self.auto_scale_cards(), self.draw()))
        
        # THE KICKSTART 
        # Print to console so you know who the game picked to start
        print(f"Game Started! User turn: {self.user.is_turn()} | Bot turn: {self.bot.is_turn()}")

        # If the bot was given the first turn, tell it to move!
        if self.bot.is_turn():
            self.root.after(1000, self.turn_manager.bot_turn)

        self.update_playable_hands()

        self.draw()

    def update_player_info(self):
        self.bot_label.config(text=f"{self.bot.get_name()}: {self.bot.get_points()} pts")
        self.user_label.config(text=f"{self.user.get_name()}: {self.user.get_points()} pts")

    #def draw_cards(self, canvas, cards): is now in render.py

    #def draw_hint_card(self, canvas, combo_obj, current_x, current_y, canvas_width, canvas_height): is now in render.py

    def render_back(self, canvas, x, y):
     from src.card import CARD
     width = CARD.WIDTH
     height = CARD.HEIGHT

    # Draw card background
     canvas.create_rectangle(
        x - width//2, y - height//2,
        x + width//2, y + height//2,
        fill="#1E3A8A",   # deep blue
        outline="white",
        width=3
    )

    # Optional: add a pattern or symbol
     canvas.create_text(
        x, y,
        text="★",
        fill="white",
        font=("Arial", 40)
    )
    def auto_scale_cards(self):
        canvas_width = self.user_canvas.winfo_width()
        num_cards = len(self.user.get_hand().get_cards())
        if num_cards == 0:
          return
    # Minimum and maximum card sizes 
        MAX_W, MAX_H = 100, 150
        MIN_W, MIN_H = 50, 75
    # Compute ideal width so all cards fit
    # take 30% overlap
        ideal_width = canvas_width / (num_cards * 0.7)

    # Clamp width between min and max
        new_width = max(MIN_W, min(MAX_W, ideal_width))
        new_height = new_width * 1.5  # keep 2:3 ratio

    # Update UI card size
        self.CARD_WIDTH = int(new_width)
        self.CARD_HEIGHT = int(new_height)

    # Overlap gap (negative)
        self.CARD_GAP = int(-self.CARD_WIDTH * 0.4)

        CARD.WIDTH = self.CARD_WIDTH
        CARD.HEIGHT = self.CARD_HEIGHT

    def update_playable_hands(self):
        if self.user.is_turn():
            self.cached_playable_hands = self.game.fetch_all_playable_hands(self.user)
        else:
            self.cached_playable_hands = []

    def draw(self):
        self.update_player_info()
        self.render_manager.draw_cards(self.bot_canvas, self.bot.get_hand().get_cards())
        self.render_manager.draw_cards(self.user_canvas, self.user.get_hand().get_cards())
        #fixed: always clear the middle table before redrawing
        self.table_canvas.delete("all")
        self.hint_canvas.delete("all")

        #get all the playable hands from Game class's function "fectch_all_playable_hands"
        playable_hands = self.cached_playable_hands


        self.hint_canvas.update_idletasks()
        c_width = self.hint_canvas.winfo_width()
        c_height = self.hint_canvas.winfo_height()
        if c_width <= 1: c_width = 180 # Fallback for startup
        
        scale = 0.65
        h_x = 15 + (self.CARD_WIDTH * scale // 2)
        h_y = 70

        for hand in playable_hands:
            # pass the positions and get to the updated ones
            result = self.render_manager.draw_hint_card(self.hint_canvas, hand, h_x, h_y, c_width, c_height)

            if result == (None, None):
                break
            
            h_x, h_y = result

        if self.game.current_combo:
            #fixed: target the middle canvas instead of bot_canvas
            self.table_canvas.update_idletasks()

            width = self.table_canvas.winfo_width()
            height = self.table_canvas.winfo_height()

            cards = self.game.current_combo.cards

            #spacing for played cards on the table
            played_card_spacing = 60

            #calculate total width of the played group
            #assuming render draws from center x
            if len(cards) > 1:
                total_group_width = (len(cards) - 1) * played_card_spacing
            else:
                total_group_width = 0

            start_x = (width // 2) - (total_group_width // 2)
            center_y = height // 2

            for i, card in enumerate(cards):
                x = start_x + i * played_card_spacing
                #fixed: Render the card onto table_canvas
                card.render(self.table_canvas, x, center_y)

    # Arrange button function
    def arrange_cards(self):
        for card in self.user.get_hand().get_cards():
            card.selected = False
        self.user.get_hand().sort()
        self.update_playable_hands()
        self.draw()

    def play_selected(self):
        if not self.user.is_turn():
            return

        selected = self.user.get_hand().get_selected_cards()

        if not selected:
            return

        success, message = self.game.play_cards(selected)
        if message and "chopped" in message:
            self.show_chop_message(message)
        self.update_playable_hands()
        self.draw()
        if self.check_game_over():
            return
        self.root.after(800, self.turn_manager.advance_turn)
    
    #def pass_turn(self): is now in turn.py

    #def bot_turn(self): is now in turn.py

    #def advance_turn(self): is now in turn.py

    #def auto_pass(self, player): is now in turn.py

    def card_clicked(self, card):
        if not self.user.is_turn():
            return

        card.toggle_selected()
        print(f"Selected:", card)
        self.draw()

    def handle_game_over(self):
        message = self.game.round_results()
        self.draw()

        popup = tk.Toplevel(self.root)
        popup.title("Round Finished")
        popup.geometry("350x300")
        popup.configure(bg="green")

        label = tk.Label(
            popup,
            text=message,
            font=("Arial", 14),
            bg="green",
            fg="white",
            justify="center")
        label.pack(pady=20)

        button_frame = tk.Frame(popup, bg="green")
        button_frame.pack(pady=10)

        continue_btn = tk.Button(
            button_frame,
            text="Continue match",
            font=("Arial", 12),
            command=lambda: self.game_flow_manager.continue_match(popup)
        )
        continue_btn.pack(fill="x", pady=5)

        new_game_btn = tk.Button(
            button_frame,
            text="New game",
            font=("Arial", 12),
            command=lambda: self.game_flow_manager.new_game(popup)
        )
        new_game_btn.pack(fill="x", pady=5)

        exit_btn = tk.Button(
            button_frame,
            text="Exit",
            font=("Arial", 12),
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

    def check_game_over(self): #don't move this to gameflow.py yet, it will break everything
        """Call after any play or pass. Returns True if game ended."""
        if self.game.is_game_over():
            self.handle_game_over()
            return True
        return False

    #def reset_game(self): is now in game_dialog.py

    #def continue_match(self, popup): is now in game_dialog.py

    #def new_game(self, popup): is now in game_dialog.py
