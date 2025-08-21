import pygame
import constantes
from personajes.elements.trees import Tree, SmallStone
import random
import os
from pygame import Surface

class WorldChunk:
    # Segmento del mundo con sus propios elementos
    def __init__(self, x, y, window_width, window_height):
        self.x = x
        self.y = y
        self.window_width = window_width
        self.window_height = window_height

        # Semilla unica basada en coordenadas
        chunk_seed = hash(f"{x},{y}")
        # Guardar estado actual
        old_state = random.getstate()
        random.seed(chunk_seed)
        # Generar elementos
        self.trees = [
            Tree(
                self.x + random.randint(0, window_width-constantes.tree),
                self.y + random.randint(0, window_height-constantes.tree)
            ) for _ in range(5)
        ]

        self.small_stones = [
            SmallStone(
                self.x + random.randint(0, window_width-constantes.small_stone),
                self.y + random.randint(0, window_height-constantes.small_stone)
            ) for _ in range(10)
        ]
        # Restaurar estado
        random.setstate(old_state)

    def draw(self, interfaz, grass_image, camera_x, camera_y):
        chunk_interfaz_x = self.x - camera_x
        chunk_interfaz_y = self.y - camera_y
        start_x = max(0, (camera_x - self.x - constantes.grass) // constantes.grass)
        end_x = min(self.window_width // constantes.grass + 1,
                   (camera_x + constantes.window_width - self.x + constantes.grass) // constantes.grass + 1)
        start_y = max(0, (camera_y - self.y - constantes.grass) // constantes.grass)
        end_y = min(self.window_height // constantes.grass + 1,
                   (camera_y + constantes.window_height - self.y + constantes.grass) // constantes.grass + 1)

        for y in range(int(start_y),  int(end_y)):
            for x in range(int(start_x), int(end_x)):
                interfaz_x = self.x + x * constantes.grass - camera_x
                interfaz_y = self.y + y * constantes.grass - camera_y
                interfaz.blit(grass_image, (interfaz_x, interfaz_y))

        self.trees = [tree for tree in self.trees if not tree.is_depleted()]
        self.small_stones = [stone for stone in self.small_stones if not stone.is_depleted()]


        for stone in self.small_stones:
            stone_interfaz_x = stone.x - camera_x
            stone_interfaz_y = stone.y - camera_y
            if (stone_interfaz_x + stone.size >= 0 and stone_interfaz_x <= constantes.window_width and
                stone_interfaz_y + stone.size >= 0 and stone_interfaz_y <= constantes.window_height):
                stone.draw(interfaz, camera_x, camera_y)
        
        for tree in self.trees:
            tree_interfaz_x = tree.x - camera_x
            tree_interfaz_y = tree.y - camera_y
            if (tree_interfaz_x + tree.size >= 0 and tree_interfaz_x <= constantes.window_width and
                tree_interfaz_y + tree.size >= 0 and tree_interfaz_y <= constantes.window_height):
                tree.draw(interfaz, camera_x, camera_y)

class World:

    def __init__(self, window_width, window_height):
        self.chunk_size = constantes.window_width
        self.activate_chunks = {}
        self.view_window_width = window_width
        self.window_height = window_height

        imagen_path = "assets//images//objects//grass.png"
        self.grass_image = pygame.image.load(imagen_path)
        self.grass_image = pygame.transform.scale(self.grass_image, (constantes.grass, constantes.grass))
        # sistema de dia y noche
        self.current_time = constantes.morning_time  # comienza a las 8:00
        self.day_overlay = Surface((self.view_window_width, self.window_height))  # establecer transparencia
        self.day_overlay.fill(constantes.day_color)  # color de dia
        self.day_overlay.set_alpha(0)  # opacidad
        
        self.generate_chunk(0, 0)
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                self.generate_chunk(dx, dy)

    def get_chunk_key(self, x, y):
        chunk_x = x // self.chunk_size
        chunk_y = y // self.chunk_size
        return (chunk_x, chunk_y)

    def generate_chunk(self, chunk_x, chunk_y):
        key = (chunk_x, chunk_y)
        if key not in self.activate_chunks:
            x = chunk_x * self.chunk_size
            y = chunk_y * self.chunk_size
            self.activate_chunks[key] = WorldChunk(x, y, self.chunk_size, self.chunk_size)

    def update_chunk(self, player_x, player_y):
        current_chunk = self.get_chunk_key(player_x, player_y)

        for dx in [-2, -1, 0, 1, 2]:
            for dy in [-2, -1, 0, 1, 2]:
                chunk_x = current_chunk[0] + dx
                chunk_y = current_chunk[1] + dy
                self.generate_chunk(chunk_x, chunk_y)
    
        chunks_to_remove = []
        for chunk_key in list(self.activate_chunks.keys()):
            distance_x = abs(chunk_key[0] - current_chunk[0])
            distance_y = abs(chunk_key[1] - current_chunk[1])
            if distance_x > 2 or distance_y > 2:
                chunks_to_remove.append(chunk_key)
        for chunk_key in chunks_to_remove:
            del self.activate_chunks[chunk_key]

    def update_time(self, dt):
        self.current_time = (self.current_time + dt) % constantes.day_length
        # color y la intensidad basdos en la hora del dia
        if constantes.morning_time <= self.current_time < constantes.dusk_time:
            # durante el dia (8:00-18:00)
            self.day_overlay.fill(constantes.day_color)
            alpha = 0
        elif constantes.dawn_time <= self.current_time < constantes.morning_time:
            # durante el amanecer (6:00-8:00)
            self.day_overlay.fill(constantes.dawn_dusk_color)
            morning_progress = (self.current_time - constantes.dawn_time) / (
                        constantes.morning_time - constantes.dawn_time)
            alpha = int(constantes.max_darkness * (1 - morning_progress))
        else: 
            # entre 00: y 06:00 noche
            self.day_overlay.fill(constantes.night_color)
            alpha = 255  # Valor por defecto
        # Calcula alpha según la hora
        alpha = min(180, alpha)  # nunca más de 180
        self.day_overlay.set_alpha(alpha)

    def Draw(self, interfaz, camera_x, camera_y):
        for chunk in self.activate_chunks.values():
            chunk.draw(interfaz, self.grass_image, camera_x, camera_y)
        interfaz.blit(self.day_overlay, (0, 0))  # aplicar efecto de dia/noche

    def draw_inventory(self, interfaz, player):
        font = pygame.font.Font(None, 24)
        instruction_text = font.render("Press 'I' to open inventory",
                                    True, constantes.color_white)
        interfaz.blit(instruction_text, (10, 10))

    @property
    def trees(self):
        all_trees = []
        for chunk in self.activate_chunks.values():
            all_trees.extend(chunk.trees)
        return all_trees

    @property
    def small_stone(self):
        all_stones = []
        for chunk in self.activate_chunks.values():
            all_stones.extend(chunk.small_stones)
        return all_stones