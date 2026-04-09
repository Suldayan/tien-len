import tkinter as tk

class MenuScreen(tk.Frame):
    def __init__(self, root, start_game_callback):
        super().__init__(root, bg = "#14532d")

        container = tk.Frame(self, bg = "#14532d")
        container.place(relx=0.5, rely=0.4, anchor="center")

        label = tk.Label(
            container,
            text="13 CARD",
            font=("Perfect DOS VGA 437", 80, "bold"),
            bg = "#14532d",
            fg="white"
        )
        label.pack(pady=(0, 100))  # reasonable gap between title and button

        new_game_button = tk.Button(
            container,
            text="NEW GAME",
            font=("Perfect DOS VGA 437", 25, "bold"),
            bg="#1a1a1a",
            fg="#e6e6e6",
            activebackground="#333333",
            activeforeground="white",
            bd=4,
            relief="ridge",
            padx=40,
            pady=15,
            cursor="hand2",         
            command=start_game_callback
        )
        new_game_button.pack()

        # Hover effect
        new_game_button.bind("<Enter>", lambda e: new_game_button.config(bg="#333333"))
        new_game_button.bind("<Leave>", lambda e: new_game_button.config(bg="#1a1a1a"))