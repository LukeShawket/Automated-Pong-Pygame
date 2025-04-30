import pygame

class Button:
    def __init__(self, x, y, wid, hei):
        self.width = wid
        self.height = hei
        self.x = x
        self.y = y
        self.pressed = False
        self.visible = True
    
    def draw(self, screen):
        if self.visible:
            pygame.draw.rect(screen, "gray", [self.x, self.y, self.width, self.height])

    def button_state_update(self, events):
        button_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                if button_rect.collidepoint(event.pos):
                    self.pressed = True
        
        return self.pressed


class Text():
    def __init__(self, size, color):
        self.size = size
        self.color = color
        pygame.font.init()
        self.font = pygame.font.SysFont("Arial", size)
    def get_text(self, text):
        text_surface = self.font.render(text, True, self.color)
        return text_surface
