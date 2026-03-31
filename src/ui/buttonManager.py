import tkinter as tk

class ButtonManager:
    def __init__(self, parent_frame, on_arrange, on_play, on_pass):
        self.frame = tk.Frame(parent_frame, bg="green")
        self.frame.pack(side="bottom", fill="x", pady=5)

        # using RoundedButton instead of tk.Button
        self.arrange_btn = RoundedButton(self.frame, text="Arrange", command=on_arrange)
        self.arrange_btn.pack(side="left", expand=True, padx=5, pady=5)

        self.play_btn = RoundedButton(self.frame, text="Play", command=on_play)
        self.play_btn.pack(side="left", expand=True, padx=5, pady=5)

        self.pass_btn = RoundedButton(self.frame, text="Pass", command=on_pass)
        self.pass_btn.pack(side="left", expand=True, padx=5, pady=5)


class RoundedButton:
    # custom Tkinter button with rounded corners using a Canvas
    def __init__(self, parent, text, command, width=100, height=40, radius=20, 
                 bg_color="#ffffff", hover_color="#dddddd", text_color="black", 
                 font=("Pixelify Sans", 20), parent_bg="green", outline_color="black", outline_width=2):
        
        self.command = command
        self.bg_color = bg_color
        self.hover_color = hover_color
        
        # canvas needs the same background as the frame so the corners blend in the background
        self.canvas = tk.Canvas(parent, width=width, height=height, bg=parent_bg, 
                                highlightthickness=0, cursor="hand2")
        
        # draw the rounded rectangle
        self.rect_id = self._create_round_rect(3, 3, width-3, height-3, radius=radius, fill=bg_color,outline=outline_color, 
            width=outline_width)
        
        # draw the text in the center
        self.text_id = self.canvas.create_text(width/2, height/2, text=text, fill=text_color, font=font)
        
        # bind events for clicking
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<Enter>", self.on_hover)
        self.canvas.bind("<Leave>", self.on_leave)
        
        # bind clicking on the text itself
        self.canvas.tag_bind(self.text_id, "<Button-1>", self.on_click)

    def _create_round_rect(self, x1, y1, x2, y2, radius=25, **kwargs):
        #logic for drawing rounded rectangle
        points = [
            x1+radius, y1, x1+radius, y1, x2-radius, y1, x2-radius, y1,
            x2, y1, x2, y1+radius, x2, y1+radius, x2, y2-radius,
            x2, y2-radius, x2, y2, x2-radius, y2, x2-radius, y2,
            x1+radius, y2, x1+radius, y2, x1, y2, x1, y2-radius,
            x1, y2-radius, x1, y1+radius, x1, y1+radius, x1, y1
        ]
        return self.canvas.create_polygon(points, **kwargs, smooth=True)

    def on_hover(self, event):
        self.canvas.itemconfig(self.rect_id, fill=self.hover_color)

    def on_leave(self, event):
        self.canvas.itemconfig(self.rect_id, fill=self.bg_color)

    def on_click(self, event):
        self.command()

    def pack(self, **kwargs):
        self.canvas.pack(**kwargs)
