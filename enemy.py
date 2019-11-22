from drawable import Drawable
import pygame
import math


class Enemy(Drawable):
    def draw(self, screen):
        pygame.draw.rect(screen, pygame.Color("black"), self.rect)

    @property
    def rect(self):
        return pygame.Rect(self.position_x, self.position_y, self.width, self.height)

    def __init__(self, width=100, height=100, position_x: float = 150, position_y: float = 150, velocity_x=80):
        self.width = width
        self.height = height
        self.position_x = position_x
        self.position_y = position_y
        self.velocity_x = velocity_x

    def update_position(self, delta_time):
        self.position_x -= self.velocity_x * delta_time


class Bowser(Enemy):

    def draw(self, screen, rect):
        center = (int(rect[0] + rect[2] / 2), int(rect[1] + rect[3] / 2))
        radius = min(rect[2] / 2, rect[3] / 2)
        pygame.draw.circle(screen, pygame.Color("blue"), center, int(radius))
