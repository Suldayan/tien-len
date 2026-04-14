import pytest
from src.core.card import CARD
from src.core.suit import SUIT
from src.core.rank import RANK
from src.core.combo import make_combo
from src.core.player import Player
from src.core.hand import Hand
from src.game.game import Game

SUIT_DATA = {
    "spades":   ("Spades",   1, "♠", "S"),
    "clubs":    ("Clubs",    2, "♣", "C"),
    "diamonds": ("Diamonds", 3, "♦", "D"),
    "hearts":   ("Hearts",   4, "♥", "H"),
}
SUITS = list(SUIT_DATA.keys())  

RANK_DATA = {
    "THREE": (1,  "3"), "FOUR":  (2,  "4"), "FIVE":  (3,  "5"),
    "SIX":   (4,  "6"), "SEVEN": (5,  "7"), "EIGHT": (6,  "8"),
    "NINE":  (7,  "9"), "TEN":   (8,  "10"),"JACK":  (9,  "J"),
    "QUEEN": (10, "Q"), "KING":  (11, "K"), "ACE":   (12, "A"),
    "TWO":   (13, "2"),
}
RANK_BY_VALUE = {v[0]: k for k, v in RANK_DATA.items()}

def make_card(rank_name, suit_name="spades"):
    s, sr, sy, sc = SUIT_DATA[suit_name]
    val, sym = RANK_DATA[rank_name]
    return CARD(SUIT(s, sr, sy, sc), RANK(rank_name, val, sym))

def make_cards(*rank_names_or_vals):
    result = []
    for r in rank_names_or_vals:
        if isinstance(r, int):
            r = RANK_BY_VALUE[r]
        result.append(make_card(r))
    return result

def make_single(rank_name, suit_name="spades"):
    return make_combo([make_card(rank_name, suit_name)])

def make_pair(rank_name, suit1="spades", suit2="diamonds"):
    return make_combo([make_card(rank_name, suit1), make_card(rank_name, suit2)])

def make_triple(rank_name):
    return make_combo([make_card(rank_name, s) for s in ["spades", "clubs", "diamonds"]])

def make_quad(rank_name):
    return [make_card(rank_name, s) for s in SUITS]

def make_straight(rank_names, suits=None):
    suits = suits or ["spades"] * len(rank_names)
    return make_combo([make_card(r, s) for r, s in zip(rank_names, suits)])

def make_double_straight(rank_names, suit1="spades", suit2="diamonds"):
    cards = [make_card(r, s) for r in rank_names for s in [suit1, suit2]]
    return make_combo(cards)

def make_player(name, rank_names):
    hand = Hand([])  
    for r in rank_names:
        hand.add(make_card(r))
    return Player(name, hand)  

def make_game(player_hands: list[list[str]]):
    """
    Build a Game with N players, each holding the specified ranks.
    e.g. make_game([["THREE","FOUR"], ["FIVE","SIX"]])
    """
    players = [make_player(f"P{i}", hands) for i, hands in enumerate(player_hands)]
    game = Game(players)
    game.current_index = 0
    return game

class MockGame:
    def __init__(self, combo):
        self.current_combo = combo

@pytest.fixture
def empty_game():
    return MockGame(None)