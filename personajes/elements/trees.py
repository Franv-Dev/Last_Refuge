import pygame
import constantes

class Tree:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.wood = 5
        image_path = "assets//images//objects//tree.png"
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (constantes.tree, constantes.tree))
        self.size = self.image.get_width()

    def draw(self, interfaz, camera_x, camera_y):
        interfaz_x = self.x - camera_x
        interfaz_y = self.y - camera_y
        if (interfaz_x + self.size >= 0 and interfaz_x <= constantes.window_width and
            interfaz_y + self.size >= 0 and interfaz_y <= constantes.window_height):
            interfaz.blit(self.image, (interfaz_x, interfaz_y))

    def chop(self, with_axe=False):
        if self.wood > 0:
            if with_axe:
                self.wood -= 2
                if self.wood < 0:
                    self.wood = 0
            else:
                self.wood -= 1
            return True
        return False

    def is_depleted(self):
        return self.wood <= 0


class SmallStone:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.stone = 1
        image_path = "assets//images//objects//stone.png"
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (constantes.small_stone, constantes.small_stone))
        self.size = self.image.get_width()

    def draw(self, interfaz, camera_x, camera_y):
        interfaz_x = self.x - camera_x
        interfaz_y = self.y - camera_y
        if (interfaz_x + self.size >= 0 and interfaz_x <= constantes.window_width and
            interfaz_y + self.size >= 0 and interfaz_y <= constantes.window_height):
            interfaz.blit(self.image, (interfaz_x, interfaz_y))

    def collect(self):
        if self.stone > 0:
            self.stone -= 1
            return True
        return False

    def is_depleted(self):
        return self.stone <= 0
