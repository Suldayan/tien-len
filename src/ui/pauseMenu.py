import tkinter as tk
class PauseMenu:
    def __init__(self, ui):
        self.ui = ui
        self.root = ui.root
        self.bg = ui.MainBG
        
        self.pause_menu = tk.Frame(self.root, bg=self.bg)
        
        self.pause_panel = tk.Frame(self.pause_menu, bg=self.bg)
        self.pause_panel.place(relx=0.5, rely=0.5, anchor="center")
        
        # Title
        self.pause_title = tk.Label(
            self.pause_panel,
            text="Pause Menu",
            font=("Perfect DOS VGA 437", 40, "bold"),
            fg="white",
            bg=self.bg
        )
        self.pause_title.pack(pady=(0, 25))
        
        # Resume 
        self.resume_menu_button = tk.Button(
            self.pause_panel,
            text="Resume",
            font=("Perfect DOS VGA 437", 20, "bold"),
            width=18,
            bg="#e6e6e6",
            fg="black",
            command=self.ui.resume_game
        )
        self.resume_menu_button.pack(pady=8)
        
        # New Game 
        self.new_game_menu_button = tk.Button(
            self.pause_panel,
            text="New Game",
            font=("Perfect DOS VGA 437", 20, "bold"),
            width=18,
            bg="#e6e6e6",
            fg="black",
            command=self.ui.pause_menu_new_game
        )
        self.new_game_menu_button.pack(pady=8)
        
        # Quit 
        self.quit_menu_button = tk.Button(
            self.pause_panel,
            text="Quit",
            font=("Perfect DOS VGA 437", 20, "bold"),
            width=18,
            bg="#e6e6e6",
            fg="black",
            command=self.root.destroy
        )
        self.quit_menu_button.pack(pady=8)
    
    def hide(self):
        self.pause_menu.place_forget()
    
    def show(self):
        self.pause_menu.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.pause_menu.lift()