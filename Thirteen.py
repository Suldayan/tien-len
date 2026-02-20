import random
import tkinter as tk


class SUIT:
    def __init__(self, name, SuitRank, symbol):
        self.name = name
        self.SuitRank = SuitRank
        self.symbol = symbol

    def __str__(self):
        return self.name


class RANK:
    def __init__(self, name, value, label):
        self.name = name
        self.value = value
        self.label = label

    def __str__(self):
        return self.label


class CARD:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank} of {self.suit}"

    def render(self, canvas, x, y):
        width = 100
        height = 150

        #color
        if self.suit.name in ["Hearts", "Diamonds"]:
            color = "red"
        else:
            color = "black"

        #card border
        canvas.create_rectangle(
            x - width//2, y - height//2,
            x + width//2, y + height//2,
            fill="white",
            outline="black",
            width=2
        )

        #middle symbol
        canvas.create_text(
            x, y,
            text=self.suit.symbol,
            fill=color,
            font=("Courier New", 48)
        )

        #top left
        canvas.create_text(
            x - 35, y - 55,
            text=self.rank.label,
            fill=color,
            font=("Times New Roman", 18)
        )

        canvas.create_text(
            x - 35, y - 35,
            text=self.suit.symbol,
            fill=color,
            font=("Courier New", 18)
        )

        #bottom right
        canvas.create_text(
            x + 35, y + 55,
            text=self.rank.label,
            fill=color,
            font=("Times New Roman", 18)
        )

        canvas.create_text(
            x + 35, y + 35,
            text=self.suit.symbol,
            fill=color,
            font=("Courier New", 18)
        )


class DECK:
    def __init__(self):
        self.suits = [
            SUIT("Hearts", 4, "♥"),
            SUIT("Spades", 1, "♠"),
            SUIT("Clubs", 2, "♣"),
            SUIT("Diamonds", 3, "♦")
        ]

        self.ranks = [
            RANK("ACE", 12, "A"), RANK("TWO", 13, "2"),
            RANK("THREE", 1, "3"), RANK("FOUR", 2, "4"),
            RANK("FIVE", 3, "5"), RANK("SIX", 4, "6"),
            RANK("SEVEN", 5, "7"), RANK("EIGHT", 6, "8"),
            RANK("NINE", 7, "9"), RANK("TEN", 8, "10"),
            RANK("JACK", 9, "J"), RANK("QUEEN", 10, "Q"),
            RANK("KING", 11, "K")
        ]

        self.cards = [CARD(suit, rank)
                      for rank in self.ranks
                      for suit in self.suits]


def main():
    deck = DECK()

    root = tk.Tk()
    root.title("Card Demo")

    canvas = tk.Canvas(root, width=800, height=600, bg="green")
    canvas.pack()

    # Draw 13 randoms cards
    sample_cards = random.sample(deck.cards, 13)

    x_position = 100
    for card in sample_cards:
        card.render(canvas, x_position, 500)
        x_position += 50

    root.mainloop()


main()
