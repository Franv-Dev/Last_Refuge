
import pygame
import constantes
from personajes.elements.trees import Tree,SmallStone
import random
class World:

    def __init__(self,width,height):
        self.width = width
        self.height = height

        self.trees = [Tree(random.randint(0,width-constantes.tree),
                            random.randint(0,height-constantes.tree))for _ in range(10)] # aparezcan aleatoriamente arboles
        
        self.small_stone = [SmallStone(random.randint(0,width-constantes.small_stone),
                            random.randint(0,height-constantes.small_stone))for _ in range(20)]# aparezcan aleatoriamente piedras pequeñas

        imagen_path = "assets//images//objects//grass.png"
        self.grass_image = pygame.image.load(imagen_path)
        self.grass_image = pygame.transform.scale(self.grass_image,(constantes.grass,constantes.grass))
    
    def Draw(self,interfaz):
        for y in range(0,self.height,constantes.grass):
            for x in range(0,self.width,constantes.grass):
                interfaz.blit(self.grass_image,(x,y))


        for stone in self.small_stone: # dibujar piedras pequeñas
            stone.Draw(interfaz)
        for tree in self.trees: # dibujar arboles
            tree.Draw(interfaz)
    
    def draw_inventory(self,interfaz,player):
        font = pygame.font.Font(None,24)
        instruction_text = font.render("Press 'I' to open inventory",
                                    True,constantes.color_white)
        interfaz.blit(instruction_text,(10,10))
        
      