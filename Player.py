from drawable import Drawable
import pygame
import math


class Player(Drawable):

    @property
    def jump_force(self):
        return 230

    @property
    def rect(self):
        return pygame.Rect(self.position_x, self.position_y, self.width, self.height)

    def __init__(self, width=100, height=100, position_x: float = 150, position_y: float = 150):
        self.width = width
        self.height = height
        self.position_x = position_x
        self.position_y = position_y
        self.y_velocity = 0
        self.jumped = False

    def draw(self, screen):
        pygame.draw.rect(screen, pygame.Color("red"), self.rect)

    def jump(self, is_grounded):
        self.y_velocity = self.jump_force
        # if is_grounded:
        #     self.y_velocity = self.jump_force
        #     self.jumped = False
        # elif not self.jumped:
        #     self.y_velocity = self.jump_force
        #     self.jumped = True




class SuperMario(Player):

    def draw(self, screen, rect):
        center = (int(rect[0] + rect[2] / 2), int(rect[1] + rect[3] / 2))
        radius = min(rect[2] / 2, rect[3] / 2)
        pygame.draw.circle(screen, pygame.Color("blue"), center, int(radius))

