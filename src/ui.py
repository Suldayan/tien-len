import tkinter as tk

class UI:
    def __init__(self, root, user, bot):
        self.root = root
        self.user = user
        self.bot = bot

        self.CARD_WIDTH = 100
        self.CARD_HEIGHT = 150
        self.CARD_GAP = 10

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

        # This configures the space between the bot cards and the user cards
        self.spacer = tk.Frame(root, bg="green")
        self.spacer.pack(fill="both", expand=True)

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
            card.render(canvas, x, y)

    def draw(self):
        self.update_player_info()
        self.draw_cards(self.bot_canvas, self.bot.get_hand().get_cards())
        self.draw_cards(self.user_canvas, self.user.get_hand().get_cards())

    # Arrange button function
    def arrange_cards(self):
        self.user.get_hand().sort()
        self.draw()