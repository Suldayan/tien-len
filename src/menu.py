import tkinter as tk

class MenuScreen(tk.Frame):
    def __init__(self, root, start_game_callback):
        super().__init__(root, bg="green")

        # This frame centers everything vertically and horizontally
        container = tk.Frame(self, bg="green")
        container.place(relx=0.5, rely=0.5, anchor="center")

        # Welcome text slightly above center
        label = tk.Label(
            container,
            text="Welcome to 13 card tutorial !",
            font=("Arial", 32),
            bg="green",
            fg="white"
        )
        label.pack(pady=(0, 30))  # push button downward a bit

        # New Game button exactly centered
        button_bg = "#1a1a1a"      # dark charcoal
        button_fg = "#e6e6e6"      # soft white
        button_border = "#cccccc"  # light border

        new_game_button = tk.Label(
            container,
            text="NEW GAME",
            font=("Arial", 22, "bold"),
            bg=button_bg,
            fg=button_fg,
            bd=4,
            relief="ridge",
            padx=40,
            pady=15
        )
        new_game_button.pack()

        # Hover effect
        def on_enter(e):
            new_game_button.config(bg="#333333", fg="white", bd=5)

        def on_leave(e):
            new_game_button.config(bg=button_bg, fg=button_fg, bd=4)

        new_game_button.bind("<Enter>", on_enter)
        new_game_button.bind("<Leave>", on_leave)

        new_game_button.bind("<Button-1>", lambda e: start_game_callback())
