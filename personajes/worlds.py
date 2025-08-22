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

        # Semilla única basada en coordenadas
        chunk_seed = hash(f"{x},{y}")
        old_state = random.getstate()
        random.seed(chunk_seed)

        # Árboles
        self.trees = [
            Tree(
                self.x + random.randint(0, window_width - constantes.tree),
                self.y + random.randint(0, window_height - constantes.tree)
            ) for _ in range(5)
        ]

        # Piedras pequeñas
        self.small_stones = [
            SmallStone(
                self.x + random.randint(0, window_width - constantes.small_stone),
                self.y + random.randint(0, window_height - constantes.small_stone)
            ) for _ in range(10)
        ]

        random.setstate(old_state)

    def draw(self, interfaz, grass_image, camera_x, camera_y):
        # Pasto dentro de este chunk (optimizado)
        start_x = max(0, (camera_x - self.x - constantes.grass) // constantes.grass)
        end_x   = min(self.window_width // constantes.grass + 1,
                      (camera_x + constantes.window_width - self.x + constantes.grass) // constantes.grass + 1)
        start_y = max(0, (camera_y - self.y - constantes.grass) // constantes.grass)
        end_y   = min(self.window_height // constantes.grass + 1,
                      (camera_y + constantes.window_height - self.y + constantes.grass) // constantes.grass + 1)

        for y in range(int(start_y), int(end_y)):
            for x in range(int(start_x), int(end_x)):
                interfaz_x = self.x + x * constantes.grass - camera_x
                interfaz_y = self.y + y * constantes.grass - camera_y
                interfaz.blit(grass_image, (interfaz_x, interfaz_y))

        # Limpiar agotados
        self.trees        = [t for t in self.trees if not t.is_depleted()]
        self.small_stones = [s for s in self.small_stones if not s.is_depleted()]

        # Dibujar piedras
        for stone in self.small_stones:
            stone.draw(interfaz, camera_x, camera_y)

        # Dibujar árboles
        for tree in self.trees:
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

        # sistema de día y noche
        self.current_time = constantes.morning_time
        self.day_overlay = Surface((self.view_window_width, self.window_height))
        self.day_overlay.fill(constantes.day_color)
        self.day_overlay.set_alpha(0)

        # Cargar anillo de chunks
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

        # Generar alrededor
        for dx in [-2, -1, 0, 1, 2]:
            for dy in [-2, -1, 0, 1, 2]:
                self.generate_chunk(current_chunk[0] + dx, current_chunk[1] + dy)

        # Limpiar lejos
        to_remove = []
        for key in list(self.activate_chunks.keys()):
            if abs(key[0] - current_chunk[0]) > 2 or abs(key[1] - current_chunk[1]) > 2:
                to_remove.append(key)
        for key in to_remove:
            del self.activate_chunks[key]

    def update_time(self, dt):
        self.current_time = (self.current_time + dt) % constantes.day_length

        if constantes.morning_time <= self.current_time < constantes.dusk_time:
            self.day_overlay.fill(constantes.day_color)
            alpha = 0
        elif constantes.dawn_time <= self.current_time < constantes.morning_time:
            self.day_overlay.fill(constantes.dawn_dusk_color)
            morning_progress = (self.current_time - constantes.dawn_time) / (constantes.morning_time - constantes.dawn_time)
            alpha = int(constantes.max_darkness * (1 - morning_progress))
        else:
            self.day_overlay.fill(constantes.night_color)
            if self.current_time >= constantes.dusk_time:
                evening_progress = (self.current_time - constantes.dusk_time) / (constantes.midnight - constantes.dusk_time)
                alpha = int(constantes.max_darkness * evening_progress)
            else:
                night_progress = (self.current_time + (constantes.day_length - constantes.midnight)) / \
                                (constantes.day_length - constantes.midnight + constantes.dawn_time)
                alpha = int(constantes.max_darkness * night_progress)

        self.day_overlay.set_alpha(alpha)

    @property
    def trees(self):
        # lista “aplanada” de árboles visibles
        all_trees = []
        for chunk in self.activate_chunks.values():
            all_trees.extend(chunk.trees)
        return all_trees

    @property
    def small_stone(self):
        # OJO: nombre singular, devuelve lista (igual que en tu archivo)
        all_stones = []
        for chunk in self.activate_chunks.values():
            all_stones.extend(chunk.small_stones)
        return all_stones

    def Draw(self, interfaz, camera_x, camera_y):
        # Pasto + elementos por chunk
        for chunk in self.activate_chunks.values():
            chunk.draw(interfaz, self.grass_image, camera_x, camera_y)
        # Overlay de día/noche
        interfaz.blit(self.day_overlay, (0, 0))
