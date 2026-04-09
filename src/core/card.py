from src.core.suit import SUIT
from src.core.rank import RANK
from PIL import Image, ImageTk
import os



class CARD:
    WIDTH = 100
    HEIGHT = 150

    image_cache = {}  

    def get_image(self, target_width):
        target_width = int(target_width)
        ratio = 80 / 56 
        target_height = int(target_width * ratio)

        key = (repr(self), target_width)

        if key not in CARD.image_cache:
            path = f"src/assets/{repr(self)}.png"
            img = Image.open(path)
            img = img.resize((target_width, target_height), Image.NEAREST)
            CARD.image_cache[key] = ImageTk.PhotoImage(img)

        return CARD.image_cache[key]
    
    
    @classmethod
    def get_back_image(cls, target_width):
        target_width = int(target_width)
        ratio = 80 / 56
        target_height = int(target_width * ratio)
        
        key = ("BACK", target_width, target_height)

        if key not in cls.image_cache: # cls from @classmethod 
            path = "src/assets/cardsBack.png"
            img = Image.open(path)
            
            img = img.resize((target_width, target_height), Image.NEAREST)
            cls.image_cache[key] = ImageTk.PhotoImage(img)

        return cls.image_cache[key]

    def __init__(self, suit: SUIT, rank: RANK):
        self.suit = suit
        self.rank = rank
        self.selected = False

        self.COURIER_NEW = "Courier New"
        self.TIMES_NEW_ROMAN = "Times New Roman"

    def __lt__(self, other):
        # Compare rank first
        if self.rank.value != other.rank.value:
            return self.rank.value < other.rank.value

        # If ranks are equal, compare suit rank
        return self.suit.SuitRank < other.suit.SuitRank

    def __eq__(self, other):
        if other is None:
            return False
        return (self.rank.value == other.rank.value and 
                self.suit.name == other.suit.name)

    def __str__(self):
        return f"{self.rank} of {self.suit}"
    
    def __repr__(self): 
        return f"{self.rank.label}{self.suit.code}"
    
    def strength(self):
        return self.rank.value * 10 + self.suit.SuitRank
    
    def toggle_selected(self):
        self.selected = not self.selected


    def render(self, canvas, x, y, width=None, height=None, click_callback=None, ignore_selected=False):
        w = int(width) if width else self.WIDTH

        img = self.get_image(w)

        h = img.height()

        #scale lift with size
        if self.selected and not ignore_selected:
            y -= int(h * 0.15)

        tag = f"card_{id(self)}"

        canvas.create_image(
            x, y,
            image=img,
            tags=tag,
            anchor = "nw"
        )

        # prevent garbage collection
        if not hasattr(canvas, "images"):
            canvas.images = []

        canvas.images.append(img)

        if click_callback:
            canvas.tag_bind(tag, "<Button-1>", lambda e: click_callback(self))

        

    def draw_text(self, canvas, base_x, base_y, text, color, font, size, offset_x, offset_y):
        canvas.create_text(
            base_x + offset_x,
            base_y + offset_y,
            text=text,
            fill=color,
            font=(font, size)
        )
    
    def card_clicked(self, ui):
        if ui.is_paused:
            return
        if not ui.user.is_turn():
            return
        self.toggle_selected()
        ui.render_manager.draw()
