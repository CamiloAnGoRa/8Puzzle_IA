import pygame
from settings import *

pygame.font.init() #Inicializacion del modulo de fuentes 


##############################
#########Bloque###############
############################## 
class Bloque(pygame.sprite.Sprite): #Hereda de pygame.sprite.Sprite
    def __init__(self, game, x, y, text): #refencia a la instancia de juego principal, x y posiciones en la cuadricula, texto mostrados en bloques
        self.groups = game.all_sprites #El bloque se añade al grupo all_sprites del juego
        pygame.sprite.Sprite.__init__(self, self.groups) #llamado al constructor pygame.sprite.Sprite, actauliza automaticamente cada frame, dibuja al ser llamado all_sprites.draw
        self.game = game #Mantiene el acceso a las configutaciones, metodos, otros sprites, superficie del juego

        self.image = pygame.Surface((tamaño_bloque, tamaño_bloque)) #Crea una superficie representando el bloque
        self.x, self.y = x, y #Posicion en la cuadricula por medio de coordenada logicas
        self.text = text #Numero del bloque
        self.rect = self.image.get_rect() #Posicion en pantalla
        if self.text != "empty":
            self.font = pygame.font.SysFont("Consolas", 50) #Fuente y tamaño
            font_surface = self.font.render(self.text, True, black) #Superficie de con texto negro
            self.image.fill(white) #Rellena el bloque con blanco
            self.font_size = self.font.size(self.text) #Calculo para centrar
            # Centrar el texto en el bloque
            font_x = (tamaño_bloque - self.font_size[0]) // 2 #Calculo de posicion para centrar horizontal y verticalmente el texto
            font_y = (tamaño_bloque - self.font_size[1]) // 2
            self.image.blit(font_surface, (font_x, font_y)) # blit dibuja la superficie del texto sobre el bloque 
        else:
            self.image.fill(BGcolor) #Color bloque vacio, del mismo del fondo

        # Llama a actualización para posicionar correctamente el rectángulo
        self.actualizacion()




    ##############################
    #########actualizacion########
    ############################## 
    def actualizacion(self): #Convertir las coordenadas logicas "grid" en coordenada de pixeles
        #Mantiene la posicion visual (rect) con la posicion logica x,y
        self.rect.x = self.x * tamaño_bloque #Cooredenada X
        self.rect.y = self.y * tamaño_bloque #Coordenada Y



    ##############################
    #########click################
    ############################## 
    def click(self, mouse_x, mouse_y): #Determina si los clicks del usuario estan por dentro o por fuera del tablero
        #Comprueba la posicion de X si esta o no entre los bordes del bloque (horizontal), Y igualmente (vertical)
        # True = dentro del bloque, False = Fuera del bloque 
        #self.rect alamacena posicion y tamaño, atributos left right, top, bottom
        return self.rect.left <= mouse_x <= self.rect.right and self.rect.top <= mouse_y <= self.rect.bottom




    ##############################
    #########derecha##############
    ############################## 
    def right(self):
        return self.rect.x + tamaño_bloque < tamaño_tablero + tamaño_bloque


    ##############################
    #########izquierda############
    ############################## 
    def left(self):
        return self.rect.x - tamaño_bloque >= 0


    ##############################
    #########arriba###############
    ##############################
    def up(self):
        return self.rect.y - tamaño_bloque >= 0


    ##############################
    #########abajo################
    ############################## 
    def down(self):
        return self.rect.y + tamaño_bloque < tamaño_tablero + tamaño_bloque
    


##############################
############UI################
############################## 

class UIElement:
    def __init__(self, x, y, text):
        self.x, self.y = x, y
        self.text = text

    ##############################
    #########Dibujar##############
    ############################## 
    def dibujar(self, screen):
        font = pygame.font.SysFont("Consolas", 20)
        text = font.render(self.text, True, white)
        screen.blit(text, (self.x, self.y))

##############################
############Boton#############
############################## 
class Boton:
    def __init__(self, x, y, width, height, text, color, text_color):
        self.color, self.text_color = color, text_color
        self.width, self.height = width, height
        self.x, self.y = x, y
        self.text = text
        self.font = pygame.font.SysFont("Consolas", 30)

    def dibujar(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))# Dibujar el rectángulo del botón
        text_surface = self.font.render(self.text, True, self.text_color) # Renderizar el texto
        text_rect = text_surface.get_rect(center=(self.x + self.width // 2,self.y + self.height // 2)) # Obtener el rectángulo del texto y centrarlo en el botón
        screen.blit(text_surface, text_rect) # Dibujar el texto en la pantalla


    def click(self, mouse_x, mouse_y): 
        return self.x <= mouse_x <= self.x + self.width and self.y <= mouse_y <= self.y + self.height
