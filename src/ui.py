import tkinter as tk
from src.game import Game
from tkinter import messagebox

class UI:
    def __init__(self, root, game: Game):
        self.root = root
        self.game = game

        self.user = game.players[0]
        self.bot = game.players[1]

        self.CARD_WIDTH = 100
        self.CARD_HEIGHT = 150
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
        self.bot_canvas.pack(fill="x", padx=10)

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
        self.user_canvas.pack(side="bottom", fill="x", padx=10)

        # 3. Put user label right above their canvas
        self.user_label = tk.Label(self.bottom_frame, text="", font=("Arial", 20), bg="green", fg="white")
        self.user_label.pack(side="bottom", pady=10)

        # --- MIDDLE ZONE: The Table ---
        # Because this is packed last with expand=True, it neatly fills the gap between Top and Bottom.
        self.table_canvas = tk.Canvas(root, bg="green", highlightthickness=0, bd=0)
        self.table_canvas.pack(fill="both", expand=True, padx=10, pady=10)

        # Redraw on resize
        root.bind("<Configure>", lambda e: self.draw())
        
        # --- THE KICKSTART ---
        # Print to console so you know who the game picked to start
        print(f"Game Started! User turn: {self.user.is_turn()} | Bot turn: {self.bot.is_turn()}")

        # If the bot was given the first turn, tell it to move!
        if self.bot.is_turn():
            self.root.after(1000, self.bot_turn)

        #added these two line so bot can start after delay 0.8sec
        self.draw()
        self.root.after(800, self.bot_turn)

    def update_player_info(self):
        self.bot_label.config(text=f"{self.bot.get_name()} - {self.bot.get_points()} pts")
        self.user_label.config(text=f"{self.user.get_name()} - {self.user.get_points()} pts")

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
                card.render(canvas, x, y)

    def draw(self):
        self.update_player_info()
        self.draw_cards(self.bot_canvas, self.bot.get_hand().get_cards())
        self.draw_cards(self.user_canvas, self.user.get_hand().get_cards())
        #fixed: always clear the middle table before redrawing
        self.table_canvas.delete("all") 

        if self.game.current_combo:
            #fixed: target the  middle canvas instead of bot_canvas
            self.table_canvas.update_idletasks()

            width = self.table_canvas.winfo_width()
            height = self.table_canvas.winfo_height()

            cards = self.game.current_combo.cards

            #spacing for played cards on the table 
            played_card_spacing = 60

            #calculate total width of the played group
            #cassuming render draws from center x
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
            if not self.game.has_valid_move(self.user):
                print("No valid move. You must pass.")
                self.game.pass_turn()
                self.draw()
                self.root.after(800, self.bot_turn)
            return
        
        message = self.game.play_cards(selected)

        print(message)

        self.draw()

        if self.game.is_game_over():
            self.handle_game_over()
            return

        self.root.after(800, self.bot_turn)


    def pass_turn(self):
        if not self.user.is_turn():
            return

        self.game.pass_turn()
        self.draw()

        self.root.after(800, self.bot_turn)

    def bot_turn(self):
            if not self.bot.is_turn() or self.game.is_game_over():
                return

            selected_cards = self.bot.make_move(self.game)

            if selected_cards:
                self.game.play_cards(selected_cards)
            else:
                self.game.pass_turn()

            self.draw()
            
            if self.game.current_player() == self.user:
                if not self.game.has_valid_move(self.user):
                    print("User has no valid move. Auto pass.")
                    self.root.after(800, self.auto_pass_user)
            else: 
                if not self.game.is_game_over():
                    self.root.after(1000, self.bot_turn)

    def auto_pass_user(self):
        if not self.user.is_turn():
            return

        self.game.pass_turn()
        self.draw()
        self.root.after(800, self.bot_turn)

    def card_clicked(self, card):
        if not self.user.is_turn():
            return

        card.toggle_selected()
        print(f"Selected:", card)
        self.draw()

    def handle_game_over(self):
        winner, loser = self.game.end_match()

        if winner:
            message = (
                f"Congratulations, {winner.get_name()}!\nYou win :)\n\n"
                f"{winner.get_name()}'s points: {winner.get_points()}\n"
                f"{loser.get_name()}'s points: {loser.get_points()}"
            )
        else: 
            message = "Game over"

        play_again = messagebox.askyesno("Match Result", message + "\n\nWanna play again?")
        if play_again:
            self.reset_game()
        else:
            self.root.destroy()
    