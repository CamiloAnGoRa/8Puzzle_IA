import pygame
from settings import *

pygame.font.init()


class bloque(pygame.sprite.Sprite):
    def __init__(self, game, x, y, text):
        self.groups = game.all.sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        self.image = pygame.Surface((tamaño_bloque, tamaño_bloque))
        self.x, self.y = x, y
        self.text = text
        self.rect = self.image.get_rect()

    def actualizacion(self):
        self.rect.x = self.x * tamaño_bloque
        self.rect.y = self.y * tamaño_bloque

    def click(self, mouse_x, mouuse_y):
        return self.rect.left <= mouse_x <= self.rect.right and self.rect.top <= mouuse_y <= self.rect.bottom