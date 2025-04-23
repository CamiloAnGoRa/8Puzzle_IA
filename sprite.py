import pygame
from settings import *

pygame.font.init()


class Bloque(pygame.sprite.Sprite):
    def __init__(self, game, x, y, text):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        self.image = pygame.Surface((tamaño_bloque, tamaño_bloque))
        self.x, self.y = x, y
        self.text = text
        self.rect = self.image.get_rect()
        if self.text != "empty":
            self.font = pygame.font.SysFont("Consolas", 50)
            font_surface = self.font.render(self.text, True, black)
            self.image.fill(white)
            self.font_size = self.font.size(self.text)
            # Centrar el texto en el bloque
            font_x = (tamaño_bloque - self.font_size[0]) // 2
            font_y = (tamaño_bloque - self.font_size[1]) // 2
            self.image.blit(font_surface, (font_x, font_y))
        
        # Llama a actualización para posicionar correctamente el rectángulo
        self.actualizacion()

    def actualizacion(self):
        self.rect.x = self.x * tamaño_bloque
        self.rect.y = self.y * tamaño_bloque

    def click(self, mouse_x, mouse_y):
        return self.rect.left <= mouse_x <= self.rect.right and self.rect.top <= mouse_y <= self.rect.bottom