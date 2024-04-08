import pygame
import sys
from deck import Deck
from text import Text
from gamemode import Gamemode
from settings import Settings
from settingsmenu import SettingsMenu
from widgets import *
from pile import *
from score import *

# Screen title and size
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_TITLE = "Solitaire"
BACKGROUND_COLOR = (0,128,0)

# GUI bar colour and size
UI_BAR_COLOR = (255,255,255)
UI_BAR_SIZE = 35

class Ui:
    def __init__(self):
        # Initialize Pygame
        pygame.init()
        self.saved_settings = Settings()
        self.settings_changed = False
        self.score = Score(self.saved_settings)
        self.setup(Gamemode.KLONDIKE)

    def setup(self, gamemode):
        self.saved_settings.update_settings(gamemode)
        self.settings_changed = False
        
        self.score.start_game()
        self.move_made = False

        self.starting_gamemode = gamemode
        
        # set screen size
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        # Set up GUI
        self.topbar = pygame.Rect(0, 0, SCREEN_WIDTH, UI_BAR_SIZE)
        self.bottom_bar = pygame.Rect(0, SCREEN_HEIGHT-UI_BAR_SIZE, SCREEN_WIDTH, UI_BAR_SIZE)
        self.new_game_btn = Button('New Game', pygame.Rect(0,0,125,Button.DEFAULT_HEIGHT+5))
        self.settings_btn = Button('Settings', pygame.Rect(self.new_game_btn.rect.right+1, 0, 125, Button.DEFAULT_HEIGHT+5))
        self.settings = SettingsMenu('Game Settings')
        self.settings_close_msg = ConfirmationBox('Changes will be applied on the next game.')
        self.end_game_screen = MessageBox('Play again?')
        self.gamemode_display = Text(str.capitalize(self.saved_settings.active_gamemode.name) + " rules applied.", (SCREEN_WIDTH//2, self.bottom_bar.bottom-19))

        # Set up saved settings
        match self.saved_settings.active_gamemode:
            case Gamemode.KLONDIKE:
                self.settings.gamemode.options[0].select()
                self.settings.gamemode.options[1].unselect()
            case Gamemode.VEGAS:
                self.settings.gamemode.options[1].select()
                self.settings.gamemode.options[0].unselect()
            case _:
                pass
        
        # set title
        pygame.display.set_caption(SCREEN_TITLE)
        
        # Background color
        self.bg_color = (BACKGROUND_COLOR) 

        # Initialize deck
        self.deck = Deck(self)
        self.deck.load_cards() 
        self.deck.shuffle_cards()
        self.deck.load_piles((SCREEN_WIDTH, SCREEN_HEIGHT))

        self.dragged_cards = []
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
                elif event.type == pygame.MOUSEMOTION and self.dragged_cards:
                    self.handle_mouse_motion(pygame.mouse.get_pos())
            
            # Fill the background with green color (or lighter green if game is over)
            self.screen.fill(self.bg_color if not self.end_game_screen.visible and not self.settings.visible and not self.settings_close_msg.visible else (125,218,88))

            # Display the deck
            self.deck.display(self.screen)

            # Display the GUI
            pygame.draw.rect(self.screen, UI_BAR_COLOR, self.topbar)
            pygame.draw.rect(self.screen, UI_BAR_COLOR, self.bottom_bar)
            self.new_game_btn.draw(self.screen)
            self.settings_btn.draw(self.screen)
            self.gamemode_display.draw(self.screen)
            
            if self.end_game_screen.visible:
                self.end_game_screen.draw(self.screen)
            elif self.settings.visible:
                self.settings.draw(self.screen)
            elif self.settings_close_msg.visible:
                self.settings_close_msg.draw(self.screen)
            
            # Display the score on the top bar
            font = pygame.font.Font(None, 30)  
            text = font.render(f'Score: {self.score.score}', True, (0, 0, 0))  # Black color for the font
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, UI_BAR_SIZE // 2))
            self.screen.blit(text, text_rect)

            # Display the move count on the top bar
            move_count_text = font.render(f'Moves: {self.score.moves_made}', True, (0, 0, 0))  
            move_count_rect = move_count_text.get_rect(center=(SCREEN_WIDTH // 3, UI_BAR_SIZE // 2))
            self.screen.blit(move_count_text, move_count_rect)

            # Check if there are any dragged cards
            if self.dragged_cards:  
                for dragged_card in self.dragged_cards:  
                    img = self.deck.card_images[dragged_card.name_of_card] 
                    offset = 0 if self.starting_gamemode == Gamemode.KLONDIKE else 50
                    self.screen.blit(img, (dragged_card.x+offset, dragged_card.y))

            # Place a win condition that restarts the game when triggered
            if len(self.deck.piles[-1].cards) == 13 and len(self.deck.piles[-2].cards) == 13 and len(self.deck.piles[-3].cards) == 13 and len(self.deck.piles[-4].cards) == 13:
                self.end_game_screen.show()
                self.new_game_btn.disable()
                self.settings_btn.disable()

            # Apply time penalty when game is not win
            # if not self.win_screen.visible:
            #     self.score.apply_time_penalty()

            # Render score
            self.score.display_score(self.screen)
        
            # Update the display
            pygame.display.flip()

    def handle_mouse_down(self, mouse_pos):
        # Handle saved settings
        if self.settings.visible:
            if self.settings.gamemode.options[0].clicked(mouse_pos):
                self.saved_settings.update_settings(Gamemode.KLONDIKE)
                self.settings_changed = True
                self.settings.gamemode.options[0].select()
                self.settings.gamemode.options[1].unselect()
            elif self.settings.gamemode.options[1].clicked(mouse_pos):
                self.saved_settings.update_settings(Gamemode.VEGAS)
                self.settings_changed = True
                self.settings.gamemode.options[1].select()
                self.settings.gamemode.options[0].unselect()

        # Handle In-game button (GUI) clicks
        if self.new_game_btn.clicked(mouse_pos) and self.new_game_btn.enabled:
            if self.settings_changed:
                self.saved_settings.update_settings(self.saved_settings.active_gamemode)
                self.score.update(self.saved_settings)
                self.score.moves_made = 0
            self.setup(self.saved_settings.active_gamemode)
            if self.saved_settings.active_gamemode == Gamemode.KLONDIKE:
                self.score = Score(self.saved_settings)
        elif self.settings_btn.clicked(mouse_pos) and self.settings_btn.enabled:
            self.settings.show()
            self.settings_btn.disable()
            self.new_game_btn.disable()

        # Handle settings menu button clicks
        if self.settings.visible and self.settings.clicked_close(mouse_pos):
            self.settings.hide()
            if self.saved_settings.active_gamemode is not self.starting_gamemode:
                self.settings_close_msg.show()
            else:
                self.settings_btn.enable()
                self.new_game_btn.enable()

        if self.settings_close_msg.visible:
            if self.settings_close_msg.clicked_ok(mouse_pos):
                self.settings_close_msg.hide()
                self.settings.hide()
                self.settings_btn.enable()
                self.new_game_btn.enable()

        # Handle end screen button clicks
        if self.end_game_screen.visible:
            if self.end_game_screen.clicked_yes(mouse_pos):
                self.end_game_screen.hide()
                self.new_game_btn.enable()
                self.settings_btn.enable()
                if self.settings_changed:
                    self.saved_settings.update_settings(self.saved_settings.active_gamemode)
                    self.score.update(self.saved_settings)
                self.setup(self.saved_settings.active_gamemode)
                if self.saved_settings.active_gamemode == Gamemode.KLONDIKE:
                    self.score = Score(self.saved_settings)
            elif self.end_game_screen.clicked_no(mouse_pos):
                pygame.quit()
                sys.exit()

        if not self.end_game_screen.visible and not self.settings.visible and not self.settings_close_msg.visible:
            # Check if the click is on the deck pile
            deck_pile = next((pile for pile in self.deck.piles if pile.pile_type == PileType.STOCK), None)
            if deck_pile and deck_pile.is_mouse_over(mouse_pos):
                 # If the deck pile is empty
                if not deck_pile.cards:
                    '''
                    Determine if possible according to the rules outlined
                    Where Draw 3 allows for 3 complete shuffles of the stock,
                    Draw 1 allows for 1 complete shuffle of the stock
                    '''
                    self.saved_settings.draw_amount -= 1
                    if not self.move_made and self.saved_settings.draw_amount <= 0:
                        self.end_game_screen.show()
                        self.new_game_btn.disable()
                        self.settings_btn.disable()
                    
                    self.move_made = False
                    
                    self.deck.transfer_waste_to_deck()
                    self.score.refresh_stockpile()
                else:
                   for _ in range(1 if self.starting_gamemode == Gamemode.KLONDIKE else 3):
                        self.deck.transfer_card_from_deck_to_waste()
                return
            
            # For all other pile types
            picked_card, picked_pile = self.deck.get_card_at_position(mouse_pos)
            if picked_card and picked_card.discovered:
                self.dragged_cards = []
                self.origin_pile = picked_pile
                self.original_positions = [] 
    
                if picked_pile.pile_type == PileType.TABLEAU:
                    # Find the index of the picked card in its pile
                    index = picked_pile.cards.index(picked_card)
                    # Select the picked card and all cards above it in the pile
                    self.dragged_cards = picked_pile.cards[index:]
                    # Store original positions for each card in the dragged stack
                    self.original_positions = [(card.x, card.y) for card in self.dragged_cards]
                else:
                    # If it's not a tableau pile, proceed with the single card
                    self.dragged_cards = [picked_card]
                    self.original_positions = [(picked_card.x, picked_card.y)]
    
                self.offset_x = mouse_pos[0] - picked_card.x
                self.offset_y = mouse_pos[1] - picked_card.y

    def handle_mouse_motion(self, mouse_pos):
        if self.dragged_cards: 
            # Calculate the new position based on the current mouse position minus the drag offset
            delta_x = mouse_pos[0] - self.offset_x
            delta_y = mouse_pos[1] - self.offset_y
            # loop through the dragged cards
            for i, card in enumerate(self.dragged_cards):
                if i == 0:
                    new_card_x = delta_x
                    new_card_y = delta_y
                else:
                    # maintain cards relative positions within the stack after the first card
                    original_delta_x = self.original_positions[i][0] - self.original_positions[0][0]
                    original_delta_y = self.original_positions[i][1] - self.original_positions[0][1]
                    new_card_x = delta_x + original_delta_x
                    new_card_y = delta_y + original_delta_y

                card.set_position(new_card_x, new_card_y)


    def handle_mouse_up(self, mouse_pos):
        if not self.end_game_screen.visible and not self.settings.visible and not self.settings_close_msg.visible:
            if self.dragged_cards: 
                target_pile = self.deck.get_pile_at_position(mouse_pos)
                move_valid = False
    
                if target_pile:
                    # Get the bottom card for validation
                    bottom_card = self.dragged_cards[0]
    
                    # Check if moving the bottom card to the target pile is valid
                    move_valid = self.deck.is_valid_move(bottom_card, self.origin_pile, target_pile)
    
                    if move_valid:
                        # Move each card in the dragged stack to the target pile if the bottom card's move is valid
                        for card in self.dragged_cards:
                            self.snap_card_to_pile(card, target_pile)
                            self.deck.move_card(card, self.origin_pile, target_pile, self.score)
    
                else:
                    move_valid = False
    
                if not move_valid:
                    # If the move is invalid, or no target pile is identified, revert cards to their original positions
                    for card, (original_x, original_y) in zip(self.dragged_cards, self.original_positions):
                        card.set_position(original_x, original_y)
                        if card not in self.origin_pile.cards:
                            self.origin_pile.cards.append(card)
                else:
                    self.move_made = True
    
                # Clear the list of dragged cards after dropping
                self.dragged_cards = []

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



