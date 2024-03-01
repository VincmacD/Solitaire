import pygame
import sys
from deck import Deck
from pile import *

# Screen title and size
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 850
SCREEN_TITLE = "Solitaire"
BACKGROUND_COLOR = (0,128,0)

class Ui:
    def __init__(self):
        # Initialize Pygame
        pygame.init()
        
        # Set up the screen with the specified width and height
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        # Set the title of the window
        pygame.display.set_caption(SCREEN_TITLE)
        
        # Define the background color (green in RGB)
        self.bg_color = (BACKGROUND_COLOR) 

        # Initialize the deck
        self.deck = Deck()
        self.deck.load_cards()  # Load card images and create Card objects
        self.deck.shuffle_cards()
        self.deck.load_piles((SCREEN_WIDTH, SCREEN_HEIGHT))  # Setup piles according to screen size

        self.dragged_card = None
        self.drag_offset_x = 0
        self.drag_offset_y = 0
        
    def mainloop(self):
        # Main loop of the game
        while True:
            # Check for events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_down(pygame.mouse.get_pos())
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.handle_mouse_up(pygame.mouse.get_pos())
                elif event.type == pygame.MOUSEMOTION and self.dragged_card:
                    self.handle_mouse_motion(pygame.mouse.get_pos())
            
            # Fill the background with the green color
            self.screen.fill(self.bg_color)

            # Display the deck
            self.deck.display(self.screen)
            
            # Optionally, draw the dragged card on top of everything else
            if self.dragged_card:
                img = self.deck.card_images[self.dragged_card.name_of_card]  # Ensure this accesses the card correctly
                self.screen.blit(img, (self.dragged_card.x, self.dragged_card.y))
            
            # Update the display
            pygame.display.flip()

    def handle_mouse_down(self, mouse_pos):

        # Check if the click is on the deck pile
        deck_pile = next((pile for pile in self.deck.piles if pile.pile_type == PileType.STOCK), None)
        if deck_pile and deck_pile.is_mouse_over(mouse_pos):
            if not deck_pile.cards:  # If the stock pile is empty
                self.deck.transfer_waste_to_deck()
            else:
                self.deck.transfer_card_from_deck_to_waste()
            return  # Skip further processing to avoid dragging logic interference

        # For all other pile types
        picked_card, picked_pile = self.deck.get_card_at_position(mouse_pos)

        if picked_card and picked_card.discovered:
            if self.deck.auto_transfer_on_click(mouse_pos, picked_card):
                self.deck.auto_transfer_on_click(mouse_pos, picked_card)

            self.dragged_card = picked_card
            self.origin_pile = picked_pile
            self.original_position = (picked_card.x, picked_card.y)  # Store the original position
            self.drag_offset_x = mouse_pos[0] - picked_card.x
            self.drag_offset_y = mouse_pos[1] - picked_card.y

    def handle_mouse_motion(self, mouse_pos):
        if self.dragged_card:
            # Update the dragged card's position based on the current mouse position
            # minus the initial offset between the card's top-left corner and the mouse click position
            new_x = mouse_pos[0] - self.drag_offset_x
            new_y = mouse_pos[1] - self.drag_offset_y
            self.dragged_card.set_position(new_x, new_y)

    def handle_mouse_up(self, mouse_pos):
        if self.dragged_card:
            target_pile = self.deck.get_pile_at_position(mouse_pos)
            if target_pile and self.deck.is_valid_move(self.dragged_card, self.origin_pile, target_pile):
                # Snap the card to the target pile and move it there in the Deck's data structure
                self.snap_card_to_pile(self.dragged_card, target_pile)
                self.deck.move_card(self.dragged_card, self.origin_pile, target_pile)
            else:
                # Move was invalid or no target pile, return card to original pile and position
                self.dragged_card.set_position(*self.original_position)
                if target_pile is None or not self.deck.is_valid_move(self.dragged_card, self.origin_pile, target_pile):
                    # If returning, ensure the card is re-added to the original pile if it was removed
                    if self.dragged_card not in self.origin_pile.cards:
                        self.origin_pile.cards.append(self.dragged_card)

            self.dragged_card = None

    def snap_card_to_pile(self, card, target_pile):
        # Snapping back to the original pile
        if target_pile == self.origin_pile:
            # Calculate the card's index in its original pile
            card_index = self.origin_pile.cards.index(card)
            # Calculate the Y position based on the card's index
            new_y = target_pile.y + card_index * target_pile.card_spacing if target_pile.pile_type == PileType.TABLEAU else target_pile.y
        else:
            if target_pile.cards:
                # Place the card at the correct offset from the last card in a tableau pile
                last_card = target_pile.cards[-1]
                new_y = last_card.y + target_pile.card_spacing if target_pile.pile_type == PileType.TABLEAU else target_pile.y
            else:
                # If the target pile is empty, place the card directly at the pile's base position
                new_y = target_pile.y

        new_x = target_pile.x
        card.set_position(new_x, new_y)



