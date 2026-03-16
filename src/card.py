from src.suit import SUIT
from src.rank import RANK


class CARD:
    WIDTH = 100
    HEIGHT = 150

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
        return (
            self.rank.value == other.rank.value and
            self.suit.SuitRank == other.suit.SuitRank
        )

    def __str__(self):
        return f"{self.rank} of {self.suit}"
    
    def __repr__(self): 
        return f"{self.rank.label}{self.suit.symbol}"
    
    def strength(self):
        return self.rank.value * 10 + self.suit.SuitRank
    
    def toggle_selected(self):
        self.selected = not self.selected


    def render(self, canvas, x, y,width=None, height=None, click_callback=None, ignore_selected=False):
        w = width if width else self.WIDTH
        h = height if height else self.HEIGHT


        # Move up if selected
        if self.selected and not ignore_selected:
            y -= 20

        color = "red" if self.suit.name in ["Hearts", "Diamonds"] else "black"

        tag = f"card_{id(self)}"

        # Card border
        canvas.create_rectangle(
            x - w//2, y - h//2,
            x + w//2, y + h//2,
            fill="white",
            outline="black",
            width= 1 if width else 2,
            tags=tag
        )
        middle_font_size = int(h * 0.45)
        # Middle symbol
        canvas.create_text(
            x, y,
            text=self.suit.symbol,
            fill=color,
            font=(self.COURIER_NEW, middle_font_size),
            tags=tag
        )
        #Dynamic font size offset
        rank_font = int(h*0.20)
        suit_font = int(h*0.20)
        #Dynamic scaling_offset 
        ox = w * 0.35
        oy1 = h * 0.17
        oy2 = h *0.35

        # Top left
        canvas.create_text(
            x - ox, y - oy2,
            text=self.rank.label,
            fill=color,
            font=(self.TIMES_NEW_ROMAN, rank_font),
            tags=tag
        )

        canvas.create_text(
            x - ox, y - oy1,
            text=self.suit.symbol,
            fill=color,
            font=(self.COURIER_NEW, suit_font),
            tags=tag
        )

        # Bottom right
        canvas.create_text(
            x + ox, y + oy2,
            text=self.rank.label,
            fill=color,
            font=(self.TIMES_NEW_ROMAN, rank_font),
            tags=tag
        )

        canvas.create_text(
            x + ox, y + oy1,
            text=self.suit.symbol,
            fill=color,
            font=(self.COURIER_NEW, suit_font),
            tags=tag
        )

        # Bind click
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
