import time 
import heapq
from collections import deque

##############################
#########Estado###############
############################## 
class Estado:
    def __init__(self, tablero, padre=None, accion=None, costo=0):
        self.tablero = tablero  # La matriz del tablero
        self.padre = padre      # Estado padre del cual se derivó este estado
        self.accion = accion    # La acción que llevó a este estado ("up", "down", "left", "right")
        self.costo = costo      # Costo acumulado para llegar a este estado
        self.vacio_pos = None   # Posición del espacio vacío (0)
        
        # Encontrar la posición del espacio vacío
        for i in range(len(tablero)):
            for j in range(len(tablero[0])):
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
        ("up", -1, 0),    # Mover el espacio vacio hacia arriba (bloque de arriba hacia abajo)
        ("down", 1, 0),   # Mover el espacio vacio hacia abajo (bloque de abajo hacia arriba)
        ("left", 0, -1),  # Mover el espacio vacio hacia la izquierda (bloque de la izquierda hacia la derecha)
        ("right", 0, 1)   # Mover el espacio vacio hacia la derecha (bloque de la derecha hacia la izquierda)
    ]
    
    for accion, dr, dc in direcciones:
        nuevo_row, nuevo_col = row + dr, col + dc #Calcula la nueva posicion
        
        # Verifica si el movimiento esta dentro de los límites del tablero
        if 0 <= nuevo_row < tamaño_tablero and 0 <= nuevo_col < tamaño_tablero:
            # Crear un nuevo tablero con el movimiento realizado
            nuevo_tablero = [list(fila) for fila in estado.tablero]  # Copiar el tablero
            
            # Intercambiar el espacio vacío con el bloque adyacente
            nuevo_tablero[row][col], nuevo_tablero[nuevo_row][nuevo_col] = nuevo_tablero[nuevo_row][nuevo_col], nuevo_tablero[row][col]
            
            # Crear el nuevo estado
            sucesor = Estado(nuevo_tablero, estado, accion, estado.costo + 1)
            sucesores.append(sucesor) 
    
    return sucesores #Devuelve la lista de todos los estados sucesores validos


##############################
#########estado_ob############
############################## 
def es_objetivo(estado, estado_objetivo):
    return estado.tablero == estado_objetivo


##############################
#########rec_camino###########
##############################
def reconstruir_camino(estado):
    camino = []
    while estado.padre:
        camino.append((estado.accion, estado.tablero))
        estado = estado.padre
    return camino[::-1]  # Invertir para obtener el camino desde el inicio hasta el objetivo

##############################
###########BFS################
##############################
def bfs(estado_inicial, estado_objetivo, tamaño_tablero):
    tiempo_inicio = time.time()
    frontera = deque([Estado(estado_inicial)])
    explorados = set()
    nodos_expandidos = 0
    
    while frontera:
        estado_actual = frontera.popleft()
        nodos_expandidos += 1
        
        # Verificar si hemos llegado al estado objetivo
        if es_objetivo(estado_actual, estado_objetivo):
            tiempo_fin = time.time()
            camino = reconstruir_camino(estado_actual)
            return {
                "exito": True,
                "camino": camino,
                "nodos_expandidos": nodos_expandidos,
                "longitud_camino": len(camino),
                "tiempo_ejecucion": tiempo_fin - tiempo_inicio
            }
        
        # Añadir el estado actual a los explorados
        estado_hash = hash(tuple(tuple(row) for row in estado_actual.tablero))
        if estado_hash in explorados:
            continue
            
        explorados.add(estado_hash)
        
        # Obtener sucesores
        for sucesor in obtener_sucesores(estado_actual, tamaño_tablero):
            sucesor_hash = hash(tuple(tuple(row) for row in sucesor.tablero))
            if sucesor_hash not in explorados:
                frontera.append(sucesor)
    
    # Si no se encuentra solución
    tiempo_fin = time.time()
    return {
        "exito": False,
        "nodos_expandidos": nodos_expandidos,
        "tiempo_ejecucion": tiempo_fin - tiempo_inicio
    }



##############################
##########resolve#############
##############################
def resolver_puzzle(tablero_actual, tablero_objetivo, algoritmo, tamaño_tablero):
    if algoritmo == "BFS":
        return bfs(tablero_actual, tablero_objetivo, tamaño_tablero)
    else:
        return {"exito": False, "error": "Solo se ha implementado el algoritmo BFS"}