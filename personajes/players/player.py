import pygame
import constantes 
from constantes import *
import os
class Player:
    
    def __init__(self,x,y):
        #self.image = image
        self.x = x
        self.y = y
        self.size = 20
        self.inventory = {"wood":0,"stone":0}#wood:madera
        
        #cargar la hoja de sprite
        image_path = os.path.join('assets','images','player','player1.png') #"assets//images//player//player.png"
        self.sprite_sheet = pygame.image.load(image_path).convert_alpha()
        #propiedades de animacion
        self.frame_size = frame_size
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_delay = animation_delay
        self.current_animation = idle_down  # animacion por defecto
        self.moving = False
        self.facing_left = False
        #cargar animaciones frame
        self.animations = self.load_animations()
        self.item_images = {
            "wood" : self.load_item_image("wood.png"),
            "stone": self.load_item_image("small_stone.png")
        }
        #barras de estado atributos
        self.energy = constantes.max_energy
        self.food = constantes.max_food
        self.thirst = constantes.max_thirst
    def load_animations(self):
        animations= {} 
        for state in range(6): #6 animaciones states
            frames = []
            for frame in range( basic_frames):
                surface= pygame.Surface((self.frame_size,self.frame_size),pygame.SRCALPHA)
                surface.blit(self.sprite_sheet,(0,0),(frame * self.frame_size, state * self.frame_size, self.frame_size, self.frame_size))
                if constantes.player != self.frame_size:
                    surface = pygame.transform.scale(surface,(constantes.player,constantes.player))
                    frames.append(surface)
                    animations[state] = frames
        return animations
    def update_animation(self,):#actualizar la animacion
        current_time = pygame.time.get_ticks()
        if current_time - self.animation_timer > self.animation_delay:
            self.animation_timer = current_time
            self.animation_frame =(self.animation_frame + 1) % 6
    #metodo para cargar los items que recolecta
    def load_item_image(self,filename):
        path = f"assets//images//objects//{filename}"
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(image,(40,40))
    #diseño de barras de estado
    def draw(self, windows):#revisar si el cambio es ente draw o en el Draw
        windows.blit(self.image,(self.x,self.y))
        self.draw_status_bars(windows)
        #interfaz.blit(self.image,(self.x,self.y))

    def Draw(self,interfaz):
        current_frame = self.animations[self.current_state][self.animation_frame]
        if self.facing_left:
            current_frame = pygame.transform.flip(current_frame, True, False)
        interfaz.blit(current_frame, (self.x, self.y))
        self.draw_status_bars(interfaz)

    def Move(self, dx, dy,world):#metodo para mover al jugador
        self.moving = dx != 0 or dy != 0
        
        if dy > 0:
            self.current_state = "walk_down"
            self.facing_left = False
        elif dy < 0:
            self.current_state = "walk_up"
            self.facing_left = False
        elif dx > 0:
            self.current_state = "walk_right"
            self.facing_left = False
        elif dx < 0:
            self.current_state = "walk_left"
            self.facing_left = True
        else:
            if self.current_state == "walk_down":
                self.current_state = "idle_down"
            elif self.current_state == "walk_up":
                self.current_state = "idle_up"
            elif self.current_state == "walk_right":
                self.current_state = "idle_right"

        new_x = self.x + dx
        new_y = self.y + dy

        for tree in world.trees:
            if self.check_collision(new_x,new_y , tree):
                self.moving = False
                return
        self.x = new_x
        self.y = new_y
        self.x = max(0,min(self.x,constantes.window_width - constantes.player))
        self.y = max(0,min(self.y,constantes.window_height - constantes.player))

        self.update_animation()
        
        
        #cuando se mueve pierde energia
        self.update_energy(-0.1)

    def check_collision(self,x,y,obj):
        return (x < obj.x + obj.size*0.75 and x + self.size*0.75 > obj.x and y < obj.y + obj.size and 
            y + self.size*0.75 > obj.y)#para que no pise la imagen del arbol
    
    def is_near(self,obj):#funcion para detectar si está cerca
        return (abs(self.x - obj.x) <=  max(self.size,obj.size)+5 and
                abs(self.y - obj.y) <=  max(self.size,obj.size)+5)
    
    def interact(self,world): # metodo para interactuar
        for tree in world.trees:
            if self.is_near(tree):
                if tree.chop():
                    self.inventory["wood"] +=1 # agregar madera al inventario
                    if tree.wood == 0:
                        world.trees.remove(tree)
                return

        for stone in world.small_stone:
            if self.is_near(stone):
                self.inventory["stone"] +=1 # agregar piedras pequeñas al inventario
                world.small_stone.remove(stone) # borrar una vez recolecta
                return
    
    def draw_inventory(self,interfaz):
        background = pygame.Surface((constantes.window_width,constantes.window_height),pygame.SRCALPHA)
        background.fill((constantes.color_transp))
        interfaz.blit(background,(0,0))

        font = pygame.font.Font(None,36)
        title = font.render("inventory",True,constantes.color_white)
        interfaz.blit(title,(constantes.window_width//2 - title.get_width()//2,20))

        item_font = pygame.font.Font(None,24)
        y_offset = 80
        for item,quantity in self.inventory.items():
            if quantity > 0:
                interfaz.blit(self.item_images[item],(constantes.window_width//2 - 60, y_offset))
                text = item_font.render(f"{item.capitalize()}: {quantity}", True, constantes.color_white)
                interfaz.blit(text, (constantes.window_width//2 + 10,y_offset + 10))
                y_offset +=50

        close_text = item_font.render("Press 'I' to close inventory",
                                    True,constantes.color_white)
        interfaz.blit(close_text, (constantes.window_width//2 - close_text.get_width()//2,
                                constantes.window_height - 40))
        
        
    def update_energy(self,amount):
        self.energy = max(0, min(self.energy + amount, constantes.max_energy))

    def update_food(self,amount):
        self.food = max(0, min(self.food + amount, constantes.max_food))

    def update_thirst(self,amount):
        self.thirst = max(0, min(self.thirst + amount, constantes.max_thirst))
    
    def draw_status_bars(self,screen):
        bar_width = 100
        bar_height = 10
        x_offset=10
        y_offset=10
        #barra energia
        pygame.draw.rect(screen, constantes.bar_background,
                                (x_offset, y_offset, bar_width, bar_height))
        pygame.draw.rect(screen, constantes.energy_color,
                         (x_offset, y_offset, bar_width * (self.energy / constantes.max_energy), bar_height))
    
        #barra de comida 
        y_offset += 15
        pygame.draw.rect(screen, constantes.bar_background,
                        (x_offset, y_offset, bar_width, bar_height))
        pygame.draw.rect(screen, constantes.food_color,
                        (x_offset, y_offset, bar_width * (self.food / constantes.max_food), bar_height))
        #barra de sed
        y_offset += 15
        pygame.draw.rect(screen, constantes.bar_background,
                        (x_offset, y_offset, bar_width, bar_height))
        pygame.draw.rect(screen, constantes.thirst_color,
                        (x_offset, y_offset, bar_width * (self.thirst / constantes.max_thirst), bar_height))
        
    def update_status(self):
        self.update_food(-1)
        self.update_thirst(-2)
        #
        if self.food < constantes.max_food * 0.2 or self.thirst < constantes.max_thirst * 0.2:
                self.update_energy(-0.5)  # reduce la energia en base la comida y movimiento
        else:
            self.update_energy(0.1)  # recupera un poco de energia si hay suficiente comida y sed