import tkinter as tk
from src.game import Game

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
        root.minsize(400, 600)

        # Bot info label
        self.bot_frame = tk.Frame(root, bg="green")
        self.bot_frame.pack(fill="x")
        self.bot_label = tk.Label(self.bot_frame, text="", font=("Arial", 20), bg="green", fg="white")
        self.bot_label.pack(pady=10)

        # Bot canvas
        self.bot_canvas = tk.Canvas(root, bg="green", highlightthickness=0, bd=0,
                                    height=self.CARD_HEIGHT + 40)
        self.bot_canvas.pack(fill="x", padx=10)

        #middle Section to put played cards
        #fixx: Replaced tk.Frame with tk.Canvas so we can draw on it
        self.table_canvas = tk.Canvas(root, bg="green", highlightthickness=0, bd=0)
        self.table_canvas.pack(fill="both", expand=True, padx=10, pady=20)

        # User canvas
        self.user_canvas = tk.Canvas(root, bg="green", highlightthickness=0, bd=0,
                                     height=self.CARD_HEIGHT + 40)
        self.user_canvas.pack(fill="x", padx=10)

        # User info label
        self.user_frame = tk.Frame(root, bg="green")
        self.user_frame.pack(fill="x")
        self.user_label = tk.Label(self.user_frame, text="", font=("Arial", 20), bg="green", fg="white")
        self.user_label.pack(pady=10)

        # Arrange button
        self.arrange_button = tk.Button(root, text="Arrange", font=("Arial", 16), command=self.arrange_cards)
        self.arrange_button.pack(pady=10)

        # Play button
        self.play_button = tk.Button(root, text="Play", font=("Arial", 16), command=self.play_selected)
        self.play_button.pack(pady=5)

        # Pass button
        self.pass_button = tk.Button(root, text="Pass", font=("Arial", 16), command=self.pass_turn)
        self.pass_button.pack(pady=5)

        # Redraw on resize
        root.bind("<Configure>", lambda e: self.draw())

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
        self.user.get_hand().sort()
        self.draw()

    def play_selected(self):
        if not self.user.is_turn():
            return

        selected = self.user.get_hand().get_selected_cards()
        
        message = self.game.play_cards(selected)

        print(message)

        self.draw()

        if self.game.is_game_over():
            print("Game Over")
            return

        self.root.after(800, self.bot_turn)


    def pass_turn(self):
        if not self.user.is_turn():
            return

        self.game.pass_turn()
        self.draw()

        self.root.after(800, self.bot_turn)


    def bot_turn(self):
        if not self.bot.is_turn():
            return

        # Simple bot: try playing one card
        for card in self.bot.get_hand().get_cards():
            success, _ = self.game.play_cards([card])
            if success:
                break
        else:
            self.game.pass_turn()

        self.draw()

    def card_clicked(self, card):
        if not self.user.is_turn():
            return

        card.toggle_selected()
        print(f"Selected:", card)
        self.draw()

    