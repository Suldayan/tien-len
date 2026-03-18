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
                self.render_back(canvas, x, y)

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

    def draw(self):
        self.ui.update_player_info()
        self.ui.render_manager.draw_cards(self.ui.bot_canvas, self.ui.bot.get_hand().get_cards())
        self.ui.render_manager.draw_cards(self.ui.user_canvas, self.ui.user.get_hand().get_cards())
        #fixed: always clear the middle table before redrawing
        self.ui.table_canvas.delete("all")
        self.ui.hint_canvas.delete("all")

        #get all the playable hands from Game class's function "fectch_all_playable_hands"
        playable_hands = self.ui.cached_playable_hands


        self.ui.hint_canvas.update_idletasks()
        c_width = self.ui.hint_canvas.winfo_width()
        c_height = self.ui.hint_canvas.winfo_height()
        if c_width <= 1: c_width = 180 # Fallback for startup
        
        scale = 0.65
        h_x = 15 + (self.ui.CARD_WIDTH * scale // 2)
        h_y = 70

        for hand in playable_hands:
            # pass the positions and get to the updated ones
            result = self.ui.render_manager.draw_hint_card(self.ui.hint_canvas, hand, h_x, h_y, c_width, c_height)

            if result == (None, None):
                break
            
            h_x, h_y = result

        if self.ui.game.current_combo:
            #fixed: target the middle canvas instead of bot_canvas
            self.ui.table_canvas.update_idletasks()

            width = self.ui.table_canvas.winfo_width()
            height = self.ui.table_canvas.winfo_height()

            cards = self.ui.game.current_combo.cards

            #spacing for played cards on the table
            played_card_spacing = 60

            #calculate total width of the played group
            #assuming render draws from center x
            if len(cards) > 1:
                total_group_width = (len(cards) - 1) * played_card_spacing
            else:
                total_group_width = 0

            start_x = (width // 2) - (total_group_width // 2)
            center_y = height // 2

            for i, card in enumerate(cards):
                x = start_x + i * played_card_spacing
                #fixed: Render the card onto table_canvas
                card.render(self.ui.table_canvas, x, center_y)

    def render_back(self, canvas, x, y):
        from src.card import CARD
        width = CARD.WIDTH
        height = CARD.HEIGHT

        #Draw card background
        canvas.create_rectangle(
        x - width//2, y - height//2,
        x + width//2, y + height//2,
        fill="#1E3A8A",   # deep blue
        outline="white",
        width=3
        )

        #Optional: add a pattern or symbol
        canvas.create_text(
        x, y,
        text="★",
        fill="white",
        font=("Arial", 40)
        )