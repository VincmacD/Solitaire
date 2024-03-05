from pile_type import Order, PileType

class Pile:
    """
    Attributes:
        cards (list): A list of Card objects in the pile.
        x (int): The x-coordinate of the pile's position.
        y (int): The y-coordinate of the pile's position.
        card_size (tuple): The width and height of the cards in the pile.
        pile_type (PileType): The type of the pile, influencing its behavior and appearance.
    """
    def __init__(self, cards, x, y, card_size, pile_type=PileType.TABLEAU):
       
        # Physical attributes of the pile and its cards.
        self.card_width, self.card_height = card_size  
        self.x, self.y = x, y  

        # Pile-specific behaviors and properties.
        self.pile_type = pile_type  
        self.fanned = pile_type == PileType.TABLEAU
        self.discovered = True if pile_type == PileType.TABLEAU else None
    
        # Spacing configuration for laying out cards in the pile.
        self.card_spacing = 25
        self.bottom_margin = 10 
        
        # The cards that belong to this pile.
        self.cards = cards

        # Update the pile to apply initial settings.
        self.update()  
    
    @property
    def pile_bottom_card(self):
        # Calculates and returns the y-coordinate of the bottom of the pile.
        return self.cards[-1].position[1] + self.card_height

    def update_faces(self):
        # Updates the face-up or face-down state of cards in the pile based on the pile's discovery attribute.
        if self.cards:
            for card in self.cards:
                card.discovered = self.discovered if self.discovered is not None else card.discovered

    def update_positions(self):
        # Updates the positions of the cards in the pile, spacing them vertically if the pile is fanned.
        if self.cards:
            for index, card in enumerate(self.cards):
                card.position = (self.x, self.y + (index * self.card_spacing)) if self.fanned else (self.x, self.y)

    def update(self):
        # Updates the faces and positions of the cards in the pile to reflect any changes in the pile's state.
        self.update_faces()
        self.update_positions()

    def is_mouse_over(self, mouse_pos):
            x, y = mouse_pos
            # Assuming the pile's position is the bottom left of the fanned cards
            pile_height = self.card_height + (len(self.cards) - 1) * self.card_spacing if self.fanned else self.card_height
            return self.x <= x <= self.x + self.card_width and self.y <= y <= self.y + pile_height
    