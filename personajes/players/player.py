import os
import pygame
from constantes import *
from inventario.inventory import Inventory

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 20
        self.inventory = Inventory()

        # Cargar hoja de sprites
        image_path = os.path.join('assets', 'images', 'player', 'player1.png')
        self.sprite_sheet = pygame.image.load(image_path).convert_alpha()

        # Propiedades de animación
        self.frame_size = frame_size
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_delay = animation_delay
        self.current_state = idle_down
        self.moving = False
        self.facing_left = False
        self.is_running = False

        # Cargar animaciones
        self.animations = self.load_animations()
        self.item_images = {
            "wood": self.load_item_image("wood.png"),
            "stone": self.load_item_image("small_stone.png")
        }

        # Barras de estado
        self.energy = max_energy
        self.food = max_food
        self.thirst = max_thirst
        self.stamina = max_stamina

    def load_animations(self):
        animations = {}
        for state in range(6):
            frames = []
            for frame in range(basic_frames):
                rect = pygame.Rect(frame * self.frame_size, state * self.frame_size, self.frame_size, self.frame_size)
                image = self.sprite_sheet.subsurface(rect)
                frames.append(image)
            animations[state] = frames
        return animations

    def update_animation(self):
        current_time = pygame.time.get_ticks()
        animation_speed = running_animation_delay if self.is_running else animation_delay
        if current_time - self.animation_timer > animation_speed:
            self.animation_frame = (self.animation_frame + 1) % basic_frames
            self.animation_timer = current_time

    def load_item_image(self, filename):
        path = os.path.join("assets", "images", "objects", filename)
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(image, (40, 40))

    def draw(self, interfaz, camera_x, camera_y):
        interfaz_x = self.x - camera_x
        interfaz_y = self.y - camera_y

        current_frame = self.animations[self.current_state][self.animation_frame]
        if self.facing_left:
            current_frame = pygame.transform.flip(current_frame, flip_x=True, flip_y=False)
        interfaz.blit(current_frame, (interfaz_x, interfaz_y))

    def Move(self, dx, dy, world):
        self.moving = dx != 0 or dy != 0
        if self.moving:
            speed_multiplier = run_speed if self.is_running and self.stamina > 0 else walk_Speed
            dx *= speed_multiplier / walk_Speed
            dy *= speed_multiplier / walk_Speed
            if dy > 0:
                self.current_state = walk_down
                self.facing_left = False
            elif dy < 0:
                self.current_state = walk_up
                self.facing_left = False
            elif dx > 0:
                self.current_state = walk_right
                self.facing_left = False
            elif dx < 0:
                self.current_state = walk_right
                self.facing_left = True
            else:
                if self.current_state == walk_down:
                    self.current_state = idle_down
                elif self.current_state == walk_up:
                    self.current_state = idle_up
                elif self.current_state == walk_right:
                    self.current_state = idle_right

        new_x = self.x + dx
        new_y = self.y + dy

        # Colisión con árboles
        for tree in world.trees:
            if self.check_collision(new_x, new_y, tree):
                self.moving = False
                return
        self.x = new_x
        self.y = new_y

        self.update_animation()

        if self.moving:
            if self.is_running and self.stamina > 0:
                self.update_stamina(-stamina_decrease_rate)
                self.update_energy(-movement_energy_cost * 2)
            else:
                self.update_energy(-movement_energy_cost)
                self.update_stamina(stamina_increase_rate)

    def check_collision(self, x, y, obj):
        return (x < obj.x + obj.size * 0.75 and x + self.size * 0.75 > obj.x and
                y < obj.y + obj.size and y + self.size * 0.75 > obj.y)

    def is_near(self, obj):
        return (abs(self.x - obj.x) <= self.size + 5 and
                abs(self.y - obj.y) <= self.size + 5)

    def interact(self, world):
        # Talar árbol
        for chunk in world.activate_chunks.values():
            for tree in chunk.trees:
                if self.is_near(tree):
                    if tree.chop():
                        self.inventory.add_item("wood")
                    return

        # Recolectar piedra
        for chunk in world.activate_chunks.values():
            for stone in chunk.small_stones:
                if self.is_near(stone):
                    if stone.collect():
                        self.inventory.add_item("stone")
                    return

    def draw_hotbar(self, interfaz):
        # Dibuja la hotbar (inventario inferior) siempre
        hotbar_x = (window_width - (slot_size * hotbar_slots)) // 2
        hotbar_y = window_height - slot_size - margin
        for i in range(hotbar_slots):
            slot_x = hotbar_x + i * slot_size
            pygame.draw.rect(interfaz, slot_border, (slot_x, hotbar_y, slot_size, slot_size))
            pygame.draw.rect(interfaz, slot_color, (slot_x + 2, hotbar_y + 2, slot_size - 4, slot_size - 4))
            item = self.inventory.hotbar[i]
            if item:
                interfaz.blit(item.image, (slot_x + (slot_size - item.image.get_width()) // 2,
                                           hotbar_y + (slot_size - item.image.get_height()) // 2))
                if item.quantity > 1:
                    font = pygame.font.Font(None, 24)
                    text = font.render(str(item.quantity), True, color_white)
                    text_rect = text.get_rect()
                    text_rect.bottomright = (slot_x + slot_size - 8, hotbar_y + slot_size - 8)
                    interfaz.blit(text, text_rect)

    def draw_inventory(self, interfaz, show_inventory=False):
        if not show_inventory:
            return
        # Tamaño del inventario
        inv_width = slot_size * inventory_cols + 20
        inv_height = slot_size * inventory_rows + 40
        x = (window_width - inv_width) // 2
        y = (window_height - inv_height) // 2  # CENTRADO EN PANTALLA

        # Fondo del inventario
        background = pygame.Surface((inv_width, inv_height), pygame.SRCALPHA)
        background.fill((30, 30, 30, 220))
        interfaz.blit(background, (x, y))

        # Dibuja los slots e items del inventario principal
        for row in range(inventory_rows):
            for col in range(inventory_cols):
                slot_x = x + 10 + col * slot_size
                slot_y = y + 30 + row * slot_size
                pygame.draw.rect(interfaz, slot_border, (slot_x, slot_y, slot_size, slot_size))
                pygame.draw.rect(interfaz, slot_color, (slot_x + 2, slot_y + 2, slot_size - 4, slot_size - 4))
                item = self.inventory.inventory[row][col]
                if item:
                    interfaz.blit(item.image, (slot_x + (slot_size - item.image.get_width()) // 2,
                                               slot_y + (slot_size - item.image.get_height()) // 2))
                    if item.quantity > 1:
                        font = pygame.font.Font(None, 24)
                        text = font.render(str(item.quantity), True, color_white)
                        text_rect = text.get_rect()
                        text_rect.bottomright = (slot_x + slot_size - 8, slot_y + slot_size - 8)
                        interfaz.blit(text, text_rect)

        # Texto para cerrar inventario
        font = pygame.font.Font(None, 24)
        close_text = font.render("Presiona 'I' para cerrar inventario", True, color_white)
        interfaz.blit(close_text, (x + (inv_width - close_text.get_width()) // 2, y + 5))

    def update_energy(self, amount):
        self.energy = max(0, min(self.energy + amount, max_energy))

    def update_food(self, amount):
        self.food = max(0, min(self.food + amount, max_food))

    def update_thirst(self, amount):
        self.thirst = max(0, min(self.thirst + amount, max_thirst))

    def update_stamina(self, amount):
        self.stamina = max(0, min(self.stamina + amount, max_stamina))

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
        food_rate = food_decrease_rate * (run_food_decrease_multiplier if self.is_running else 1)
        thirst_rate = thirst_decrease_rate * (run_thirst_decrease_multiplier if self.is_running else 1)
        self.update_food(-food_rate)
        self.update_thirst(-thirst_rate)

        if self.food < max_food * 0.2 or self.thirst < max_thirst * 0.2:
            self.update_energy(-energy_decrease_rate)
        else:
            self.update_energy(energy_increase_rate)

        if not self.is_running:
            self.update_stamina(stamina_increase_rate)