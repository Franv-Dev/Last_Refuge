import pygame
import constantes
import os

class InventoryItem:
    def __init__(self, name, image_path, quantity=1):
        self.name = name
        self.quantity = quantity
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (constantes.slot_size - 10, constantes.slot_size - 10))
        self.dragging = False
        self.drag_offset = (0, 0)

class Inventory:
    def __init__(self):
        self.hotbar = [None] * constantes.hotbar_slots
        self.inventory = [[None for _ in range(constantes.inventory_cols)] for _ in range(constantes.inventory_rows)]
        self.dragged_item = None
        self.font = pygame.font.Font(None, 24)

        # cargar imagenes de items
        self.item_images = {
            "wood": os.path.join("assets", "images", "objects", "wood.png"),
            "stone": os.path.join("assets", "images", "objects", "small_stone.png")
        }

    def add_item(self, item_name, quantity=1):
        for i, slot in enumerate(self.hotbar):
            if slot and slot.name == item_name:
                slot.quantity += quantity
                return True
        # apilar en el inventario principal
        for row in range(constantes.inventory_rows):
            for col in range(constantes.inventory_cols):
                if self.inventory[row][col] and self.inventory[row][col].name == item_name:
                    self.inventory[row][col].quantity += quantity
                    return True
        # buscar un espacio vacío en la hotbar
        for i, slot in enumerate(self.hotbar):
            if slot is None:
                self.hotbar[i] = InventoryItem(item_name, self.item_images[item_name], quantity)
                return True
        # buscar un espacio vacío en el inventario principal
        for row in range(constantes.inventory_rows):
            for col in range(constantes.inventory_cols):
                if self.inventory[row][col] is None:
                    self.inventory[row][col] = InventoryItem(item_name, self.item_images[item_name], quantity)
                    return True
        return False  # no se pudo agregar el item

    def draw(self, interfaz, show_inventory=False):
        self._draw_hotbar(interfaz)

        #dibujar inventario principal si está abierto
        if show_inventory:
            background = pygame.Surface((constantes.window_width, constantes.window_height), pygame.SRCALPHA)
            background.fill((0, 0, 0, 128))  # fondo semitransparente
            interfaz.blit(background, (0, 0))
            self._draw_main_inventory(interfaz)

        # dibujar items arrastrados
        if self.dragged_item:
            mouse_pos = pygame.mouse.get_pos()
            interfaz.blit(self.dragged_item.image, 
                          (mouse_pos[0] - self.dragged_item.drag_offset[0],
                           mouse_pos[1] - self.dragged_item.drag_offset[1]))
            if self.dragged_item.quantity > 1:
                text = self.font.render(str(self.dragged_item.quantity), True, constantes.color_white)
                text_rect = text.get_rect()
                text_rect.bottomright = (mouse_pos[0] - self.dragged_item.image.get_width() // 2 - 5,
                                         mouse_pos[1] - self.dragged_item.image.get_height() // 2 - 5)
                interfaz.blit(text, text_rect)

    def _draw_hotbar(self, interfaz):
        for i in range(constantes.hotbar_slots):
            x = constantes.hotbar_x + i * (constantes.slot_size)
            y = constantes.hotbar_y

            # dibujar fondo de la barra
            pygame.draw.rect(interfaz, constantes.slot_border,
                             (x, y, constantes.slot_size, constantes.slot_size))
            pygame.draw.rect(interfaz, constantes.slot_color,
                             (x + 2, y + 2, constantes.slot_size - 4, constantes.slot_size - 4))
            if self.hotbar[i]:
                self._draw_item(interfaz, self.hotbar[i], x, y)

    def _draw_main_inventory(self, interfaz):
        for row in range(constantes.inventory_rows):
            for col in range(constantes.inventory_cols):
                x = constantes.inventory_x + (col * constantes.slot_size)
                y = constantes.inventory_y + (row * constantes.slot_size)

                # dibujar fondo del slot
                pygame.draw.rect(interfaz, constantes.slot_border,
                                 (x, y, constantes.slot_size, constantes.slot_size))
                pygame.draw.rect(interfaz, constantes.slot_color,
                                 (x + 2, y + 2, constantes.slot_size - 4, constantes.slot_size - 4))
                if self.inventory[row][col]:
                    self._draw_item(interfaz, self.inventory[row][col], x, y)

    def _draw_item(self, interfaz, item, x, y):
        item_x = x + (constantes.slot_size - item.image.get_width()) // 2
        item_y = y + (constantes.slot_size - item.image.get_height()) // 2
        interfaz.blit(item.image, (item_x, item_y))

        if item.quantity > 1:
            text = self.font.render(str(item.quantity), True, constantes.color_white)
            text_rect = text.get_rect()
            text_rect.bottomright = (item_x + item.image.get_width() - 5, 
                                     item_y + item.image.get_height() - 5)
            interfaz.blit(text, text_rect)

    def handle_click(self, pos, button, show_inventory=False):
        mouse_x, mouse_y = pos
        if constantes.hotbar_y <= mouse_y <= constantes.hotbar_y + constantes.slot_size:
            slot_index = (mouse_x - constantes.hotbar_x) // constantes.slot_size
            if 0 <= slot_index < constantes.hotbar_slots:
                self._handle_hotbar_click(button, self.hotbar, slot_index,
                                          constantes.hotbar_x + (slot_index * constantes.slot_size),
                                          constantes.hotbar_y)
                return True
        if show_inventory and constantes.inventory_y <= mouse_y <= constantes.inventory_y + (constantes.inventory_rows * constantes.slot_size):
            row = (mouse_y - constantes.inventory_y) // constantes.slot_size
            col = (mouse_x - constantes.inventory_x) // constantes.slot_size
            if (0 <= row < constantes.inventory_rows and
                0 <= col < constantes.inventory_cols):
                self._handle_inventory_click(button, row, col, 
                                            constantes.inventory_x + (col * constantes.slot_size),
                                            constantes.inventory_y + (row * constantes.slot_size))
                return True
            
            if self.dragged_item and button == 1:
                self._return_dragged_item()
            return False

    def _handle_hotbar_click(self, button, hotbar, slot_index, slot_x, slot_y):
        mouse_pos = pygame.mouse.get_pos()
        mouse_x, mouse_y = mouse_pos
        if button == 1:  # click izquierdo
            if self.dragged_item:
                if hotbar[slot_index] is None:
                    hotbar[slot_index] = self.dragged_item
                    self.dragged_item = None
                else:
                    hotbar[slot_index], self.dragged_item = self.dragged_item, hotbar[slot_index]
            elif hotbar[slot_index]:
                self.dragged_item = hotbar[slot_index]
                hotbar[slot_index] = None
                item_rect = self.dragged_item.image.get_rect()
                item_rect.x = slot_x 
                item_rect.y = slot_y
                self.dragged_item.drag_offset = (mouse_x - item_rect.centerx, mouse_y - item_rect.centery)

    def _handle_inventory_click(self, button, row, col, slot_x, slot_y):
        mouse_pos = pygame.mouse.get_pos()
        mouse_x, mouse_y = mouse_pos
        if button == 1:
            if self.dragged_item:
                if self.inventory[row][col] is None:
                    self.inventory[row][col] = self.dragged_item
                    self.dragged_item = None
                else:
                    self.inventory[row][col], self.dragged_item = self.dragged_item, self.inventory[row][col]
            elif self.inventory[row][col]:
                self.dragged_item = self.inventory[row][col]
                self.inventory[row][col] = None
                item_rect = self.dragged_item.image.get_rect()
                item_rect.x = slot_x
                item_rect.y = slot_y
                self.dragged_item.drag_offset = (mouse_x - item_rect.centerx, mouse_y - item_rect.centery)

    def _return_dragged_item(self):
        for i, slot in enumerate(self.hotbar):
            if slot is None:
                self.hotbar[i] = self.dragged_item
                self.dragged_item = None
                return
        for row in range(constantes.inventory_rows):
            for col in range(constantes.inventory_cols):
                if self.inventory[row][col] is None:
                    self.inventory[row][col] = self.dragged_item
                    self.dragged_item = None
                    return