import os

# Constants for sizing
CARD_SCALE = 0.6

# How big are the cards?
CARD_WIDTH = 140 * CARD_SCALE
CARD_HEIGHT = 190 * CARD_SCALE

# Card constants
CARD_VALUES = ["ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king"]
CARD_SUITS = ["clubs", "hearts", "spades", "diamonds"]

# Value Map use to verify move validation in the Deck class
CARD_VALUE_MAP = {
    "ace": 1, "2": 2, "3": 3, "4": 4,
    "5": 5, "6": 6, "7": 7, "8": 8,
    "9": 9, "10": 10, "jack": 11,
    "queen": 12, "king": 13
}

class Card:
    """ 
    Attributes:
        name_of_card (str): name of the card based on the images.png found in resources/cards
        suit (str): The suit of the card ('clubs', 'hearts', 'spades', 'diamonds').
        value (str): The face value of the card ('ace' through 'king').
        discovered (bool): Whether the card is face up (discovered) or face down.
        position (tuple): The (x, y) screen position of the card.
    """
 
    def __init__(self, name_of_card, card_size, suit, value, discovered=False):
        # Basic card attributes
        self.name_of_card = name_of_card 
        self.suit = suit 
        self.value = value
        self.discovered = discovered

        #Image and appearance
        self.card_size = card_size
       
        # Initial position is set to (0, 0) but can be updated to move the card on the screen.
        self.position = (0, 0)
    
    @property
    def color(self):
        if self.suit in ['hearts', 'diamonds']:
            return 'red'
        else:
            return 'black'
        
    @property
    def x(self):
        # Returns the x-coordinate of the card's position.
        return self.position[0]

    @property
    def y(self):
        # Returns the y-coordinate of the card's position.
        return self.position[1]
    
    def set_position(self, x, y):
        # Set the card's position on the game screen.
        self.position = (x, y)
    
    def is_mouse_over(self, mouse_pos):
        #Checks if the mouse is over the card.
        x, y = mouse_pos
        return self.x <= x <= self.x + self.card_size[0] and self.y <= y <= self.y + self.card_size[1]