import tkinter as tk
from src.game import Game
from src.deck import DECK
from tkinter import messagebox
from src.card import CARD

class UI:
    def __init__(self, root, game: Game, deck: DECK):
        self.root = root
        self.game = game
        self.deck = deck

        self.user = game.players[0]
        self.bot = game.players[1]

        from src.card import CARD
        
        self.CARD_WIDTH = CARD.WIDTH
        self.CARD_HEIGHT = CARD.HEIGHT
        self.CARD_GAP = -40


        root.configure(bg="green")
        root.minsize(500, 700) # Increased slightly to give the cards room to breathe

        # --- TOP ZONE: Bot ---
        self.top_frame = tk.Frame(root, bg="green")
        self.top_frame.pack(side="top", fill="x")
        
        self.bot_label = tk.Label(self.top_frame, text="", font=("Arial", 20), bg="green", fg="white")
        self.bot_label.pack(pady=10)

        self.bot_canvas = tk.Canvas(self.top_frame, bg="green", highlightthickness=0, bd=0,
                                    height=self.CARD_HEIGHT + 40)
        self.bot_canvas.pack(fill="both", expand=True, padx=10)

        # --- BOTTOM ZONE: User & Controls ---
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

        self.pass_button = tk.Button(self.controls_frame, text="Pass", font=("Arial", 16), command=self.pass_turn)
        self.pass_button.pack(side="left", expand=True, padx=5)

        # 2. Put user canvas right above the buttons
        self.user_canvas = tk.Canvas(self.bottom_frame, bg="green", highlightthickness=0, bd=0,
                                     height=self.CARD_HEIGHT + 40)
        self.user_canvas.pack(fill="both", expand=True, padx=10)

        # 3. Put user label right above their canvas
        self.user_label = tk.Label(self.bottom_frame, text="", font=("Arial", 20), bg="green", fg="white")
        self.user_label.pack(side="bottom", pady=10)

        # --- MIDDLE ZONE: The Table ---
        # Because this is packed last with expand=True, it neatly fills the gap between Top and Bottom.
        self.table_canvas = tk.Canvas(root, bg="green", highlightthickness=0, bd=0)
        self.table_canvas.pack(fill="both", expand=True, padx=10, pady=10)

        # Redraw on resize
        root.bind("<Configure>", lambda e: (self.auto_scale_cards(), self.draw()))
        
        # --- THE KICKSTART ---
        # Print to console so you know who the game picked to start
        print(f"Game Started! User turn: {self.user.is_turn()} | Bot turn: {self.bot.is_turn()}")

        # If the bot was given the first turn, tell it to move!
        if self.bot.is_turn():
            self.root.after(1000, self.bot_turn)

        self.draw()

    def update_player_info(self):
        self.bot_label.config(text=f"{self.bot.get_name()}: {self.bot.get_points()} pts")
        self.user_label.config(text=f"{self.user.get_name()}: {self.user.get_points()} pts")

    def draw_cards(self, canvas, cards):
        canvas.update_idletasks()
        canvas.delete("all")

        num_cards = len(cards)
        if num_cards == 0:
            return

        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()

        total_width = num_cards * self.CARD_WIDTH + (num_cards - 1) * self.CARD_GAP
        start_x = (canvas_width - total_width) // 2 + self.CARD_WIDTH // 2
        y = canvas_height // 2

        for i, card in enumerate(cards):
            x = start_x + i * (self.CARD_WIDTH + self.CARD_GAP)
            if canvas == self.user_canvas:
                card.render(canvas, x, y, click_callback=self.card_clicked)
            else:
                self.render_back(canvas, x, y)

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


    def draw(self):
        self.update_player_info()
        self.draw_cards(self.bot_canvas, self.bot.get_hand().get_cards())
        self.draw_cards(self.user_canvas, self.user.get_hand().get_cards())
        #fixed: always clear the middle table before redrawing
        self.table_canvas.delete("all")

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
        self.draw()

    def play_selected(self):
        if not self.user.is_turn():
            return

        selected = self.user.get_hand().get_selected_cards()

        if not selected:
            return

        self.game.play_cards(selected)
        self.draw()
        if self.check_game_over():
            return
        self.root.after(800, self.advance_turn)

    def pass_turn(self):
        if not self.user.is_turn():
            return

        self.game.pass_turn()
        self.draw()
        if self.check_game_over():
            return
        self.root.after(800, self.advance_turn)

    def bot_turn(self):
        if not self.bot.is_turn() or self.game.is_game_over():
            return

        selected_cards = self.bot.make_move(self.game)

        if selected_cards:
            self.game.play_cards(selected_cards)
        else:
            self.game.pass_turn()

        self.draw()
        if self.check_game_over():
            return
        self.root.after(800, self.advance_turn)

    def advance_turn(self):
        """Single choke point: decides what happens after any play or pass."""
        if self.game.is_game_over():
            self.handle_game_over()
            return

        current = self.game.current_player()

        if not self.game.has_valid_move(current):
            # Whoever is stuck gets auto-passed, bot or user
            self.root.after(800, lambda: self.auto_pass(current))
        elif current == self.bot:
            self.root.after(800, self.bot_turn)
        # else: user's turn — just wait for their input

    def auto_pass(self, player):
        """Automatically passes for any player with no valid moves."""
        if not player.is_turn():
            return

        print(f"{player.get_name()} has no valid move. Auto pass.")
        self.game.pass_turn()
        self.draw()
        self.root.after(800, self.advance_turn)

    def card_clicked(self, card):
        if not self.user.is_turn():
            return

        card.toggle_selected()
        print(f"Selected:", card)
        self.draw()

    def handle_game_over(self):
        message = self.game.round_results()
        play_again = messagebox.askyesno("Match Result", message + "\n\nWanna play again?")
        if play_again:
            self.reset_game()
        else:
            self.root.destroy()

    def check_game_over(self):
        """Call after any play or pass. Returns True if game ended."""
        if self.game.is_game_over():
            self.handle_game_over()
            return True
        return False

    def reset_game(self):
        self.game.reset(self.deck)
        self.draw()
        if self.bot.is_turn():
            self.root.after(800, self.bot_turn)