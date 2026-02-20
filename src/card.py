class CARD:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

        self.COURIER_NEW = "Courier New"
        self.TIMES_NEW_ROMAN = "Times New Roman"

    def __str__(self):
        return f"{self.rank} of {self.suit}"

    def render(self, canvas, x, y):
        width = 100
        height = 150

        color = "red" if self.suit.name in ["Hearts", "Diamonds"] else "black"

        # card border
        canvas.create_rectangle(
            x - width//2, y - height//2,
            x + width//2, y + height//2,
            fill="white",
            outline="black",
            width=2
        )

        # middle symbol
        self.draw_text(canvas, x, y, self.suit.symbol, color, self.COURIER_NEW, 48, 0, 0)

        # top left
        self.draw_text(canvas, x, y, self.rank.label, color, self.TIMES_NEW_ROMAN, 18, -35, -55)
        self.draw_text(canvas, x, y, self.suit.symbol, color, self.COURIER_NEW, 18, -35, -35)

        # bottom right
        self.draw_text(canvas, x, y, self.rank.label, color, self.TIMES_NEW_ROMAN, 18, 35, 55)
        self.draw_text(canvas, x, y, self.suit.symbol, color, self.COURIER_NEW, 18, 35, 35)
        

    def draw_text(self, canvas, base_x, base_y, text, color, font, size, offset_x, offset_y):
        canvas.create_text(
            base_x + offset_x,
            base_y + offset_y,
            text=text,
            fill=color,
            font=(font, size)
        )

