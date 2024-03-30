import math
import pygame

from text import Text

class Button:

    DEFAULT_WIDTH = 100
    DEFAULT_HEIGHT = 30

    def __init__(self, content, rect=pygame.Rect(0,0,DEFAULT_WIDTH,DEFAULT_HEIGHT)):
        self.rect = rect
        self.border = rect
        self.content = content
        self.text = Text(self.content, (self.rect.left + (self.rect.w / 2)-1, self.rect.top + (self.rect.h / 2)-1))
        self.enable()
    
    def clicked(self, mouse_pos):
        return mouse_pos[0] > self.rect.left and mouse_pos[0] < self.rect.right and mouse_pos[1] > self.rect.top and mouse_pos[1] < self.rect.bottom

    def enable(self):
        self.enabled = True
        self.text.colour = (0,0,0)
    
    def disable(self):
        self.enabled = False
        self.text.colour = (198,198,198)

    def draw(self, surface):
        pygame.draw.rect(surface, (206,206,206) if self.enabled else (232,232,232), self.rect)
        pygame.draw.rect(surface, (0,0,0) if self.enabled else (224, 226, 227), self.border, 1)
        self.text.draw(surface)


class RadioButton:

    BORDER_COLOUR = (128,128,128)
    UNSELECTED_COLOUR = (255,255,255)
    SELECTED_COLOUR = (36,160,237)

    def __init__(self, prompt, pos=(10,10), radius=10):
        self.pos = pos
        self.radius = radius
        self.prompt = Text(prompt, (self.pos[0]+self.radius+35, self.pos[1]))
        self.selected = False

    def select(self):
        self.selected = True
    
    def unselect(self):
        self.selected = False

    def clicked(self, mouse_pos):
        # Formula assisted by ChatGPT
        dx = mouse_pos[0] - self.pos[0]
        dy = mouse_pos[1] - self.pos[1]
        return math.sqrt(dx**2 + dy**2) < self.radius

    def draw(self, surface):
        pygame.draw.circle(surface, self.UNSELECTED_COLOUR if not self.selected else self.SELECTED_COLOUR, self.pos, self.radius)
        pygame.draw.circle(surface, self.BORDER_COLOUR, self.pos, self.radius, 2)
        self.prompt.draw(surface)


class RadioGroup:
    def __init__(self, pos, options, x_spacing=100, y_spacing=22, orientation='h'):
        self.options = options
        self.options[0].select()
        for i in range(len(self.options)):
            if orientation == 'h':
                self.options[i].pos = (pos[0]+i*x_spacing, pos[1])
                self.options[i].prompt.display_rect.center = (pos[0]+50+i*x_spacing, pos[1])
            else:
                self.options[i].pos = (pos[0], pos[1]+i*y_spacing)
                self.options[i].prompt.display_rect.center = (pos[0]+50, pos[1]+i*y_spacing-1)

        return None

    def draw(self, surface):
        for option in self.options:
            option.draw(surface)

class ConfirmationBox:
    def __init__(self, title):
        self.visible = False
        self.menu = pygame.Rect(MessageBox.ORIGIN_X, MessageBox.ORIGIN_Y, MessageBox.WIDTH, MessageBox.HEIGHT)
        self.border = pygame.Rect(MessageBox.ORIGIN_X, MessageBox.ORIGIN_Y, MessageBox.WIDTH, MessageBox.HEIGHT)
        self.prompt = Text(title, (self.menu.left + (self.menu.w / 2)-1, self.menu.top + 25), pygame.font.SysFont('Times New Roman', 18))
        self.ok = Button('Ok', pygame.Rect(self.menu.x + 150, self.menu.y + 75, Button.DEFAULT_WIDTH, Button.DEFAULT_HEIGHT))

    def clicked_ok(self, mouse_pos):
        return self.ok.clicked(mouse_pos)

    def show(self):
        self.visible = True
        self.ok.enable()

    def hide(self):
        self.visible = False
        self.ok.disable()

    def draw(self, surface):
        pygame.draw.rect(surface, (206,206,206), self.menu)
        pygame.draw.rect(surface, (0,0,0), self.border, 1)
        self.ok.draw(surface)
        self.prompt.draw(surface)

class MessageBox:
    
    ORIGIN_X = 312
    ORIGIN_Y = 309
    WIDTH = 400
    HEIGHT = 125

    def __init__(self, title):
        self.visible = False

        self.menu = pygame.Rect(self.ORIGIN_X, self.ORIGIN_Y, self.WIDTH, self.HEIGHT)
        self.border = pygame.Rect(self.ORIGIN_X, self.ORIGIN_Y, self.WIDTH, self.HEIGHT)
        self.prompt = Text(title, (self.menu.left + (self.menu.w / 2)-1, self.menu.top + 25), pygame.font.SysFont('Times New Roman', 24))
        self.yes = Button('Yes', pygame.Rect(self.menu.x + 75, self.menu.y + 75, Button.DEFAULT_WIDTH, Button.DEFAULT_HEIGHT))
        self.no = Button('Exit', pygame.Rect(self.yes.rect.x+self.yes.rect.w + 50, self.yes.rect.y, Button.DEFAULT_WIDTH, Button.DEFAULT_HEIGHT))

    def clicked_yes(self, mouse_pos):
        return self.yes.clicked(mouse_pos)

    def clicked_no(self, mouse_pos):
        return self.no.clicked(mouse_pos)

    def show(self):
        self.visible = True
        self.yes.enable()
        self.no.enable()

    def hide(self):
        self.visible = False
        self.yes.disable()
        self.no.disable()

    def draw(self, surface):
        pygame.draw.rect(surface, (206,206,206), self.menu)
        pygame.draw.rect(surface, (0,0,0), self.border, 1)
        self.yes.draw(surface)
        self.no.draw(surface)
        self.prompt.draw(surface)
