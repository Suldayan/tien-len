import tkinter as tk

class Layout:
    def __init__(self, root, theme, card_height):
        self.root = root
        self.theme = theme
        self.card_height = card_height
        self.build()

    def build(self):
        """Creates the zones: Top, Middle, and Bottom"""
        bg = self.theme.get("bg", "#14532d")
        
        # TOP ZONE: Bot
        self.top_frame = tk.Frame(self.root, bg=bg)
        self.top_frame.pack(side="top", fill="x")
        
        self.bot_label = tk.Label(self.top_frame, font=("Perfect DOS VGA 437", 20), bg=bg, fg="white")
        self.bot_label.pack(pady=10)

        self.bot_canvas = tk.Canvas(self.top_frame, bg=bg, highlightthickness=0, height=self.card_height)
        self.bot_canvas.pack(fill="both", expand=True, padx=10)

        # BOTTOM ZONE: User Controls & Cards
        self.bottom_frame = tk.Frame(self.root, bg=bg)
        self.bottom_frame.pack(side="bottom", fill="x")

        self.user_zone = tk.Frame(self.bottom_frame, bg=bg)
        self.user_zone.pack(fill="x", padx=10, pady=(5, 0))

        # MIDDLE ZONE: The Table
        self.mid_frame = tk.Frame(self.root, bg=bg)
        self.mid_frame.pack(fill="both", expand=True)

        self.table_canvas = tk.Canvas(self.mid_frame, bg=bg, highlightthickness=0)
        self.table_canvas.place(relx=0, rely=0, relwidth=1.0, relheight=1.0)

        self.hint_canvas = tk.Canvas(self.mid_frame, bg = bg, highlightthickness=0)
        self.hint_canvas.place(relx=0, rely=0, relwidth=0.2, relheight=0.7)

        self.user_canvas = tk.Canvas(self.user_zone, bg = bg, highlightthickness=0, bd=0,
                             height=self.card_height + 40)
        self.user_canvas.pack(fill="x")
