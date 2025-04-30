import pygame

class Ball:
    
    def __init__(self, screen, _pos):
        self.pos = _pos
        self.hit = ''
        pygame.draw.circle(screen, "green", _pos, 15)
    
    def collision(self, ball_pos, right_paddle_rect, left_paddle_rect):
        ball_rect = pygame.Rect(ball_pos.x, ball_pos.y, 30, 30)
        if ball_rect.colliderect(right_paddle_rect):
            self.hit = "right_hit"
        if ball_rect.colliderect(left_paddle_rect):
            self.hit = "left_hit"
        return self.hit