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