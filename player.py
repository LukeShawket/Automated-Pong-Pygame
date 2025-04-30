import pygame
import random


class Player:
    def __init__(self, screen, x, y, color, min_speed, max_speed):
        self.min_speed = min_speed
        self.max_speed = max_speed
        pygame.draw.rect(screen, color, [x, y, 30, 200])
    
    def predict(self):
        random_value = random.randint(1, 10)
        return random_value