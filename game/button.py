import pygame

class Button:

    DEFAULT_WIDTH = 100
    DEFAULT_HEIGHT = 30

    def __init__(self, content, rect=pygame.Rect(0,0,DEFAULT_WIDTH,DEFAULT_HEIGHT)):
        self.rect = rect
        self.border = rect
        
        self.content = content
        self.font = pygame.font.SysFont('Times New Roman', 18)
        self.text = self.font.render(self.content, True, (0,0,0))
        self.text_rect = self.text.get_rect()
        self.text_rect.center = (self.rect.left + (self.rect.w / 2)-1, self.rect.top + (self.rect.h / 2)-1)

        self.enable()
    
    def clicked(self, mouse_pos):
        return mouse_pos[0] > self.rect.left and mouse_pos[0] < self.rect.right and mouse_pos[1] > self.rect.top and mouse_pos[1] < self.rect.bottom

    def enable(self):
        self.enabled = True
        self.text = self.font.render(self.content, True, (0,0,0))
    
    def disable(self):
        self.enabled = False
        self.text = self.font.render(self.content, True, (198,198,198))

    def draw(self, surface):
        pygame.draw.rect(surface, (206,206,206) if self.enabled else (232,232,232), self.rect)
        pygame.draw.rect(surface, (0,0,0) if self.enabled else (224, 226, 227), self.border, 1)
        surface.blit(self.text, self.text_rect)
