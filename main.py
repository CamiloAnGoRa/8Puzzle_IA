import pygame
import random
import time
from sprite import *
from settings import *

#Definimos la clase de juego
class juego:
    #Toma de un constructor
    def __init__(self): 
        #iniciar juego
        pygame.init()
        #Creacion de pantalla
        self.screen = pygame.display.set_mode((width, height))
        #Colocar el titulo del juego
        pygame.display.set_caption(titulo)
        #Crear el reloj para la toma del tiempo
        self.clock = pygame.time.Clock()


    def crear_juego(self):
        grid = []
        number = 1
        for x in range(tamaño_tablero):
            grid.append([])
            for y in range(tamaño_tablero):
                grid[x].append(number)
                number += 1

        grid[-1][-1] = 0
        print(grid)


    #Deficion de clase para un nuevo juego
    def nuevo_juego(self):
        self.crear_juego()




    #Deficion de clase para iniciar juego
    def iniciar(self):
        #Creamos esta variable para poder modificarla posteriormente al iniciar un nuevo juego
        self.jugando = True
        while self.jugando:
            #Llamamos al reloj y adjuntamos los fps
            self.clock.tick(fps)
            #Generamos un llamado a los eventos 
            self.eventos()
            #LLamado acutalizacion
            self.actualizar()
            #LLamado de dibujado
            self.dibujar()




    #Deficion de clase para actulizar el juego
    def actualizar(self):
        pass


    #Dibujamos la cuadricula del juego
    def dibujar_cuadricula(self):

        #Determinamos el ancho total que va a tener el tablero
        ancho_tab = tamaño_tablero * tamaño_bloque

        #Determinamos el Alto total que va a tener el tablero
        alto_tab = tamaño_tablero * tamaño_bloque


        #Sombra (Creamos un bloque mas grande de fondo para dar una lligera sombra)
        pygame.draw.rect(self.screen, shadow_color, (-shadow_size, -shadow_size, ancho_tab + shadow_size * 2, alto_tab + shadow_size * 2),border_radius=3)

        #Dibujamos fondo del tablero cubriendo el centro de la sombra 
        pygame.draw.rect(self.screen, BGcolor, (0, 0, ancho_tab, alto_tab))



        #Incluimos un borde exterior comenzando en un rango con -1 
        #Terminamos la linea en el ancho total del tablero
        #Depende del tamaño del bloque
        for row in range(-1, tamaño_tablero * tamaño_bloque, tamaño_bloque):


            #Dibuja una linea vertical en cada posicion
            #Desde la parte superior hasta la inferior (row, 0) -> (row, altura_total)
            pygame.draw.line(self.screen, gris_claro, (row, 0), (row, tamaño_tablero * tamaño_bloque), width=grosor_linea)
        for col in range(-1, tamaño_tablero * tamaño_bloque, tamaño_bloque):


            #Dibuja 4 lineas verticales en x = -1, 100, 200, 300
            #Dibuja 4 lineas horizontales en y = -1, 100, 200, 300
            #Crea una cuadricula visible de 3x3
            pygame.draw.line(self.screen, gris_claro, (0, col), (tamaño_tablero * tamaño_bloque, col), width=grosor_linea)




    #Caracteristicas del tablero del juego
    def dibujar(self):
        #Establecemos el color de fondo del tablero
        self.screen.fill(BGcolor)

        #Hacemos un llamado a la funcion dibujar_cuadricula para poder observar el table en el ejecutable
        self.dibujar_cuadricula()  
        pygame.display.flip()




    #Deficion de clase para llevar el control de los eventos
    def eventos(self):




        #Obtenemos informacion de todos los eventos pendientes
        for event in pygame.event.get():
            #Verificamos si el evento es para cerrar
            if event.type == pygame.QUIT:
                #Cierra el pygame
                pygame.quit()
                #Sale del programa
                quit(0)





game = juego()
while True:
    game.nuevo_juego()
    game.iniciar()