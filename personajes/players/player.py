import os
import pygame
from constantes import *
import constantes
from inventario.inventory import Inventory

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        # ARREGLO: un solo tamaño; el hitbox debe coincidir con lo dibujado
        self.size = constantes.player
        self.inventory = Inventory()

        # Sprite base
        image_path = os.path.join('assets', 'images', 'player', 'player1.png')
        self.sprite_sheet = pygame.image.load(image_path).convert_alpha()

        # Sprite de acciones (hacha)
        self.action_sprite_sheet = pygame.image.load(
            os.path.join('assets', 'images', 'player', 'action_sprites.png')
        ).convert_alpha()

        # Estado animación
        self.frame_size = frame_size
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_delay = animation_delay
        self.current_state = idle_down
        self.moving = False
        self.facing_left = False
        self.is_running = False

        # Hacha
        self.is_chopping = False
        self.chop_timer = 0
        self.chop_frame = 0

        # Animaciones
        self.animations = self.load_animations()
        self.axe_animations = self.load_axe_animations()

        # Barras de estado
        self.energy  = max_energy
        self.food    = max_food
        self.thirst  = max_thirst
        self.stamina = max_stamina

    def load_animations(self):
        animations = {}
        for state in range(6):  # 6 estados
            frames = []
            for frame in range(basic_frames):
                temp_surface = pygame.Surface((self.frame_size, self.frame_size), pygame.SRCALPHA)
                temp_surface.blit(self.sprite_sheet, (0, 0),
                                  (frame * self.frame_size, state * self.frame_size, self.frame_size, self.frame_size))
                surface = pygame.Surface((constantes.player, constantes.player), pygame.SRCALPHA)
                scaled_temp = pygame.transform.scale(temp_surface, (constantes.player, constantes.player))
                surface.blit(scaled_temp, (0, 0))
                frames.append(surface)
            animations[state] = frames
        return animations

    def load_axe_animations(self):
        animation = {}
        # filas 3,4,5 (derecha/abajo/arriba) como en el video
        row_mapping = {3: 3, 4: 4, 5: 5}
        for state, row in row_mapping.items():
            frames = []
            for frame in range(axe_frames):
                temp_surface = pygame.Surface((constantes.action_frame_size, constantes.action_frame_size), pygame.SRCALPHA)
                x = (frame % axe_cols) * constantes.action_frame_size
                frame_rect = pygame.Rect(x, row * constantes.action_frame_size,
                                         constantes.action_frame_size, constantes.action_frame_size)
                # copiar región
                temp_surface.blit(self.action_sprite_sheet, (0, 0), frame_rect)
                # escalar al tamaño del jugador
                action_scale = constantes.action_frame_size / constantes.frame_size
                action_size = int(constantes.frame_size * action_scale)
                surface = pygame.Surface((action_size, action_size), pygame.SRCALPHA)
                scaled_temp = pygame.transform.scale(temp_surface, (action_size, action_size))
                surface.blit(scaled_temp, (0, 0))
                frames.append(surface)
            animation[state] = frames
        return animation

    def update_animation(self):
        current_time = pygame.time.get_ticks()
        if self.is_chopping and current_time - self.chop_timer > constantes.axe_animation_delay:
            self.chop_timer = current_time
            self.chop_frame = (self.chop_frame + 1) % constantes.axe_frames
            if self.chop_frame == 0:  # completada
                self.is_chopping = False
        else:
            animation_speed = running_animation_delay if self.is_running else animation_delay
            if current_time - self.animation_timer > animation_speed:
                self.animation_frame = (self.animation_frame + 1) % basic_frames
                self.animation_timer = current_time

    def draw(self, interfaz, camera_x, camera_y):
        interfaz_x = self.x - camera_x
        interfaz_y = self.y - camera_y

        if self.is_chopping:
            if self.current_state in [idle_right, walk_right]:
                current_frame = self.axe_animations[3][self.chop_frame]
                if self.facing_left:
                    current_frame = pygame.transform.flip(current_frame, True, False)
            elif self.current_state in [idle_down, walk_down]:
                current_frame = self.axe_animations[4][self.chop_frame]
            elif self.current_state in [idle_up, walk_up]:
                current_frame = self.axe_animations[5][self.chop_frame]
        else:
            current_frame = self.animations[self.current_state][self.animation_frame]
            if self.facing_left:
                current_frame = pygame.transform.flip(current_frame, True, False)

        # Centrado del frame de hacha
        if self.is_chopping:
            action_scale = constantes.action_frame_size / constantes.frame_size
            size_diff = int(constantes.player * (action_scale - 1))
            interfaz.blit(current_frame, (interfaz_x - size_diff // 2, interfaz_y - size_diff // 2))
        else:
            interfaz.blit(current_frame, (interfaz_x, interfaz_y))

        self.draw_status_bars(interfaz)

    # ARREGLO: este método estaba FUERA de la clase. Lo metemos adentro y limpiamos duplicados.
    def Move(self, dx, dy, world):
        self.moving = dx != 0 or dy != 0
        if self.moving:
            speed_multiplier = run_speed if self.is_running and self.stamina > 0 else walk_Speed
            dx *= speed_multiplier / walk_Speed
            dy *= speed_multiplier / walk_Speed

            # estado/facing
            if   dy > 0: self.current_state = walk_down;  self.facing_left = False
            elif dy < 0: self.current_state = walk_up;    self.facing_left = False
            elif dx > 0: self.current_state = walk_right; self.facing_left = False
            elif dx < 0: self.current_state = walk_right; self.facing_left = True
            else:
                if self.current_state == walk_down:  self.current_state = idle_down
                if self.current_state == walk_up:    self.current_state = idle_up
                if self.current_state == walk_right: self.current_state = idle_right

        # mover en X con colisión contra árboles
        new_x = self.x + dx
        if any(self.check_collision(new_x, self.y, t) for t in world.trees):
            new_x = self.x
        self.x = new_x

        # mover en Y con colisión contra árboles
        new_y = self.y + dy
        if any(self.check_collision(self.x, new_y, t) for t in world.trees):
            new_y = self.y
        self.y = new_y

        # animación + costes
        self.update_animation()
        if self.moving:
            if self.is_running and self.stamina > 0:
                self.update_stamina(-stamina_decrease_rate)
                self.update_energy(-movement_energy_cost * 2)
            else:
                self.update_energy(-movement_energy_cost)
                self.update_stamina(stamina_increase_rate)

    # ARREGLO: también estaba anidado por error; va como método normal.
    def check_collision(self, x, y, obj):
        player_left   = x
        player_right  = x + self.size
        player_top    = y
        player_bottom = y + self.size

        obj_left   = obj.x
        obj_right  = obj.x + obj.size
        obj_top    = obj.y
        obj_bottom = obj.y + obj.size

        return not (player_right <= obj_left or
                    player_left  >= obj_right or
                    player_bottom <= obj_top or
                    player_top    >= obj_bottom)

    # ARREGLO: método normal (no dentro de Move)
    def is_near(self, obj):
        dx = self.x - obj.x
        dy = self.y - obj.y
        dist2 = dx*dx + dy*dy
        radius = (self.size // 2) + (obj.size // 2) + 8  # margen pequeño extra
        return dist2 <= (radius * radius)

    # ARREGLO: este método también estaba fuera de la clase.
    def interact(self, world):
        # Árboles: talar (con hacha más rápido; sin hacha más lento)
        for tree in world.trees:
            if self.is_near(tree):
                has_axe = self.inventory.has_axe_equipped()
                if has_axe:
                    self.is_chopping = True
                    self.chop_timer = pygame.time.get_ticks()
                    self.chop_frame = 0
                if tree.chop(with_axe=has_axe):
                    self.inventory.add_item('wood')
                return  # ya interactuamos con un árbol cercano

        # Piedras pequeñas: recoger
        for stone in world.small_stone:  # propiedad que devuelve la lista "plana"
            if self.is_near(stone):
                if stone.collect():                  # consume 1 de la piedra
                    self.inventory.add_item('stone') # suma al inventario (se apila solo)
                return

    # ------- UI/estadísticas -------
    def update_energy(self, amount): self.energy  = max(0, min(self.energy  + amount, max_energy))
    def update_food(self, amount):   self.food    = max(0, min(self.food    + amount, max_food))
    def update_thirst(self, amount): self.thirst  = max(0, min(self.thirst  + amount, max_thirst))
    def update_stamina(self, amount):self.stamina = max(0, min(self.stamina + amount, max_stamina))

    def draw_status_bars(self, screen):
        bar_width = 100
        bar_height = 10
        x_offset = 10
        y_offset = 10
        # Energía
        pygame.draw.rect(screen, bar_background, (x_offset, y_offset, bar_width, bar_height))
        pygame.draw.rect(screen, energy_color, (x_offset, y_offset, bar_width * (self.energy / max_energy), bar_height))
        # Comida
        y_offset += 15
        pygame.draw.rect(screen, bar_background, (x_offset, y_offset, bar_width, bar_height))
        pygame.draw.rect(screen, food_color, (x_offset, y_offset, bar_width * (self.food / max_food), bar_height))
        # Sed
        y_offset += 15
        pygame.draw.rect(screen, bar_background, (x_offset, y_offset, bar_width, bar_height))
        pygame.draw.rect(screen, thirst_color, (x_offset, y_offset, bar_width * (self.thirst / max_thirst), bar_height))
        # Resistencia
        y_offset += 15
        pygame.draw.rect(screen, bar_background, (x_offset, y_offset, bar_width, bar_height))
        pygame.draw.rect(screen, stamina_color, (x_offset, y_offset, bar_width * (self.stamina / max_stamina), bar_height))

    def update_status(self):
        food_rate   = food_decrease_rate   * (run_food_decrease_multiplier   if self.is_running else 1)
        thirst_rate = thirst_decrease_rate * (run_thirst_decrease_multiplier if self.is_running else 1)
        self.update_food(-food_rate)
        self.update_thirst(-thirst_rate)

        if self.food < max_food * 0.2 or self.thirst < max_thirst * 0.2:
            self.update_energy(-energy_decrease_rate)
        else:
            self.update_energy(energy_increase_rate)

        if not self.is_running:
            self.update_stamina(stamina_increase_rate)
