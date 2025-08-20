
import pygame
import constantes
from personajes.elements.trees import Tree,SmallStone
import random
import os
from pygame import Surface
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
        #sistema de dia y noche
        self.current_time = constantes.morning_time #comienza a las 8:00
        self.day_overlay = Surface((self.width,self.height)) # establecer transparencia
        self.day_overlay.fill(constantes.day_color) # color de dia
        self.day_overlay.set_alpha(0) # opacidad
        
    def update_time(self,dt):
        self.current_time = (self.current_time + dt) % constantes.day_length
        #color y la intensidad basdos en la hora del dia
        if constantes.morning_time <= self.current_time < constantes.dusk_time:
            #durante el dia (8:00-18:00)
            self.day_overlay.fill(constantes.day_color)
            alpha = 0
        elif constantes.dawn_time <= self.current_time < constantes.morning_time:
            #durante el amanecer (6:00-8:00)
            self.day_overlay.fill(constantes.dawn_dusk_color)
            morning_progress = (self.current_time - constantes.dawn_time) / (
                        constantes.morning_time - constantes.dawn_time)
            alpha = int(constantes.max_darkness * (1 - morning_progress))
        else: 
            #entre 00: y 06:00 noche
            self.day_overlay.fill(constantes.night_color)
            alpha = constantes.max_darkness          
        self.day_overlay.set_alpha(alpha)

    def Draw(self,interfaz):
        for y in range(0,self.height,constantes.grass):
            for x in range(0,self.width,constantes.grass):
                interfaz.blit(self.grass_image,(x,y))


        for stone in self.small_stone: # dibujar piedras pequeñas
            stone.Draw(interfaz)
        for tree in self.trees: # dibujar arboles
            tree.Draw(interfaz)
        
        interfaz.blit(self.day_overlay,(0,0))#aplicar efecto de dia/noche

    def draw_inventory(self,interfaz,player):
        font = pygame.font.Font(None,24)
        instruction_text = font.render("Press 'I' to open inventory",
                                    True,constantes.color_white)
        interfaz.blit(instruction_text,(10,10))
        
