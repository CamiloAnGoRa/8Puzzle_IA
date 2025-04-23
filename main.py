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

        self.revolver_tiempo = 0
        self.iniciar_rev = False
        self.mov_prev = ""
        self.ini_jue = False
        self.iniciar_crono = 0
        self.tiempo_transcurrido = 0
        self.puntaje = float(self.puntaje()[0])



    ##############################
    ##########Puntaje#############
    ############################## 
    def puntaje(self):
        with open("Puntajes.txt", "r") as file:
            puntajes = file.read().splitlines()
        return puntajes
    

    ##############################
    ##########Guardar#############
    ############################## 
    def guardar(self):
        with open("Puntajes.txt", "w") as file:
            file.write(str("%.3f\n"% self.puntaje))




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
    ##########Revolver############
    ############################## 
    def revolver(self, num_movimientos=100):
    # Inicializa mov_prev si no existe
        if not hasattr(self, 'mov_prev'):
            self.mov_prev = None
    
        for _ in range(num_movimientos):
            # Encuentra la posición del espacio vacío
            espacio_vacio = None
            for row in range(tamaño_tablero):
                for col in range(tamaño_tablero):
                    if self.bloques_grid[row][col] == 0:
                        espacio_vacio = (row, col)
                        break
                if espacio_vacio:
                    break
                
            if not espacio_vacio:
                return  # No se encontró espacio vacío (no debería ocurrir)

            row, col = espacio_vacio
            movimientos_posibles = []

            # Verifica qué movimientos son posibles desde la posición del espacio vacío
            # Derecha (mover bloque de la derecha hacia la izquierda)
            if col < tamaño_tablero - 1:
                movimientos_posibles.append("right")
            # Izquierda (mover bloque de la izquierda hacia la derecha)
            if col > 0:
                movimientos_posibles.append("left")
            # Abajo (mover bloque de abajo hacia arriba)
            if row < tamaño_tablero - 1:
                movimientos_posibles.append("down")
            # Arriba (mover bloque de arriba hacia abajo)
            if row > 0:
                movimientos_posibles.append("up")

            # Evita movimientos que deshagan el anterior
            if self.mov_prev == "right" and "left" in movimientos_posibles:
                movimientos_posibles.remove("left")
            elif self.mov_prev == "left" and "right" in movimientos_posibles:
                movimientos_posibles.remove("right")
            elif self.mov_prev == "up" and "down" in movimientos_posibles:
                movimientos_posibles.remove("down")
            elif self.mov_prev == "down" and "up" in movimientos_posibles:
                movimientos_posibles.remove("up")

            if not movimientos_posibles:
                continue  # Si no hay movimientos posibles (raro, pero por seguridad)
            
            # Elige un movimiento aleatorio
            choice = random.choice(movimientos_posibles)
            self.mov_prev = choice

            # Realiza el movimiento (intercambia el espacio vacío con el bloque adyacente)
            if choice == "right":  # Mover bloque derecho hacia el espacio vacío
                self.bloques_grid[row][col], self.bloques_grid[row][col + 1] = self.bloques_grid[row][col + 1], self.bloques_grid[row][col]
            elif choice == "left":  # Mover bloque izquierdo hacia el espacio vacío
                self.bloques_grid[row][col], self.bloques_grid[row][col - 1] = self.bloques_grid[row][col - 1], self.bloques_grid[row][col]
            elif choice == "up":  # Mover bloque superior hacia el espacio vacío
                self.bloques_grid[row][col], self.bloques_grid[row - 1][col] = self.bloques_grid[row - 1][col], self.bloques_grid[row][col]
            elif choice == "down":  # Mover bloque inferior hacia el espacio vacío
                self.bloques_grid[row][col], self.bloques_grid[row + 1][col] = self.bloques_grid[row + 1][col], self.bloques_grid[row][col]

        # Actualizar la visualización después de revolver
        #self.all_sprites.empty()
        #self.dibujar_bloques()

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
        self.tiempo_transcurrido = 0
        self.iniciar_crono = False
        self.ini_jue = False
        self.botones = []
        self.botones.append(Boton(775, 100, 200, 50, "Revolver", white, black ))
        self.botones.append(Boton(775, 170, 200, 50, "Reiniciar", white, black ))
        self.botones.append(Boton(775, 240, 200, 50, "Resolver", white, black ))
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
        

        if self.ini_jue:
            if self.bloques_grid == self.bloques_grid_completado:
                self.ini_jue = False
                if self.puntaje > 0:
                    self.puntaje = self.tiempo_transcurrido if self.tiempo_transcurrido < self.puntaje else self.puntaje
                else:
                    self.puntaje = self.tiempo_transcurrido
                self.guardar()

            if self.iniciar_crono:
                self.timer = time.time()
                self.iniciar_crono = False
            self.tiempo_transcurrido = time.time() - self.timer


        #Condicion para revolver el tablero
        if self.iniciar_rev:
            self.revolver()
            self.dibujar_bloques()
            self.revolver_tiempo += 1
            if self.revolver_tiempo > 120: #Si al presionar revolver el tablero llega a los dos segundos, para 
                self.iniciar_rev = False #Pasamos a un estado False o apagado para que no se revuelva mas el tablero
                self.ini_jue = True
                self.iniciar_crono = True

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
            pygame.draw.line(self.screen, gris_claro, (row, 0), (row, alto_tab),width=grosor_linea)

        # Líneas horizontales
        for col in range(-1, alto_tab + 1, tamaño_bloque):  #Comienza antes del borde y termina despues para bordes completos (Horizontal)
            pygame.draw.line(self.screen, gris_claro, (0, col), (ancho_tab, col),width=grosor_linea)


    ##############################
    #######dibujo_juego###########
    ############################## 
    def dibujar(self):
        self.screen.fill(BGcolor) #Limpar pantalla
        self.dibujar_cuadricula() #Dibuja el tablero
        for Boton in self.botones:
            Boton.dibujar(self.screen)
        UIElement(710, 380, "Puntaje mas alto - %.3f" % (self.puntaje if self.puntaje > 0 else 0)).dibujar(self.screen)
        #Cronometro en la parte superior de los botones, inicia y solo muestra 3 de los decimales para que no se salga de la pantalla
        UIElement(825, 35, '%.3f' % self.tiempo_transcurrido).dibujar(self.screen)
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
                            
                for boton in self.botones:
                    if boton.click(mouse_x, mouse_y):
                        if boton.text == "Revolver":
                            self.revolver_tiempo = 0
                            self.iniciar_rev = True
                        if boton.text == "Reiniciar":
                            self.nuevo_juego()
                        #if boton.text == "Resolver":


##############################
#########bucle################
############################## 
game = juego() #Creacion de la instancia de juego
while True: #Bucle infinito del programa
    game.nuevo_juego() #Incia el nuevo juego
    game.iniciar() #Comienza el bucle del juego