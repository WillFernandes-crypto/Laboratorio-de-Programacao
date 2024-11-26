# entities/healthbar.py
import pygame

class HealthBar:
    def __init__(self, x, y, max_value, color, bar_length):
        self.x = x
        self.y = y
        self.max_value = max_value
        self.color = color
        self.bar_length = bar_length

    def draw(self, surface, current_value):
        health_percentage = current_value / self.max_value
        pygame.draw.rect(surface, (0, 0, 0), (self.x - 2, self.y - 2, self.bar_length + 4, 20))
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.bar_length * health_percentage, 16))
