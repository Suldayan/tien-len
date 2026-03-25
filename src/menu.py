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
            text="Welcome",
            font=("Arial", 32),
            bg="green",
            fg="white"
        )
        label.pack(pady=(0, 30))  # push button downward a bit

        # New Game button exactly centered
        new_game_button = tk.Button(
            container,
            text="New Game",
            font=("Arial", 20),
            command=start_game_callback
        )
        new_game_button.pack()