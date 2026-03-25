import tkinter as tk

class TutorialOverlay:
    def __init__(self, parent_window):
        # parent_window is the main game window
        self.parent = parent_window
        

        self.canvas = tk.Canvas(self.parent, bg="green", highlightthickness=0)
        self.rect_id = None
        self.text_id = None

        # 2 Bind the click event to the whole canvas
        self.canvas.bind("<Button-1>", self.on_click)

        #Variables
        self.is_visible = False
        self.on_dismiss_callback = None 
        self.dismissible = True 

    def _create_round_rect(self, x1, y1, x2, y2, radius=25, **kwargs):
        """Helper method to draw a rounded rectangle on a Tkinter canvas."""
        points = [
            x1+radius, y1, x1+radius, y1, x2-radius, y1, x2-radius, y1,
            x2, y1, x2, y1+radius, x2, y1+radius, x2, y2-radius,
            x2, y2-radius, x2, y2, x2-radius, y2, x2-radius, y2,
            x1+radius, y2, x1+radius, y2, x1, y2, x1, y2-radius,
            x1, y2-radius, x1, y1+radius, x1, y1+radius, x1, y1
        ]
        # smooth=True 
        return self.canvas.create_polygon(points, **kwargs, smooth=True)

    def show(self, message, on_dismiss=None, dismissible=True):
        """Pops the overlay onto the screen with a newly sized rounded box."""
        self.on_dismiss_callback = on_dismiss
        # clear anything drawn previously
        self.canvas.delete("all") 
        
        # Create the text first 
        self.text_id = self.canvas.create_text(
            0, 0, 
            text=message, 
            font=("Helvetica", 12, "bold"), 
            fill="black",
            width=600,     #wrapping     
            justify="center",
            anchor="center"
        )
        
        # Get the exact width and height of the text block
        bbox = self.canvas.bbox(self.text_id)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Add padding for breathing room
        pad_x, pad_y = 15, 10
        box_width = text_width + (pad_x * 2)
        box_height = text_height + (pad_y * 2)
        
        # resize the canvas to fit our new box perfectly
        self.canvas.config(width=box_width, height=box_height)
        
        # Draw the rounded rectangle 
        self.rect_id = self._create_round_rect(
            3, 3, box_width-1, box_height-1, #border thickess padding
            radius=20, 
            fill="#FFFFFF", 
            outline="#000000", 
            width=2
        )
        
        # move the text to the exact center of our new box and pull it to the front
        self.canvas.coords(self.text_id, box_width/2, box_height/2)
        self.canvas.tag_raise(self.text_id)
        
        # 7. Place the canvas in the center of the screen
        self.canvas.place(relx=0.5, rely=0.63, anchor="center")

        self.parent.update_idletasks()
        self.is_visible = True



    def hide(self):
        """Removes the overlay from the screen."""
        self.canvas.place_forget()
        self.is_visible = False

    def on_click(self, event):
        """Fires when the user clicks the overlay."""
        if self.is_visible and self.dismissible:
            self.hide()
            
            # If the game told us to do something after the click, do it right now
            if self.on_dismiss_callback:
                self.on_dismiss_callback()