# 8Puzzle_IA
Objetivo del Proyecto
Desarrollar un juego interactivo del 8-puzzle que permita:

1. Resolver el tablero de forma manual, promoviendo la comprensión del espacio de estados.

2. Resolver el tablero de forma automática, permitiendo al usuario seleccionar entre diferentes algoritmos de búsqueda y comparar su rendimiento.

Modo 1: Juego Manual Interactivo
Descripción:

El jugador podrá mover las fichas libremente para intentar resolver el puzzle sin ayuda algorítmica. Este modo fomenta la exploración y el razonamiento por parte del usuario.

Requisitos funcionales:

- Visualización gráfica del tablero 3x3 con casilla vacía.

- Movimiento manual de fichas por clic o arrastre.

- Botones para:

- Reiniciar

- Aleatorizar el tablero

- Verificar si se alcanzó el objetivo

- Contador de movimientos

- Opción para definir el estado inicial manualmente o generarlo aleatoriamente

Extensiones Opcionales:

- Sistema de puntaje o niveles de dificultad.

- Temporizador con retos contrarreloj.

- Efectos visuales o sonoros al mover fichas o alcanzar el objetivo.

Modo 2: Resolución Automática con Algoritmos IA
Descripción:

Este modo permite al usuario seleccionar un algoritmo de búsqueda para que el sistema resuelva automáticamente el 8-puzzle desde un estado inicial aleatorio o definido. El juego mostrará los pasos hacia la solución y presentará métricas de comparación.

Algoritmos disponibles:

1. Búsqueda en anchura (BFS)

2. Búsqueda en profundidad limitada (DFS limitada)

3. Búsqueda A* con heurística de Manhattan

Interfaz requerida:

- Selector para elegir el algoritmo.

- Opción para definir el estado inicial manualmente o generarlo aleatoriamente

- Botón "Resolver" para iniciar la búsqueda.

- Visualización paso a paso de la solución.

- Tabla comparativa con:

- Tiempo de ejecución

- Número de nodos expandidos

- Longitud del camino encontrado

- Recomendación final automática del algoritmo más eficiente para el caso.

Extensiones Opcionales:

- Ejecución paralela de algoritmos con comparación en tiempo real.

- Exportación de trayectorias o animaciones.

- Visualización tipo grafo de estados explorados.

- Implementación en interfaz web (Flask, Streamlit, etc.)



############################# SOLUCION #######################################

librerias a usar archivo main.py
- pygame (import pygame) (conda install -c conda-forge pygame) 
- random (import random)
- time (import time)
- sprite (archivo creador por nosotros "sprite.py") (from sprite import *)
- settings (archivo creado por nosotros "settings.py") (from settings import *)


Diagrama juego
INICIO
  |
  v
Establecer jugando=True
  |
  v
┌───────────────────────┐
│ while self.jugando:   │
│   │                   │
│   v                   │
│  Control FPS          │
│   │                   │
│   v                   │
│  Procesar Eventos     │
│   │                   │
│   v                   │
│  Actualizar Lógica    │
│   │                   │
│   v                   │
│  Dibujar Pantalla     │
│   │                   │
│   └───────────────────┘
  |
  v
FIN (cuando jugando=False) 

Clase juego
- def __init__
- def crear_juego
- def dibujar_bloques
- def nuevo_juego
- def iniciar
- def actualizar
- def dibujar_cuadricula
- def dibujar
- def eventos


Bucle del juego


Configuraciones archivo settings.py
Colores, sombras, tamaños, titulo, lineas del tablero

Configuraciones archivo sprite.py
Librerias usadas
- pygame (import pygame)
- settings (Archivo creado por nosotro) (from settings import *)
Clase Bloque
- def __init__
- def actualizacion
- def click