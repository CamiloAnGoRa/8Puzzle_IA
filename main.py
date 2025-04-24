##############################
##########Librerias###########
############################## 
import pygame  #Libreria principal de creacion de juegos en python
import random #Genera numeros aleatorios (posiciones, comportamientos aleatorios)
import time #Manejo de tiempos y retrasos
from sprite import * #Archivo de sprites o modelos para el juegos sprite.py
from settings import * #Archivo de configuraciones base para detalles del juego settings.py
from metodos_busqueda import * #Archivo de algoritmos de busqueda base para resolver el puzzle de manera automatica


##############################
##########Clases##############
############################## 
class juego:
    #Ejecucion inmediata de manera automatica al crear una instancia de clase
    def __init__(self): 
        pygame.init() #Inicia todos los modulos de pygame, necesarios llamarlo antes de usar cualquier funcion de pygame
        self.screen = pygame.display.set_mode((width, height))#Creacion de pantalla de juego 
        pygame.display.set_caption(titulo)#Titulo de la pantalla de juego
        self.clock = pygame.time.Clock()#Creacion de un objeto clock, control los fps del juego (misma velocidad en distintos dispositivos)
        self.revolver_tiempo = 0 #El tiempo cuando se elige la opcion de resolver inicializa en 0 para determinar cuando se demoro el algoritmo
        self.iniciar_rev = False #Revolverlo solo hasta que se seleccione para iniciar el juego
        self.mov_prev = "" #guardar los movimientos anteriores para los algoritmos de busqueda
        self.ini_jue = False #El juego inicia hasta que se revuelva, todos los parametros se encuentra en 0 inicialmente
        self.iniciar_crono = 0 #Tiempo en 0 hasta que se revuelva el tablero
        self.tiempo_transcurrido = 0 #Inicia en 0 el tiempo y va incrementandose
        self.movimientos = 0 #Contador de movimientos iniciando en 0 
        self.puntaje, self.mejor_movimientos = self.leer_puntajes()# Leer puntajes del archivo


    ##############################
    ##########Puntaje#############
    ############################## 
    def leer_puntajes(self):#Lectura de datos del archivo
        try:
            with open("Puntajes.txt", "r") as file: #with para cerrar el archivo de manera correcta, "r" para abrir el archivo en modo lectura
                contenido = file.readlines() #Leer todas las lineas del archivo, retorno de lista donde cada linea es un elemento
                if contenido: #Comprobar si el archivo se encuentra vacio
                    primera_linea = contenido[0].strip() #Toma desde la primera linea, el strip elimina los espacion en blanco y los saltos de linea
                    if "," in primera_linea:
                        tiempo, movimientos = primera_linea.split(",") #split separa los valores ","
                        return float(tiempo), int(movimientos)
                    else:
                        return float(primera_linea), 0
                else:
                    return 0, 0 
        except:
            return 0, 0 #En caso de errores retorna los valores 0,0


    ##############################
    ##########Guardar#############
    ############################## 
    def guardar(self):
        datos_algoritmos = {} #Diccionario vacio de almacenamiento de datos para los algoritmos
        try: #Manejo de errores
            with open("Puntajes.txt", "r") as file: #Modo lectura, cerramos el archivo correctamente
                lineas = file.readlines() #Leer todas las lineas del archivo y guardarlos en una lista
                manual_data = lineas [0].strip() #Primera linea "0", eliminamos espacio con strip, puntajes manuales
                for i in range(1, len(lineas)): #Iteracion desde la segunda linea para los datos de los algoritmos
                    partes = lineas[i].strip().split(",") #Dividir cada linea por ","
                    if len(partes) >=4: #Verificacion de cada linea 4 elemtentos (algoritmo, 3 metricas)
                        algo = partes[0] #Nombre del algoritmo como primer elemento
                        datos_algoritmos[algo] = ",".join(partes[1:]) #Union de elementos por medio de ",", guardar en el diccionario
        except:
            manual_data = f"{self.puntaje:.3f},{self.mejor_movimientos}" #Creacion de datos manuales usando valores actuales
        with open("Puntajes.txt", "w") as file: #Archivo en modo escritura, sobreescribe el contenido existente
            file.write(f"{self.puntaje:.3f},{self.mejor_movimientos}\n") #Escribir los nuevos puntajes manuales
            if self.stats_solucion and self.stats_solucion["exito"]: #Verificacion de estadisticas de solucion "Exitosa"
                algoritmo = self.stats_solucion.get("algoritmo", "BFS") #Algoritmo BFS como predeterminado
                #formatear y guardar datos del algoritmo, tiempo, longitd, nodos
                datos_algoritmos[algoritmo] = f"{self.stats_solucion['tiempo_ejecucion']:.3f},{self.stats_solucion['longitud_camino']},{self.stats_solucion['nodos_expandidos']}"
            for algo, datos in datos_algoritmos.items(): #Escribir todos los datos de algoritmos
                file.write(f"{algo},{datos}\n") #Una linea por cada algoritmo con datos


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
    def revolver(self, num_movimientos=100): #Cantidad de movimientos aleatorios
        if not hasattr(self, 'mov_prev'): #hasatt, funcion para verificar si un objeto tiene un atributo especifico, maneja el estado de movimiento previo
            self.mov_prev = None #Verificar si existe un movimiento previo, en caso de que no es iniciado como "none"
        for _ in range(num_movimientos): #Realizar la cantidad de num_movimientos, "_" para variables que no se usan
            espacio_vacio = None #Buscamos el espacio vacio en el tablero
            for row in range(tamaño_tablero):
                for col in range(tamaño_tablero):#Revisamos cada celda
                    if self.bloques_grid[row][col] == 0:
                        espacio_vacio = (row, col)
                        break#Al encontrar el espacio vacio, guarda la posicion en espacio vacio, salimos del bucle
                if espacio_vacio:
                    break
            if not espacio_vacio:
                return  # No se encontro espacio vacio (no deberia ocurrir)
            row, col = espacio_vacio
            movimientos_posibles = [] #Lista vacia para almacenar los movimientos validos
            # Verifica que movimientos son posibles desde la posicion del espacio vacio
            if col < tamaño_tablero - 1:
                movimientos_posibles.append("right")#Derecha (mover bloque de la derecha hacia la izquierda)
            if col > 0:
                movimientos_posibles.append("left")#Izquierda (mover bloque de la izquierda hacia la derecha)
            if row < tamaño_tablero - 1:
                movimientos_posibles.append("down")#Abajo (mover bloque de abajo hacia arriba)
            if row > 0:
                movimientos_posibles.append("up")#Arriba (mover bloque de arriba hacia abajo)
            #Evita movimientos que deshagan el anterior
            if self.mov_prev == "right" and "left" in movimientos_posibles:
                movimientos_posibles.remove("left")
            elif self.mov_prev == "left" and "right" in movimientos_posibles:
                movimientos_posibles.remove("right")
            elif self.mov_prev == "up" and "down" in movimientos_posibles:
                movimientos_posibles.remove("down")
            elif self.mov_prev == "down" and "up" in movimientos_posibles:
                movimientos_posibles.remove("up")
            if not movimientos_posibles:
                continue  #Si no hay movimientos posibles
            choice = random.choice(movimientos_posibles) #Elige un movimiento aleatorio
            self.mov_prev = choice
            if choice == "right":  # Mover bloque derecho hacia el espacio vacio
                self.bloques_grid[row][col], self.bloques_grid[row][col + 1] = self.bloques_grid[row][col + 1], self.bloques_grid[row][col]
            elif choice == "left":  # Mover bloque izquierdo hacia el espacio vacio
                self.bloques_grid[row][col], self.bloques_grid[row][col - 1] = self.bloques_grid[row][col - 1], self.bloques_grid[row][col]
            elif choice == "up":  # Mover bloque superior hacia el espacio vacio
                self.bloques_grid[row][col], self.bloques_grid[row - 1][col] = self.bloques_grid[row - 1][col], self.bloques_grid[row][col]
            elif choice == "down":  # Mover bloque inferior hacia el espacio vacio
                self.bloques_grid[row][col], self.bloques_grid[row + 1][col] = self.bloques_grid[row + 1][col], self.bloques_grid[row][col]


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
        self.movimientos = 0 #Cuenta de movimientos realizados inicia en 0
        self.tiempo_transcurrido = 0 #Tiempo inicia en 0
        self.iniciar_crono = False #Tiempo sin iniciar
        self.ini_jue = False #Juego sin iniciar
        self.botones = [] #Lista de botones de la interfaz
        self.botones.append(Boton(810, 100, 200, 50, "Revolver", white, black )) #posicion, tamaño, valor, color, texto
        self.botones.append(Boton(810, 170, 200, 50, "Reiniciar", white, black )) #posicion, tamaño, valor, color, texto
        self.botones.append(Boton(810, 240, 200, 50, "Resolver", white, black )) #posicion, tamaño, valor, color, texto
        self.botones.append(Boton(810, 310, 55, 35, "BFS", white, black)) #posicion, tamaño, valor, color, texto
        self.botones.append(Boton(875, 310, 55, 35, "DFS", white, black)) #posicion, tamaño, valor, color, texto
        self.botones.append(Boton(940, 310, 55, 35, "A*", white, black)) #posicion, tamaño, valor, color, texto
        self.resolviendo = False # Variables para la solución automática
        self.solucion_pasos = []
        self.paso_actual = 0
        self.tiempo_paso = 0
        self.algoritmo_seleccionado = "BFS" #Algoritmo por defecto
        self.stats_solucion = None
        try:  #Leer datos si existen
            with open("Puntajes.txt", "r") as file:
                lineas = file.readlines()
                #La primera linea contiene los datos del juego manual
            #A partir de la segunda línea estan los datos de los algoritmos
            for i in range(1, len(lineas)): #len devuelve el numero total de lineas en el archivo y determina el limite superior del rango
                datos_algoritmo = lineas[i].strip().split(",") #Dividir espacio de linea con ","
                if len(datos_algoritmo) >= 4:
                    nombre_algoritmo = datos_algoritmo[0]
                    if nombre_algoritmo == self.algoritmo_seleccionado:#Si el algoritmo coincide con el seleccionado, cargar sus datos
                        self.stats_solucion = {
                            "exito": True,
                            "algoritmo": nombre_algoritmo,
                            "tiempo_ejecucion": float(datos_algoritmo[1]),
                            "longitud_camino": int(datos_algoritmo[2]),
                            "nodos_expandidos": int(datos_algoritmo[3])
                        }
                        break  #Encontramos los datos del algoritmo actual
        except:
            pass
        self.dibujar_bloques()  #Llamado de metodo para representacion visual en objetos, de manera inmediata para tener los bloques listos


    ##############################
    #######inicio_juego###########
    ############################## 
    def iniciar(self):
        self.jugando = True #Inicia el bucle principal, termina el juego al cambiar el estado de True->False
        self.solucion_pasos = [] #Lista vacia para almacenar los pasos de la solucion
        self.resolviendo = False #Resolver solo se activa hasta que el usuario le de click
        self.paso_actual = 0
        self.tiempo_paso = 0
        self.stats_solucion = None
        while self.jugando: #Bucle ejecutado mientras el estado sea True
            self.clock.tick(fps) #Regula la velocidad del juego
            self.eventos() #Procesa todoos los enventos generados por el usuarios, 
            self.actualizar() #Actualiza la logica del juego en "Posiciones, colisiones, Estado, condiciones de terminado"
            self.dibujar() #Dibuja los elementos del tablero


    ##############################
    #######actualizaciones########
    ############################## 
    def actualizar(self):
        if not self.resolviendo: #Solo ejecutar cuando no se esta resolviendo automaticamente
            if self.ini_jue: #Solo ejecutar cuando el juego este iniciado
                if self.bloques_grid == self.bloques_grid_completado: #Verificar si el tablero actual esta resuelto
                    self.ini_jue = False #Se termina el juego
                    if self.puntaje <= 0 or self.tiempo_transcurrido < self.puntaje: #Comprobar si es el mejor puntaje o es el primer puntaje que se registra
                        self.puntaje = self.tiempo_transcurrido #Guarda el tiempo record
                        self.mejor_movimientos = self.movimientos  # Guardar los movimientos iguales al mejor tiempo
                        self.guardar() #Los guarda dentor del txt
                if self.iniciar_crono: #Comprobar si iniciar el tiempo
                    self.timer = time.time() #Guardar tiempo actual como punto referencia
                    self.iniciar_crono = False #Evitar que se reinicie el coronometro en frame
                self.tiempo_transcurrido = time.time() - self.timer #Tiempo actual diferente al inicio
        if self.iniciar_rev: #Condicion para revolver el tablero
            self.revolver() #llamar metodo para revolver
            self.dibujar_bloques() #llama metodo para dibujar los bloques del tablero
            self.revolver_tiempo += 1 #Aumentar contador de frames de la animacion
            if self.revolver_tiempo > 120: #Si al presionar revolver el tablero llega a los dos segundos, para (a 60fps)
                self.iniciar_rev = False #Pasamos a un estado False o apagado para que no se revuelva mas el tablero
                self.ini_jue = True #Terminar de mezclar el tablero y iniciar juego
                self.iniciar_crono = True #Iniciar el temporizador
        if self.resolviendo and self.solucion_pasos:# Manejo de la solución paso a paso
            if self.tiempo_paso >= 15:  # Esperar 0.5 segundos entre pasos (30 frames a 60 FPS)
                if self.paso_actual < len(self.solucion_pasos): #Comprobar si hay pasos pendientes para mostrar
                    _, nuevo_tablero = self.solucion_pasos[self.paso_actual]#Extrar el nuevo estado del tablero (paso actual)
                    self.bloques_grid = []#Crear una copia profunda del tablero para evitar problemas de referencia
                    for fila in nuevo_tablero:
                        self.bloques_grid.append(list(fila))
                    self.all_sprites.empty()#Actualizar la visualizacion
                    self.dibujar_bloques()
                    self.paso_actual += 1#Actualizar contador y tiempo
                    self.movimientos = self.paso_actual
                    self.tiempo_paso = 0
                    self.dibujar()#Forzar dibujo
                else:
                    self.resolviendo = False #Finalizar la resolucion
                    self.ini_jue = False #Permitir reiniciar o revolver el juego
                    if self.bloques_grid == self.bloques_grid_completado:
                        self.guardar()
            else:
                self.tiempo_paso += 1
        self.all_sprites.update()#Asegurarse de que todos los sprites se actualicen correctamente


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
        UIElement(710, 460, "Mejores movimientos - %d" % self.mejor_movimientos).dibujar(self.screen)
        #Cronometro en la parte superior de los botones, inicia y solo muestra 3 de los decimales para que no se salga de la pantalla
        UIElement(825, 35, "Tiempo - %.3f" % self.tiempo_transcurrido).dibujar(self.screen)
        UIElement(825, 70, "Movimientos - %d" % self.movimientos).dibujar(self.screen)
        # Mostrar algoritmo seleccionado actualmente
        UIElement(500, 320, f"Algoritmo seleccionado: {self.algoritmo_seleccionado}").dibujar(self.screen)
        # Mostrar estadísticas de la solución si están disponibles
        if self.stats_solucion:
            y_offset = 500
            algoritmo_usado = self.stats_solucion.get("algoritmo", "BFS")
            UIElement(710, y_offset, f"Algoritmo: {algoritmo_usado}").dibujar(self.screen)
            UIElement(710, y_offset + 30, f"Nodos expandidos: {self.stats_solucion['nodos_expandidos']}").dibujar(self.screen)
            UIElement(710, y_offset + 60, f"Longitud del camino: {self.stats_solucion.get('longitud_camino', 'N/A')}").dibujar(self.screen)
            UIElement(710, y_offset + 90, f"Tiempo de ejecución: {self.stats_solucion['tiempo_ejecucion']:.4f} s").dibujar(self.screen)
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
            if event.type == pygame.MOUSEBUTTONDOWN:#Detectar mouse presionado
                mouse_x, mouse_y = pygame.mouse.get_pos() #Obtener coordenadas (x,y)
                for boton in self.botones: # Procesar clicks en botones primero
                    if boton.click(mouse_x, mouse_y):
                        if boton.text == "Revolver":
                            self.revolver_tiempo = 0
                            self.iniciar_rev = True
                            self.resolviendo = False  #Detener cualquier solucion en progreso
                        elif boton.text == "Reiniciar":
                            self.nuevo_juego()
                            self.resolviendo = False  #Asegurarse de que no este resolviendo
                        elif boton.text == "Resolver":
                            if not self.resolviendo:  #Evitar iniciar multiples soluciones
                                self.resolver_puzzle()
                        elif boton.text in ["BFS", "DFS", "A*"]: #Seleccionar algoritmo de busqueda
                            self.algoritmo_seleccionado = boton.text #Actualizar el metodo elegido
                            print(f"Algoritmo seleccionado: {self.algoritmo_seleccionado}") #Mostrar el cambio de algoritmo
                        return  #Procesamos el click del boton y salimos
                if not self.resolviendo:  #Solo procesar clicks en bloques si no se esta resolviendo
                    for row, bloques in enumerate(self.bloques):
                        for col, bloque in enumerate(bloques):
                            if bloque.click(mouse_x, mouse_y): #Buscar si algun bloque se movio, obtener las coordenadas
                                # Derecha
                                if col < tamaño_tablero - 1 and self.bloques_grid[row][col + 1] == 0:
                                    # Intercambiar valores en la matriz
                                    self.bloques_grid[row][col], self.bloques_grid[row][col + 1] = self.bloques_grid[row][col + 1], self.bloques_grid[row][col]
                                    # Incrementar contador de movimientos
                                    self.movimientos += 1
                                    # Recrear los bloques visuales
                                    self.all_sprites.empty()  # Limpiar sprites antiguos
                                    self.dibujar_bloques()
                                    return  # Salir después de mover
                                # Izquierda
                                elif col > 0 and self.bloques_grid[row][col - 1] == 0:
                                    self.bloques_grid[row][col], self.bloques_grid[row][col - 1] = self.bloques_grid[row][col - 1], self.bloques_grid[row][col]
                                    self.movimientos += 1
                                    self.all_sprites.empty()
                                    self.dibujar_bloques()
                                    return
                                # Arriba
                                elif row > 0 and self.bloques_grid[row - 1][col] == 0:
                                    self.bloques_grid[row][col], self.bloques_grid[row - 1][col] = self.bloques_grid[row - 1][col], self.bloques_grid[row][col]
                                    self.movimientos += 1
                                    self.all_sprites.empty()
                                    self.dibujar_bloques()
                                    return
                                # Abajo
                                elif row < tamaño_tablero - 1 and self.bloques_grid[row + 1][col] == 0:
                                    self.bloques_grid[row][col], self.bloques_grid[row + 1][col] = self.bloques_grid[row + 1][col], self.bloques_grid[row][col]
                                    self.movimientos += 1
                                    self.all_sprites.empty()
                                    self.dibujar_bloques()
                                    return


    ##############################
    #########resolver#############
    ##############################
    def resolver_puzzle(self):
        if self.bloques_grid == self.bloques_grid_completado: # Verificar si el juego ya esta resuelto
            return
        self.resolviendo = False
        #llamado a funcion del metodo que almacena los algotirmos (estado acutal, objetivo, algoritmo, tamaño)
        resultado = resolver_puzzle(self.bloques_grid, self.bloques_grid_completado, self.algoritmo_seleccionado, tamaño_tablero)
        if resultado["exito"]: #Comprobar si se encontro solucion
            self.solucion_pasos = resultado["camino"]# Guardar la solucion para la visualizacion paso a paso
            self.stats_solucion = resultado #Alamacena los datos
            self.stats_solucion["algoritmo"] = self.algoritmo_seleccionado #Guardar el algoritmo usado
            self.resolviendo = True #Mostrar la solucion
            self.paso_actual = 0 #Mostrar solucion desde el primer paso
            self.tiempo_paso = 0
            self.ini_jue = False#Detener el temporizador del juego manual
            print(f"Solucion encontrada con {self.algoritmo_seleccionado}: {len(self.solucion_pasos)} pasos")#Imprimir algunos datos para depuracion
        else:
            print(f"No se pudo encontrar una solucion con {self.algoritmo_seleccionado}: {resultado.get('error', 'Error desconocido')}")#Mensaje de error en caso de no haber solucion
            self.stats_solucion = resultado
            self.stats_solucion["algoritmo"] = self.algoritmo_seleccionado  #Guardar el algoritmo usado


##############################
#########bucle################
############################## 
game = juego() #Creacion de la instancia de juego
while True: #Bucle infinito del programa
    game.nuevo_juego() #Incia el nuevo juego
    game.iniciar() #Comienza el bucle del juego