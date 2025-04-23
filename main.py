import pygame
import random
import time
from sprite import *
from settings import *

class juego:
    def __init__(self): 
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(titulo)
        self.clock = pygame.time.Clock()

    def crear_juego(self):
        grid = [[x + y * tamaño_tablero for x in range(1, tamaño_tablero + 1)] for y in range(tamaño_tablero)]
        grid[-1][-1] = 0
        return grid

    def dibujar_bloques(self):
        self.bloques = []
        for row, x in enumerate(self.bloques_grid):
            self.bloques.append([])
            for col, valor in enumerate(x):  # Cambiado 'bloque' por 'valor' para evitar confusión
                if valor != 0:
                    self.bloques[row].append(Bloque(self, col, row, str(valor)))
                else:
                    self.bloques[row].append(Bloque(self, col, row, "empty"))

    def nuevo_juego(self):
        self.all_sprites = pygame.sprite.Group()
        self.bloques_grid = self.crear_juego()
        self.bloques_grid_completado = self.crear_juego()
        self.dibujar_bloques()  # Añadido para crear los bloques visuales inmediatamente

    def iniciar(self):
        self.jugando = True
        while self.jugando:
            self.clock.tick(fps)
            self.eventos()
            self.actualizar()
            self.dibujar()

    def actualizar(self):
        # Asegurarse de que todos los sprites se actualicen correctamente
        self.all_sprites.update()

    def dibujar_cuadricula(self):
        ancho_tab = tamaño_tablero * tamaño_bloque
        alto_tab = tamaño_tablero * tamaño_bloque

        # Sombra
        pygame.draw.rect(
            self.screen, 
            shadow_color, 
            (-shadow_size, -shadow_size, ancho_tab + shadow_size*2, alto_tab + shadow_size*2),
            border_radius=3
        )

        # Fondo
        pygame.draw.rect(self.screen, BGcolor, (0, 0, ancho_tab, alto_tab))

        # Líneas verticales
        for row in range(-1, ancho_tab + 1, tamaño_bloque):
            pygame.draw.line(
                self.screen, 
                gris_claro, 
                (row, 0), 
                (row, alto_tab),
                width=grosor_linea
            )

        # Líneas horizontales
        for col in range(-1, alto_tab + 1, tamaño_bloque):
            pygame.draw.line(
                self.screen, 
                gris_claro, 
                (0, col), 
                (ancho_tab, col),
                width=grosor_linea
            )

    def dibujar(self):
        self.screen.fill(BGcolor)
        self.dibujar_cuadricula()
        self.all_sprites.draw(self.screen)  # Dibuja todos los bloques
        pygame.display.flip()

    def eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)

game = juego()
while True:
    game.nuevo_juego()
    game.iniciar()