from src.core.player import Player

class Bot(Player):
    def __init__(self, name, hand=None, points=0):
        super().__init__(name, hand, points)

    def make_move(self, game):
        playable = game.fetch_all_playable_hands(self)

        # Case 1: No valid moves, pass
        if not playable:
            return None

        # Case 2: Table is empty, pick a random combo type but play the weakest of that type
        if game.current_combo is None:
            from random import choice

            # Group playable combos by type
            combo_types = {}
            for combo in playable:
                if combo.combo_type not in combo_types:
                    combo_types[combo.combo_type] = []
                combo_types[combo.combo_type].append(combo)

            # Pick a random type, then play the weakest of that type
            chosen_type = choice(list(combo_types.keys()))
            best = min(combo_types[chosen_type], key=lambda combo: max(combo.cards, key=lambda c: c.strength()).strength())
            return best.cards

        # Case 3: Table has a combo — apply strategy to find best candidate
        safe_to_play = [
            combo for combo in playable
            if not any(c.rank.value == 13 for c in combo.cards)
            and combo.combo_type != "PAIR"
        ]
        candidates = safe_to_play if safe_to_play else playable

        table_strength = max(game.current_combo.cards, key=lambda c: c.strength()).strength()
        threshold = 25 if game.current_combo.combo_type == "SINGLE" else 15

        within_threshold = [
            combo for combo in candidates
            if max(combo.cards, key=lambda c: c.strength()).strength() - table_strength <= threshold
        ]
        candidates = within_threshold if within_threshold else candidates

        best = min(candidates, key=lambda combo: max(combo.cards, key=lambda c: c.strength()).strength())
        return best.cards