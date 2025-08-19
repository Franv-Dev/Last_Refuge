import pygame
import constantes
class Tree:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.wood = 5
        image_path = "assets//images//objects//tree.png"
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image,(constantes.tree,constantes.tree))
        self.size = self.image.get_width()

    def Draw(self,interfaz):
        interfaz.blit(self.image,(self.x,self.y))

    def chop(self):
        if self.wood > 0:
            self.wood -= 1
            return True
        return False
class SmallStone:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.stone = 1
        image_path = "assets//images//objects//stone.png"
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image,(constantes.small_stone,constantes.small_stone))
        self.size = self.image.get_width()

    
    def Draw(self,interfaz):
        interfaz.blit(self.image,(self.x,self.y))
    