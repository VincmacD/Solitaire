import pygame
from button import Button


class MessageBox:
    
    ORIGIN_X = 312
    ORIGIN_Y = 309
    WIDTH = 400
    HEIGHT = 125

    def __init__(self, title):
        self.visible = False

        self.menu = pygame.Rect(self.ORIGIN_X, self.ORIGIN_Y, self.WIDTH, self.HEIGHT)
        self.border = pygame.Rect(self.ORIGIN_X, self.ORIGIN_Y, self.WIDTH, self.HEIGHT)

        self.font = pygame.font.SysFont('Times New Roman', 24)
        self.prompt = self.font.render(title, True, (0,0,0))
        self.prompt_rect = self.prompt.get_rect()
        self.prompt_rect.center = (self.menu.left + (self.menu.w / 2)-1, self.menu.top + 25)

        self.yes = Button('Yes', pygame.Rect(self.menu.x + 75, self.menu.y + 75, Button.DEFAULT_WIDTH, Button.DEFAULT_HEIGHT))
        self.no = Button('No', pygame.Rect(self.yes.rect.x+self.yes.rect.w + 50, self.yes.rect.y, Button.DEFAULT_WIDTH, Button.DEFAULT_HEIGHT))

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
        surface.blit(self.prompt, self.prompt_rect)
