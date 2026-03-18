class RenderManager:
    def __init__(self, ui):
        self.ui = ui

    def draw_cards(self, canvas, cards):
        canvas.update_idletasks()
        canvas.delete("all")

        num_cards = len(cards)
        if num_cards == 0:
            return

        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()

        total_width = num_cards * self.ui.CARD_WIDTH + (num_cards - 1) * self.ui.CARD_GAP
        start_x = (canvas_width - total_width) // 2 + self.ui.CARD_WIDTH // 2
        y = canvas_height // 2

        for i, card in enumerate(cards):
            x = start_x + i * (self.ui.CARD_WIDTH + self.ui.CARD_GAP)
            if canvas == self.ui.user_canvas:
                card.render(canvas, x, y, click_callback=self.ui.card_clicked)
            else:
                self.ui.render_back(canvas, x, y)

    def draw_hint_card(self, canvas, combo_obj, current_x, current_y, canvas_width, canvas_height):
        scale = 0.65
        mini_w = self.ui.CARD_WIDTH * scale
        mini_h = self.ui.CARD_HEIGHT * scale
        
        padding_left = 15
        card_overlap = -int(mini_w * 0.4)
        combo_gap = 25

        num_cards = len(combo_obj.cards)
        total_combo_width = mini_w + (num_cards - 1) * (mini_w + card_overlap)

        if current_x + total_combo_width > (canvas_width - 10):
            # Move the whole group to the next row
            current_x = padding_left + (mini_w // 2)
            current_y += (mini_h + 15)
        
        #if the combos exceeding the height of canvas, it won't show the next combos
        if current_y + mini_h > (canvas_height - 10):
            return None, None 

        for card in combo_obj.cards:
            card.render(canvas, current_x, current_y, width=mini_w, height=mini_h, ignore_selected = True)
            current_x += (mini_w + card_overlap)

        
        
        return (current_x - card_overlap + combo_gap), current_y