##############################
##########Librerias###########
############################## 

import pygame  #Libreria principal de creacion de juegos en python
import random #Genera numeros aleatorios (posiciones, comportamientos aleatorios)
import time #Manejo de tiempos y retrasos
from sprite import * #Archivo de sprites o modelos para el juegos sprite.py
from settings import * #Archivo de configuraciones base para detalles del juego settings.py


##############################
##########Clases##############
############################## 

class juego:
    #Ejecucion inmediata de manera automatica al crear una instancia de clase
    def __init__(self): 
        #Inicia todos los modulos de pygame, necesarios llamarlo antes de usar cualquier funcion de pygame
        pygame.init()
        #Creacion de pantalla de juego 
        self.screen = pygame.display.set_mode((width, height))
        #Titulo de la pantalla de juego
        pygame.display.set_caption(titulo)
        #Creacion de un objeto clock, control los fps del juego (misma velocidad en distintos dispositivos)
        self.clock = pygame.time.Clock()



    ##############################
    #######crear_juego############
    ############################## 

    def crear_juego(self):
        #for y in range(tamaño_tablero) genera filas dependiendo de la variable tamaño_tablero "Archivo settings.py" 
        #for x in range(1, tamaño_tablero + 1) genera columnas con valores de 1 al tamaño_tablero
        #x + y * tamaño_tablero genera numeros unicos consecutivos:
        grid = [[x + y * tamaño_tablero for x in range(1, tamaño_tablero + 1)] for y in range(tamaño_tablero)]
        #grid[1] accede a la ultima dila, [-1] accede al ultimo elemento de esa fila, estableciendo que espacio queda vacio "0"
        grid[-1][-1] = 0
        return grid #Devuelve la matriz generada para el juego




    ##############################
    #######dibujar_bloques########
    ############################## 
    def dibujar_bloques(self):
        self.bloques = [] #Lista vacia para almacenar todas las filas de bloques
        for row, x in enumerate(self.bloques_grid): #Recorremos cada fila del grid, mantenemos el indice "row" y el contenido de "x"
            self.bloques.append([]) #Nueva lista vacia para representacion de la fila actual
            for col, valor in enumerate(x):  # enumerate(x) recorre cada valor en la fila actual manteniendo el indice de columna (col) y el valor
                if valor != 0: #Si el valor no es 0 crea un nuevo objeto Bloque
                    #self referencia a la instancia actual, col, row posicion en el grid
                    #str(valor) El valor convertido a cadena como identificador
                    self.bloques[row].append(Bloque(self, col, row, str(valor))) 
                else: #En caso de que el valor sea 0 crea un bloque vacio
                    self.bloques[row].append(Bloque(self, col, row, "empty"))


    ##############################
    #######nuevo_juego############
    ############################## 
    def nuevo_juego(self):
        #Nuevo grupo de sprites vacios
        self.all_sprites = pygame.sprite.Group() #contenedor de pygame para manejo de multipples sprites, permite actualizar y dibujar todos los sprites del juego de forma eficiente
        self.bloques_grid = self.crear_juego() #Llamado de metodo "crear_juego", genera matriz de numeros ordenados, estado inicial del tablero
        self.bloques_grid_completado = self.crear_juego() #Una segunda matriz igual, referencia de juego completado
        self.dibujar_bloques()  # Llamado de metodo para representacion visual en objetos, de manera inmediata para tener los bloques listos


    ##############################
    #######inicio_juego###########
    ############################## 
    def iniciar(self):
        self.jugando = True #Inicia el bucle principal, termina el juego al cambiar el estado de True->False
        while self.jugando: #Bucle ejecutado mientras el estado sea True
            self.clock.tick(fps) #Regula la velocidad del juego
            self.eventos() #Procesa todoos los enventos generados por el usuarios, 
            self.actualizar() #Actualiza la logica del juego en "Posiciones, colisiones, Estado, condiciones de terminado"
            self.dibujar() #Dibuja los elementos del tablero


    ##############################
    #######actualizaciones########
    ############################## 
    def actualizar(self):
        # Asegurarse de que todos los sprites se actualicen correctamente
        self.all_sprites.update()



    ##############################
    #######cuadriculas############
    ############################## 
    def dibujar_cuadricula(self):
        #Numero de casillas por lado
        #Tamaño en pixeles de cada bloque
        #Dimensiones totales del tablero
        ancho_tab = tamaño_tablero * tamaño_bloque
        alto_tab = tamaño_tablero * tamaño_bloque

        # Sombra
        pygame.draw.rect(
            self.screen, 
            shadow_color, #Color de la sombra
            (-shadow_size, -shadow_size, ancho_tab + shadow_size*2, alto_tab + shadow_size*2),
            border_radius=3 
        )

        # Fondo
        pygame.draw.rect(self.screen, BGcolor, (0, 0, ancho_tab, alto_tab))

        # Líneas verticales
        for row in range(-1, ancho_tab + 1, tamaño_bloque): #Comienza antes del borde y termina despues para bordes completos (Vertical)
            pygame.draw.line(
                self.screen, 
                gris_claro, 
                (row, 0), 
                (row, alto_tab),
                width=grosor_linea
            )

        # Líneas horizontales
        for col in range(-1, alto_tab + 1, tamaño_bloque):  #Comienza antes del borde y termina despues para bordes completos (Horizontal)
            pygame.draw.line(
                self.screen, 
                gris_claro, 
                (0, col), 
                (ancho_tab, col),
                width=grosor_linea
            )


    ##############################
    #######dibujo_juego###########
    ############################## 
    def dibujar(self):
        self.screen.fill(BGcolor) #Limpar pantalla
        self.dibujar_cuadricula() #Dibuja el tablero
        self.all_sprites.draw(self.screen)  # Dibuja todos los bloques
        pygame.display.flip() #Actualiza la pantalla


    ##############################
    #########eventos##############
    ############################## 
    def eventos(self):
        for event in pygame.event.get(): #Obtiene los eventos pendientes de la cola de enventos
            if event.type == pygame.QUIT: #Procesa cada evento de manera individual, permite el manejo multiple de eventos
                pygame.quit() #Al dar click en la X de la ventalla se llama a "pygame.quit"
                quit(0) #Termina el programa sin errores, el codigo de salida es (0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for row, bloques in enumerate(self.bloques):
                    for col, bloque in enumerate(bloques):
                        if bloque.click(mouse_x, mouse_y):
                            # Verificar si hay un espacio vacío adyacente
                            # Derecha
                            if col < tamaño_tablero - 1 and self.bloques_grid[row][col + 1] == 0:
                                # Intercambiar valores en la matriz
                                self.bloques_grid[row][col], self.bloques_grid[row][col + 1] = self.bloques_grid[row][col + 1], self.bloques_grid[row][col]
                                # Recrear los bloques visuales
                                self.all_sprites.empty()  # Limpiar sprites antiguos
                                self.dibujar_bloques()
                                return  # Salir después de mover
                            # Izquierda
                            elif col > 0 and self.bloques_grid[row][col - 1] == 0:
                                self.bloques_grid[row][col], self.bloques_grid[row][col - 1] = self.bloques_grid[row][col - 1], self.bloques_grid[row][col]
                                self.all_sprites.empty()
                                self.dibujar_bloques()
                                return
                            # Arriba
                            elif row > 0 and self.bloques_grid[row - 1][col] == 0:
                                self.bloques_grid[row][col], self.bloques_grid[row - 1][col] = self.bloques_grid[row - 1][col], self.bloques_grid[row][col]
                                self.all_sprites.empty()
                                self.dibujar_bloques()
                                return
                            # Abajo
                            elif row < tamaño_tablero - 1 and self.bloques_grid[row + 1][col] == 0:
                                self.bloques_grid[row][col], self.bloques_grid[row + 1][col] = self.bloques_grid[row + 1][col], self.bloques_grid[row][col]
                                self.all_sprites.empty()
                                self.dibujar_bloques()
                                return

##############################
#########bucle################
############################## 
game = juego() #Creacion de la instancia de juego
while True: #Bucle infinito del programa
    game.nuevo_juego() #Incia el nuevo juego
    game.iniciar() #Comienza el bucle del juego