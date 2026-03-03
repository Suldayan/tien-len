from src.suit import SUIT
from src.rank import RANK

class CARD:
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
    
    def toggle_selected(self):
        self.selected = not self.selected

    def render(self, canvas, x, y, click_callback=None):
        width = 100
        height = 150

        # Move up if selected
        if self.selected:
            y -= 20

        color = "red" if self.suit.name in ["Hearts", "Diamonds"] else "black"

        tag = f"card_{id(self)}"

        # Card border
        canvas.create_rectangle(
            x - width//2, y - height//2,
            x + width//2, y + height//2,
            fill="white",
            outline="black",
            width=2,
            tags=tag
        )

        # Middle symbol
        canvas.create_text(
            x, y,
            text=self.suit.symbol,
            fill=color,
            font=(self.COURIER_NEW, 48),
            tags=tag
        )

        # Top left
        canvas.create_text(
            x - 35, y - 55,
            text=self.rank.label,
            fill=color,
            font=(self.TIMES_NEW_ROMAN, 18),
            tags=tag
        )

        canvas.create_text(
            x - 35, y - 35,
            text=self.suit.symbol,
            fill=color,
            font=(self.COURIER_NEW, 18),
            tags=tag
        )

        # Bottom right
        canvas.create_text(
            x + 35, y + 55,
            text=self.rank.label,
            fill=color,
            font=(self.TIMES_NEW_ROMAN, 18),
            tags=tag
        )

        canvas.create_text(
            x + 35, y + 35,
            text=self.suit.symbol,
            fill=color,
            font=(self.COURIER_NEW, 18),
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