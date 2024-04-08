import pygame

from text import Text
from widgets import Button, RadioButton, RadioGroup

class SettingsMenu:
    
    ORIGIN_X = 300
    ORIGIN_Y = 225
    WIDTH = 400
    HEIGHT = 300

    def __init__(self, title):
        self.visible = False

        self.menu = pygame.Rect(self.ORIGIN_X, self.ORIGIN_Y, self.WIDTH, self.HEIGHT)
        self.border = pygame.Rect(self.ORIGIN_X, self.ORIGIN_Y, self.WIDTH, self.HEIGHT)
        
        self.prompt = Text(title, (self.menu.left + (self.menu.w / 2)-1, self.menu.top + 25), pygame.font.SysFont('Times New Roman', 24))
        
        ''' Additional widgets '''
        self.gamemode_prompt = Text('Gamemode', (self.menu.left+60, self.menu.top+95))
        self.gamemode = RadioGroup((self.menu.left+225, self.menu.top+95), [RadioButton('Klondike'), RadioButton('Vegas      ')])
        self.close = Button('Ok', pygame.Rect(self.menu.x+150, self.menu.bottom-50, Button.DEFAULT_WIDTH, Button.DEFAULT_HEIGHT))

    def clicked_close(self, mouse_pos):
        return self.close.clicked(mouse_pos)

    def show(self):
        self.visible = True
        self.close.enable()

    def hide(self):
        self.visible = False
        self.close.disable()

    def draw(self, surface):
        pygame.draw.rect(surface, (206,206,206), self.menu)
        pygame.draw.rect(surface, (0,0,0), self.border, 1)
        self.gamemode_prompt.draw(surface)
        self.gamemode.draw(surface)
        self.close.draw(surface)
        self.prompt.draw(surface)
