import os
import pygame
from constantes import *

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 20
        self.inventory = {"wood": 0, "stone": 0}

        # Cargar hoja de sprites
        image_path = os.path.join('assets', 'images', 'player', 'player1.png')
        self.sprite_sheet = pygame.image.load(image_path).convert_alpha()

        # Propiedades de animación
        self.frame_size = frame_size
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_delay = animation_delay
        self.current_state = idle_down  # ← Inicialización correcta
        self.moving = False
        self.facing_left = False

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

    def load_animations(self):
        animations = {}
        for state in range(6):  # 6 estados de animación
            frames = []
            for frame in range(basic_frames):
                rect = pygame.Rect(frame * self.frame_size, state * self.frame_size, self.frame_size, self.frame_size)
                image = self.sprite_sheet.subsurface(rect)
                frames.append(image)
            animations[state] = frames
        return animations

    def update_animation(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.animation_timer > self.animation_delay:
            self.animation_frame = (self.animation_frame + 1) % basic_frames
            self.animation_timer = current_time

    def load_item_image(self, filename):
        path = os.path.join("assets", "images", "objects", filename)
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(image, (40, 40))

    def draw(self, window):
        current_frame = self.animations[self.current_state][self.animation_frame]
        if self.facing_left:
            current_frame = pygame.transform.flip(current_frame, True, False)
        window.blit(current_frame, (self.x, self.y))
        self.draw_status_bars(window)

    def Draw(self, interfaz):
        return self.draw(interfaz)

    def Move(self, dx, dy, world):
        self.moving = dx != 0 or dy != 0
        if dy > 0:
            self.current_state = walk_down
        elif dy < 0:
            self.current_state = walk_up
        elif dx > 0:
            self.current_state = walk_right
            self.facing_left = False
        elif dx < 0:
            self.current_state = walk_right
            self.facing_left = True
        else:
            self.current_state = idle_down

        new_x = self.x + dx
        new_y = self.y + dy

        # Colisión con árboles
        for tree in world.trees:
            if self.check_collision(new_x, new_y, tree):
                return  # No se mueve si hay colisión

        # Mantener dentro de la pantalla
        self.x = max(0, min(new_x, window_width - self.size))
        self.y = max(0, min(new_y, window_height - self.size))

        self.update_animation()
        self.update_energy(-0.1)       
    def update_time(self, dt):
        alpha = min(180, calculo_de_alpha)  # nunca más de 180
        
    def check_collision(self, x, y, obj):
        return (x < obj.x + obj.size * 0.75 and x + self.size * 0.75 > obj.x and
                y < obj.y + obj.size and y + self.size * 0.75 > obj.y)

    def is_near(self, obj):
        return (abs(self.x - obj.x) <= self.size + 5 and
                abs(self.y - obj.y) <= self.size + 5)

    def interact(self, world):
        for tree in world.trees:
            if self.is_near(tree):
                if not hasattr(tree, "hits"):
                    tree.hits = 0
                tree.hits += 1
                if tree.hits >= 5:
                    self.inventory["wood"] += 5
                    world.trees.remove(tree)
                break
        for stone in world.small_stone:
            if self.is_near(stone):
                self.inventory["stone"] += 1
                world.small_stone.remove(stone)
                break

    def draw_inventory(self, interfaz):
        background = pygame.Surface((window_width, window_height), pygame.SRCALPHA)
        background.fill(color_transp)
        interfaz.blit(background, (0, 0))

        font = pygame.font.Font(None, 36)
        title = font.render("Inventory", True, color_white)
        interfaz.blit(title, (window_width // 2 - title.get_width() // 2, 20))

        item_font = pygame.font.Font(None, 24)
        y_offset = 80
        for item, quantity in self.inventory.items():
            item_img = self.item_images[item]
            interfaz.blit(item_img, (window_width // 2 - 60, y_offset))
            text = item_font.render(f"{item}: {quantity}", True, color_white)
            interfaz.blit(text, (window_width // 2, y_offset + 10))
            y_offset += 60

        close_text = item_font.render("Press 'I' to close inventory", True, color_white)
        interfaz.blit(close_text, (window_width // 2 - close_text.get_width() // 2, window_height - 40))

    def update_energy(self, amount):
        self.energy = max(0, min(self.energy + amount, max_energy))

    def update_food(self, amount):
        self.food = max(0, min(self.food + amount, max_food))

    def update_thirst(self, amount):
        self.thirst = max(0, min(self.thirst + amount, max_thirst))

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

    def update_status(self):
        self.update_food(-0.2)
        self.update_thirst(-0.2)
        if self.food < max_food * 0.2 or self.thirst < max_thirst * 0.2:
            self.update_energy(-0.5)