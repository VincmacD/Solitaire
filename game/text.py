import pygame
pygame.init() # Due to the order of calls, pygame complains without this

class Text:
    def __init__(self, content, centre, font=pygame.font.SysFont('Times New Roman', 18), colour=(0,0,0)):
        self.content = content
        self.font = font
        self.colour = colour
        self.display = self.font.render(self.content, True, self.colour)
        self.display_rect = self.display.get_rect()
        self.display_rect.center = centre

    def draw(self, surface):
        surface.blit(self.display, self.display_rect)
