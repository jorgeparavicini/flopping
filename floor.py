from drawable import Drawable
import pygame


class Floor(Drawable):
    def draw(self, screen):
        rect = 0, screen.get_size()[1]-self.floor_level, screen.get_size()[0], self.floor_level
        pygame.draw.rect(screen, pygame.Color(0, 165, 19, 255), rect)

    @property
    def floor_level(self):
        return 200




