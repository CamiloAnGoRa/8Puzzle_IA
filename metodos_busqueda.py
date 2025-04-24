import time 
import heapq
from collections import deque

##############################
#########Estado###############
############################## 
class Estado:
    def __init__(self, tablero, padre=None, accion=None, costo=0):
        self.tablero = tablero #La matriz del tablero
        self.padre = padre  #Estado padre del cual se derivo este estado
        self.accion = accion #La accion que llevo a este estado ("up", "down", "left", "right")
        self.costo = costo  #Costo acumulado para llegar a este estado
        self.vacio_pos = None #Posicion del espacio vacio (0)
        for i in range(len(tablero)): #Encontrar la posicion del espacio vacio
            for j in range(len(tablero[0])): #Al encontar el espacio vacio, guarda las coordenadas como tupla
                if tablero[i][j] == 0:
                    self.vacio_pos = (i, j)
                    break
            if self.vacio_pos:
                break
    

    ##############################
    #########Estado###############
    ############################## 
    def __eq__(self, other): #Metodo de python usado para definir comportamiento de comparacion de igualdad entre objetos de una clase
        return self.tablero == other.tablero
    

    ##############################
    #########Estado###############
    ############################## 
    def __hash__(self): #Metodo de python que permite a los objetos de tu clase ser usado como caves
        # Convertir la matriz en una tupla para poder usarla como llave en un diccionario
        return hash(tuple(tuple(row) for row in self.tablero))
    

    ##############################
    #########Estado###############
    ############################## 
    def __lt__(self, other): 
        # Para comparación en la cola de prioridad en A*
        return self.costo < other.costo
    


##############################
#########Sucesores############
############################## 
def obtener_sucesores(estado, tamaño_tablero): #Genera todos los posibles estados sucesores o (movimientos validos) a partir de un estado actual del puzzle
    sucesores = []
    row, col = estado.vacio_pos #Obtiene las coordenadas del espacio vacio "0"
    # Posibles movimientos: arriba, abajo, izquierda, derecha
    direcciones = [
        ("up", -1, 0), #Mover el espacio vacio hacia arriba (bloque de arriba hacia abajo)
        ("down", 1, 0), #Mover el espacio vacio hacia abajo (bloque de abajo hacia arriba)
        ("left", 0, -1), #Mover el espacio vacio hacia la izquierda (bloque de la izquierda hacia la derecha)
        ("right", 0, 1) #Mover el espacio vacio hacia la derecha (bloque de la derecha hacia la izquierda)
    ]
    for accion, dr, dc in direcciones:
        nuevo_row, nuevo_col = row + dr, col + dc #Calcula la nueva posicion
        #Verifica si el movimiento esta dentro de los limites del tablero
        if 0 <= nuevo_row < tamaño_tablero and 0 <= nuevo_col < tamaño_tablero:
            #Crear un nuevo tablero con el movimiento realizado
            nuevo_tablero = [list(fila) for fila in estado.tablero]  #Copiar el tablero
            #Intercambiar el espacio vacio con el bloque
            nuevo_tablero[row][col], nuevo_tablero[nuevo_row][nuevo_col] = nuevo_tablero[nuevo_row][nuevo_col], nuevo_tablero[row][col]
            #Crear el nuevo estado
            sucesor = Estado(nuevo_tablero, estado, accion, estado.costo + 1)
            sucesores.append(sucesor)
    return sucesores #Devuelve la lista de todos los estados sucesores validos


##############################
#########estado_ob############
############################## 
def es_objetivo(estado, estado_objetivo): #Definir el estado en el que se quiere terminar el juego
    return estado.tablero == estado_objetivo


##############################
#########rec_camino###########
##############################
def reconstruir_camino(estado):
    camino = [] #Lista vacia para almacenar los pasos del camino
    while estado.padre: #Continuar mientrar el estado no sea el inicial
        camino.append((estado.accion, estado.tablero)) #Añade tupla con movimiento y estado del tablero
        estado = estado.padre #Avanza para atras del arbol de busqueda, el estado actual se vuelve padre del siguiente
    return camino[::-1]  #Invertir para obtener el camino desde el inicio hasta el objetivo


##############################
###########BFS################
##############################
def bfs(estado_inicial, estado_objetivo, tamaño_tablero): #(inicial, objetivo, tamaño)
    tiempo_inicio = time.time() #Registro de inicio para tiempo de ejecucion
    frontera = deque([Estado(estado_inicial)]) #deque (cola doble) alamacena los estados por explorar
    explorados = set() ##alamacena los estados ya visitados para no repetir, usa busquedas eficientes
    nodos_expandidos = 0 #lleva la cuenta de los nodos que se han expandido
    while frontera: #continua mientras existan estados por explorar
        estado_actual = frontera.popleft() #obtiene y elimina el primer estado (FIFO), define comportamiento de busqueda en anchura
        nodos_expandidos += 1 #Incrementa el contador de nodos
        if es_objetivo(estado_actual, estado_objetivo): #verificar si se llego a la solucion
            tiempo_fin = time.time() #registrar el tiempo final si encuentra la solucion
            camino = reconstruir_camino(estado_actual) #obtener la secuencia de movimientos
            return {"exito": True,"camino": camino,"nodos_expandidos": nodos_expandidos,"longitud_camino": len(camino),"tiempo_ejecucion": tiempo_fin - tiempo_inicio} #Devuelve un diccionario con los indicadores exito, solucion y rendimiento
        #Usamos el hash para identificar de cada estado de manera unica, para verificar si un estado ya se visito
        estado_hash = hash(tuple(tuple(row) for row in estado_actual.tablero)) #Converitr el tablero en tupla de tuplas, calcula un hash unico de estado
        if estado_hash in explorados:
            continue #Si el estado ya se visito se salta
        explorados.add(estado_hash) #el estado actual pasa a ser visitado
        for sucesor in obtener_sucesores(estado_actual, tamaño_tablero):#genera todos los estados vecinos posibles
            sucesor_hash = hash(tuple(tuple(row) for row in sucesor.tablero))#calcula el identificador unicio del estado sucesor
            if sucesor_hash not in explorados:#si no fue explorado lio agrega al fuinal
                frontera.append(sucesor)
    tiempo_fin = time.time() #retorna valores aunque no haya encontrado la solucion
    return {"exito": False,"nodos_expandidos": nodos_expandidos,"tiempo_ejecucion": tiempo_fin - tiempo_inicio}


##############################
##########resolve#############
##############################
def resolver_puzzle(tablero_actual, tablero_objetivo, algoritmo, tamaño_tablero):
    if algoritmo == "BFS":
        return bfs(tablero_actual, tablero_objetivo, tamaño_tablero)
    elif algoritmo == "DFS":
        return dfs(tablero_actual, tablero_objetivo, tamaño_tablero)
    elif algoritmo == "A*":
        return astar(tablero_actual, tablero_objetivo, tamaño_tablero)
    else:
        return {"exito": False, "error": "No se pudo resolver"}
    


##############################
########Heuristica############
##############################
def heuristica_manhattan(estado, estado_objetivo):
    #Calcula la distancia Manhattan para cada pieza del puzzle
    h = 0
    n = len(estado.tablero)
    
    #Crear un diccionario que lleve cada valor a su posicion objetivo
    posiciones_objetivo = {}
    for i in range(n):
        for j in range(n):
            posiciones_objetivo[estado_objetivo[i][j]] = (i, j)
    
    #Calcular la distancia Manhattan para cada pieza
    for i in range(n):
        for j in range(n):
            valor = estado.tablero[i][j]
            if valor != 0:  #Ignoramos el espacio vacio
                pos_obj = posiciones_objetivo[valor]
                h += abs(i - pos_obj[0]) + abs(j - pos_obj[1])
    
    return h


##############################
#############A*###############
##############################
def astar(estado_inicial, estado_objetivo, tamaño_tablero):
    tiempo_inicio = time.time()
    #Crear el estado inicial con el tablero inicial
    estado_inicial = Estado(estado_inicial)
    #Inicializar la cola de prioridad con el estado inicial
    frontera = []
    #La prioridad es f(n) = g(n) + h(n), donde g(n) es el costo hasta ahora y h(n) es la heuristica
    f_valor = estado_inicial.costo + heuristica_manhattan(estado_inicial, estado_objetivo)
    heapq.heappush(frontera, (f_valor, id(estado_inicial), estado_inicial)) #heapq.heappush funcion modulo heapq, permite insertar elementos en una cola de proridad
    #Diccionario para almacenar estados visitados y su costo
    explorados = {}
    #Contador de nodos expandidos
    nodos_expandidos = 0
    while frontera:
        #Obtener el estado con menor f(n)
        _, _, estado_actual = heapq.heappop(frontera)
        nodos_expandidos += 1
        #Verificar si hemos llegado al estado objetivo
        if es_objetivo(estado_actual, estado_objetivo):
            tiempo_fin = time.time()
            camino = reconstruir_camino(estado_actual)
            return {"exito": True,"camino": camino,"nodos_expandidos": nodos_expandidos,"longitud_camino": len(camino),"tiempo_ejecucion": tiempo_fin - tiempo_inicio}
        #Generar un hash para el estado actual
        estado_hash = hash(tuple(tuple(row) for row in estado_actual.tablero))
        #Si ya exploramos este estado con un costo menor, no lo expandimos de nuevo
        if estado_hash in explorados and explorados[estado_hash] <= estado_actual.costo:
            continue
        #Marcar como explorado
        explorados[estado_hash] = estado_actual.costo
        #Obtener sucesores
        for sucesor in obtener_sucesores(estado_actual, tamaño_tablero):
            sucesor_hash = hash(tuple(tuple(row) for row in sucesor.tablero))
            #Si no hemos explorado este estado o encontramos un camino mejor
            if sucesor_hash not in explorados or explorados[sucesor_hash] > sucesor.costo:
                # Calcular f(n) = g(n) + h(n)
                f_valor = sucesor.costo + heuristica_manhattan(sucesor, estado_objetivo)
                heapq.heappush(frontera, (f_valor, id(sucesor), sucesor))#heapq.heappush funcion modulo heapq, permite insertar elementos en una cola de proridad
    #Si no se encuentra solucion
    tiempo_fin = time.time()
    return {"exito": False,"nodos_expandidos": nodos_expandidos,"tiempo_ejecucion": tiempo_fin - tiempo_inicio}


##############################
###########DFS################
##############################
def dfs(estado_inicial, estado_objetivo, tamaño_tablero, limite_profundidad=2000):
    tiempo_inicio = time.time()
    #Usamos una lista como pila (append para push, pop para pop)
    frontera = [Estado(estado_inicial)]
    explorados = set()
    nodos_expandidos = 0
    #Para llevar un registro de la profundidad maxima alcanzada
    profundidad_maxima = 0
    while frontera:
        estado_actual = frontera.pop() #Extraer el ultimo elemento (LIFO - pila)
        nodos_expandidos += 1
        profundidad_maxima = max(profundidad_maxima, estado_actual.costo)#Registrar la profundidad maxima
        if es_objetivo(estado_actual, estado_objetivo):#Verificar si hemos llegado al estado objetivo
            tiempo_fin = time.time()
            camino = reconstruir_camino(estado_actual)
            return {"exito": True,"camino": camino,"nodos_expandidos": nodos_expandidos,"longitud_camino": len(camino),"tiempo_ejecucion": tiempo_fin - tiempo_inicio,"profundidad_maxima": profundidad_maxima}
        if estado_actual.costo >= limite_profundidad:#Si excedemos el limite de profundidad, no expandimos el nodo
            continue
        estado_hash = hash(tuple(tuple(row) for row in estado_actual.tablero))#Añadir el estado actual a los explorados
        if estado_hash in explorados:
            continue
        explorados.add(estado_hash)
        sucesores = obtener_sucesores(estado_actual, tamaño_tablero)#Obtener sucesores y añadirlos a la frontera
        for sucesor in sucesores:#random.shuffle(sucesores)
            sucesor_hash = hash(tuple(tuple(row) for row in sucesor.tablero))
            if sucesor_hash not in explorados:
                frontera.append(sucesor)
    tiempo_fin = time.time()#Si no se encuentra solucion
    return {"exito": False,"error": f"No se encontro solucion dentro del limite de profundidad {limite_profundidad}","nodos_expandidos": nodos_expandidos,"tiempo_ejecucion": tiempo_fin - tiempo_inicio,"profundidad_maxima": profundidad_maxima}