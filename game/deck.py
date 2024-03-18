import os
import random
import pygame
from pile import *
from card import *
from pile_type import *
import sys

# Directory of the current script
script_dir = os.path.dirname(__file__)

# Path for the cards' images
back_of_card = os.path.join(script_dir, "resources", "miscellaneous", "card_back.jpg")
cards_dir = os.path.join(script_dir,'resources', 'cards') 

class Deck:
    #Represents the deck of cards in the game
    def __init__(self, card_size=(CARD_WIDTH, CARD_HEIGHT)):
        self.cards = [] # List of Card objects
        self.suits = CARD_SUITS
        self.values = CARD_VALUES
        self.mat_color = (136, 191, 134)
        self.piles = [] # List of Pile objects
        self.card_images = {} # Dictionary to store card images
        self.card_size = card_size

        # Load back of card image and resize
        self.back_image_of_card = pygame.image.load(back_of_card)
        self.back_image_of_card = self.resize_back_image_of_card()
    
    
    def resize_back_image_of_card(self):
        return pygame.transform.scale(self.back_image_of_card, self.card_size)

    def resize_card_images(self):
        for name_of_card, card_image in self.card_images.items():
            self.card_images[name_of_card] = pygame.transform.scale(card_image, self.card_size)

    def load_cards(self):
        # Loads card images from resources and creates Card objects for each suit and value.
        for suit in self.suits:
            for value in self.values:
                filename = f'{value}_of_{suit}.png'
                image_path = os.path.join(cards_dir, filename)
                try:
                    card_image = pygame.image.load(image_path)
                    resized_image = pygame.transform.scale(card_image, self.card_size)
                    # Use filename as the key to store the image
                    self.card_images[filename] = resized_image
                    # Also pass just the filename to the Card constructor
                    self.cards.append(Card(filename, self.card_size, suit, value))
                except pygame.error as e:
                    print(f"Error loading image {image_path}: {e}")
                    sys.exit(1)

    def load_piles(self, display_size):
        #Initializes the piles for the game.
        SCREEN_WIDTH, SCREEN_HEIGHT = display_size
        pile_spacing = 50
        start_x = 50
        start_y = CARD_HEIGHT + 100 

        # Initialize tableau piles
        tableau_piles = [
            (self.cards[0:1], start_x, start_y),
            (self.cards[1:3], start_x + CARD_WIDTH + pile_spacing, start_y),
            (self.cards[3:6], start_x + CARD_WIDTH*2 + pile_spacing*2, start_y),
            (self.cards[6:10], start_x + CARD_WIDTH*3 + pile_spacing*3, start_y),
            (self.cards[10:15], start_x + CARD_WIDTH*4 + pile_spacing*4, start_y),
            (self.cards[15:21], start_x + CARD_WIDTH*5 + pile_spacing*5, start_y),
            (self.cards[21:28], start_x + CARD_WIDTH*6 + pile_spacing*6, start_y),
        ]

        for cards, x, y in tableau_piles:
            tableau = Pile(cards, x, y, (CARD_WIDTH, CARD_HEIGHT))
            # Set all cards in the pile to face-down except the last one
            for card in tableau.cards[:-1]:
                card.discovered = False
            tableau.cards[-1].discovered = True
            self.piles.append(tableau)

        # Initialize stock, waste, and foundation piles
        stock = Pile(self.cards[28:], start_x, pile_spacing, (CARD_WIDTH, CARD_HEIGHT), pile_type=PileType.STOCK)
        waste = Pile([], start_x + CARD_WIDTH + pile_spacing, pile_spacing, (CARD_WIDTH, CARD_HEIGHT), pile_type=PileType.WASTE)
        foundation1 = Pile([], start_x + CARD_WIDTH*3 + pile_spacing*3, pile_spacing, (CARD_WIDTH, CARD_HEIGHT), pile_type=PileType.FOUNDATION)
        foundation2 = Pile([], start_x + CARD_WIDTH*4 + pile_spacing*4, pile_spacing, (CARD_WIDTH, CARD_HEIGHT), pile_type=PileType.FOUNDATION)
        foundation3 = Pile([], start_x + CARD_WIDTH*5 + pile_spacing*5, pile_spacing, (CARD_WIDTH, CARD_HEIGHT), pile_type=PileType.FOUNDATION)
        foundation4 = Pile([], start_x + CARD_WIDTH*6 + pile_spacing*6, pile_spacing, (CARD_WIDTH, CARD_HEIGHT), pile_type=PileType.FOUNDATION)

        # Aggregate all piles into a list
        self.piles.extend([stock, waste, foundation1, foundation2, foundation3, foundation4])

    def shuffle_cards(self):
        # Shuffles the cards in the deck.
        random.shuffle(self.cards)

    def update(self, piles_to_update):
        #Updates the specified piles or all piles if none are specified.
        for pile in self.piles:
            pile.update()
        if piles_to_update != None:
            for pile in piles_to_update:
                pile.update_positions()
            
    def get_card_at_position(self, mouse_pos):
        #Returns the card and its pile at the given mouse position
        for pile in self.piles:
            for card in reversed(pile.cards):
                if card.is_mouse_over(mouse_pos):
                    return card, pile
        return None, None

    def get_pile_at_position(self, mouse_pos):
        #determines which pile is selected and it's position
        for pile in self.piles:
            if pile.is_mouse_over(mouse_pos): 
                return pile
        return None

    def move_card(self, card, origin_pile, target_pile, score=None):
        # checks if the move is valid using the existing logic
        if not self.is_valid_move(card, origin_pile, target_pile):
            return False  # Exit if the move is not valid

        # Remove the card from the origin pile and add it to the target pile
        origin_pile.cards.remove(card)
        target_pile.cards.append(card)

        # If there are still cards in the origin pile, turn the new top card face up
        if origin_pile.cards:
            origin_pile.cards[-1].discovered = True

        # Update position of both piles
        origin_pile.update_positions()
        target_pile.update_positions()

        # Update the score if a score object is passed, when card is moved from stock pile/deck to foundation pile or tableau pile
        if score:
            # If the move is valid, increment the move count
            score.increment_move_count()

            if target_pile.pile_type == PileType.FOUNDATION:
                score.move_to_foundation()
            elif target_pile.pile_type == PileType.TABLEAU:
                score.move_to_tableau()
                score.reset_consecutive_moves()
            else: 
                score.reset_consecutive_moves()  # Reset the counter if the move is not to the foundation or tableau

        return True
    


    
    def transfer_card_from_deck_to_waste(self):
        # Find the deck and waste piles
        deck_pile = next((pile for pile in self.piles if pile.pile_type == PileType.STOCK), None)
        waste_pile = next((pile for pile in self.piles if pile.pile_type == PileType.WASTE), None)

        if deck_pile and waste_pile and deck_pile.cards:
            # Take the top card from the deck pile
            card = deck_pile.cards.pop()
            card.discovered = True  # Flip the card face up

            # Set the card's position to the waste pile's position
            card.set_position(waste_pile.x, waste_pile.y)

            waste_pile.cards.append(card) 

    def transfer_waste_to_deck(self):
       
        deck_pile = next((pile for pile in self.piles if pile.pile_type == PileType.STOCK), None)
        waste_pile = next((pile for pile in self.piles if pile.pile_type == PileType.WASTE), None)

        # Check if the stock pile is empty and the waste pile has cards
        if deck_pile and waste_pile and not deck_pile.cards and waste_pile.cards:
            # Reverse the order of cards in the waste pile to maintain the correct order when moving back to the deck
            reversed_cards = reversed(waste_pile.cards)  
            for card in reversed_cards:
                card.discovered = False 
                card.set_position(deck_pile.x, deck_pile.y)  # Set the card's position to the deck pile's position
                deck_pile.cards.append(card)
            waste_pile.cards.clear()  
        
    def is_valid_move(self, card, origin_pile, target_pile):
        # Check if the target pile is not empty
        if target_pile.cards:
            top_target_card = target_pile.cards[-1]
            
            # Ensure the move is to a tableau pile and check color and value rules
            if target_pile.pile_type == PileType.TABLEAU:
                # Different colors and the moving card's value is one less than the top card's value
                if ((card.color != top_target_card.color) and
                    (CARD_VALUE_MAP[card.value] == CARD_VALUE_MAP[top_target_card.value] - 1)):
                    return True

            # For moves to the foundation piles
            elif target_pile.pile_type == PileType.FOUNDATION:
                # Same suit and the moving card's value is one more than the top card's value
                if (card.suit == top_target_card.suit and
                    CARD_VALUE_MAP[card.value] == CARD_VALUE_MAP[top_target_card.value] + 1):
                    return True

        # If the target pile is empty and the moving card is an Ace
        elif not target_pile.cards and card.value == "ace" and target_pile.pile_type == PileType.FOUNDATION:
            return True

        # If the target tableau pile is empty and the moving card is a King
        elif not target_pile.cards and card.value == "king" and target_pile.pile_type == PileType.TABLEAU:
            return True

        return False

    def display(self, game_display):
        # draw the stock pile
        stock_pile = next((pile for pile in self.piles if pile.pile_type == PileType.STOCK), None)
        if stock_pile:
            self.draw_pile(game_display, stock_pile)
        
        # draw the waste pile
        waste_pile = next((pile for pile in self.piles if pile.pile_type == PileType.WASTE), None)
        if waste_pile:
            self.draw_pile(game_display, waste_pile)
        
        # Draw other piles
        for pile in self.piles:
            if pile not in [stock_pile, waste_pile]:
                self.draw_pile(game_display, pile)

    def draw_pile(self, game_display, pile):
        margin = 3 

        # Draw the mats with slightly larger size than cards
        pygame.draw.rect(game_display, self.mat_color, [
            pile.x - margin, 
            pile.y - margin, 
            self.card_size[0] + (margin * 2), 
            self.card_size[1] + (margin * 2)
        ])
        # Draws cards on top of mats
        for pile in self.piles:
            for card in pile.cards:
                img = self.card_images[card.name_of_card] if card.discovered else self.back_image_of_card
                game_display.blit(img, (card.x, card.y))

            