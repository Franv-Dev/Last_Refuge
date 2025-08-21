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
        self.left_hand = None
        self.right_hand = None
        self.hotbar = [None] * constantes.hotbar_slots
        self.inventory = [[None for _ in range(constantes.inventory_cols)] for _ in range(constantes.inventory_rows)]
        self.crafting_grid = [[None for _ in range(constantes.crafting_grid_size)] for _ in range(constantes.crafting_grid_size)]
        self.crafting_result = None
        self.dragged_item = None
        self.font = pygame.font.Font(None, 24)

        # cargar imagenes de items
        self.item_images = {
            "wood": os.path.join("assets", "images", "objects", "wood.png"),
            "stone": os.path.join("assets", "images", "objects", "small_stone.png"),
            "axe": os.path.join("assets", "images", "objects", "axe.png")
        }

        #definir recetas
        # ARREGLO: usar self.recipes (el código más abajo lo usa así)
        self.recipes = {  # ← antes estaba "recipies"
            'axe': {
                'pattern': [('wood', 'stone'), (None, None)],
                'result': 'axe'
            }
        }

    def add_item(self, item_name, quantity=1):
        # apilar en hotbar
        for i, slot in enumerate(self.hotbar):
            if slot and slot.name == item_name:
                slot.quantity += quantity
                return True
        # apilar en inventario principal
        for row in range(constantes.inventory_rows):
            for col in range(constantes.inventory_cols):
                if self.inventory[row][col] and self.inventory[row][col].name == item_name:
                    self.inventory[row][col].quantity += quantity
                    return True
        # buscar primer espacio libre en hotbar
        for i, slot in enumerate(self.hotbar):
            if slot is None:
                self.hotbar[i] = InventoryItem(item_name, self.item_images[item_name], quantity)
                return True
        # buscar primer espacio libre en inventario
        for row in range(constantes.inventory_rows):
            for col in range(constantes.inventory_cols):
                if self.inventory[row][col] is None:
                    self.inventory[row][col] = InventoryItem(item_name, self.item_images[item_name], quantity)
                    return True
        return False  # no se pudo agregar el item

    def draw(self, interfaz, show_inventory=False):
        #dibujar slot de manos (siempre visible)
        self._draw_hand_slots(interfaz)
        #dibujar hotbar(siempre visible)
        self._draw_hotbar(interfaz)
        

        #dibujar inventario principal si está abierto
        if show_inventory:
            background = pygame.Surface((constantes.window_width, constantes.window_height), pygame.SRCALPHA)
            background.fill((0, 0, 0, 128))  # fondo semitransparente
            interfaz.blit(background, (0, 0))

            self._draw_main_inventory(interfaz)
            self._draw_crafting_grid(interfaz)

        # dibujar item arrastrado
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
    def _draw_hand_slots(self, interfaz):
        # dibujar slot de mano izquierda
        pygame.draw.rect(
            interfaz, constantes.slot_border,
            (constantes.left_hand_slot_x, constantes.left_hand_slot_y,
            constantes.slot_size, constantes.slot_size)
        )
        pygame.draw.rect(
            interfaz, constantes.slot_color,
            (constantes.left_hand_slot_x + 2, constantes.left_hand_slot_y + 2,
            constantes.slot_size - 4, constantes.slot_size - 4)
        )
        if self.left_hand:
            self._draw_item(interfaz, self.left_hand,
                            constantes.left_hand_slot_x,
                            constantes.left_hand_slot_y)

        # dibujar slot de mano derecha
        pygame.draw.rect(
            interfaz, constantes.slot_border,
            (constantes.right_hand_slot_x, constantes.right_hand_slot_y,
            constantes.slot_size, constantes.slot_size)
        )
        pygame.draw.rect(
            interfaz, constantes.slot_color,
            (constantes.right_hand_slot_x + 2, constantes.right_hand_slot_y + 2,
            constantes.slot_size - 4, constantes.slot_size - 4)
        )
        if self.right_hand:
            self._draw_item(interfaz, self.right_hand,
                            constantes.right_hand_slot_x,
                            constantes.right_hand_slot_y)
            
            
    def handle_click(self, pos, button, show_inventory=False):
        mouse_x, mouse_y = pos
        #verificar slot de las manos
        if constantes.hotbar_y <=mouse_y <= constantes.hotbar_y + constantes.slot_size:
            #slot mano izquierda
            if(constantes.left_hand_slot_x <= mouse_x <=
                constantes.left_hand_slot_x + constantes.slot_size):
                self._handle_hand_slot_click(button, 'left')
                return True
            #slot mano derecha
            elif(constantes.right_hand_slot_x <= mouse_x <=
                    constantes.right_hand_slot_x + constantes.slot_size):
                self._handle_hand_slot_click(button, 'right')
                return True
        # hotbar
        if constantes.hotbar_y <= mouse_y <= constantes.hotbar_y + constantes.slot_size:
            slot_index = (mouse_x - constantes.hotbar_x) // constantes.slot_size
            if 0 <= slot_index < constantes.hotbar_slots:
                self._handle_hotbar_click(button, self.hotbar, slot_index,
                                          constantes.hotbar_x + (slot_index * constantes.slot_size),
                                            constantes.hotbar_y)
                return True

        if show_inventory:
            # inventario principal
            if constantes.inventory_y <= mouse_y <= constantes.inventory_y + (constantes.inventory_rows * constantes.slot_size):
                row = (mouse_y - constantes.inventory_y) // constantes.slot_size
                col = (mouse_x - constantes.inventory_x) // constantes.slot_size
                if (0 <= row < constantes.inventory_rows and 0 <= col < constantes.inventory_cols):
                    self._handle_inventory_click(button, row, col,
                                                 constantes.inventory_x + (col * constantes.slot_size),
                                                 constantes.inventory_y + (row * constantes.slot_size))
                    return True

            # cuadricula de crafteo
            if constantes.crafting_grid_y <= mouse_y <= constantes.crafting_grid_y + (constantes.crafting_grid_size * constantes.slot_size):
                row = (mouse_y - constantes.crafting_grid_y) // constantes.slot_size
                col = (mouse_x - constantes.crafting_grid_x) // constantes.slot_size
                if (0 <= row < constantes.crafting_grid_size and 0 <= col < constantes.crafting_grid_size):
                    self._handle_crafting_grid_click(button, row, col)
                    return True

            # resultado crafteo
            if (constantes.crafting_result_slot_x <= mouse_x <= constantes.crafting_result_slot_x + constantes.slot_size and
                constantes.crafting_result_slot_y <= mouse_y <= constantes.crafting_result_slot_y + constantes.slot_size):
                self._handle_crafting_result_click(button)
                return True

        # click fuera de los slots
        if self.dragged_item and button == 1:
            self._return_dragged_item()
        return False

    def _handle_hotbar_click(self, button, hotbar, slot_index, slot_x, slot_y):
        mouse_x, mouse_y = pygame.mouse.get_pos()
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
        mouse_x, mouse_y = pygame.mouse.get_pos()
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
    def _handle_hand_slot_click(self, button, hand):
        if button == 1:  # click izquierdo
            if hand == 'left':
                if self.dragged_item:
                    if self.dragged_item.name == 'axe':
                        self.left_hand, self.dragged_item = self.dragged_item, self.left_hand
            elif self.left_hand:
                self.dragged_item = self.left_hand
                self.left_hand = None
        else:   # click derecho
            if self.dragged_item:
                if self.dragged_item.name == 'axe':
                    self.right_hand, self.dragged_item = self.dragged_item, self.right_hand
            elif self.right_hand:
                self.dragged_item = self.right_hand
                self.right_hand = None

    def has_axe_equipped(self):
        return( (self.left_hand and self.left_hand.name == 'axe') or 
                    (self.right_hand and self.right_hand.name == 'axe')
        )

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

    def _draw_crafting_grid(self, interfaz):  # revisar esta linea si es interfaz o windows
        #dibujar cuadricula de crafteo 
        for row in range(constantes.crafting_grid_size):
            for col in range(constantes.crafting_grid_size):
                x = constantes.crafting_grid_x + (col * constantes.slot_size)
                y = constantes.crafting_grid_y + (row * constantes.slot_size)
                #dibujar fondo del slot
                # ARREGLO: pygame.draw.rect requiere un rectángulo como TUPLA (x, y, w, h)
                pygame.draw.rect(interfaz, constantes.slot_border,
                                 (x, y, constantes.slot_size, constantes.slot_size))
                pygame.draw.rect(interfaz, constantes.slot_color,
                                 (x + 2, y + 2, constantes.slot_size - 4, constantes.slot_size - 4))
                #dibujar item si existe
                if self.crafting_grid[row][col]:
                    self._draw_item(interfaz, self.crafting_grid[row][col], x, y)

        #dibujar slot de resultado
        pygame.draw.rect(interfaz, constantes.slot_border,
                         (constantes.crafting_result_slot_x, constantes.crafting_result_slot_y, constantes.slot_size, constantes.slot_size))
        pygame.draw.rect(interfaz, constantes.slot_color,
                         (constantes.crafting_result_slot_x + 2, constantes.crafting_result_slot_y + 2, constantes.slot_size - 4, constantes.slot_size - 4))
        #dibujar resultado si existe
        if self.crafting_result:
            self._draw_item(interfaz, self.crafting_result, constantes.crafting_result_slot_x, constantes.crafting_result_slot_y)

    def _handle_crafting_grid_click(self, button, row, col):
        if button == 1:  # CLICK izquierdo
            if self.dragged_item:
                #soltar item en la cuadricula
                if self.crafting_grid[row][col] is None:
                    self.crafting_grid[row][col] = self.dragged_item
                    self.dragged_item = None
                else:
                    #intercambiar items
                    self.crafting_grid[row][col], self.dragged_item = self.dragged_item, self.crafting_grid[row][col]
            elif self.crafting_grid[row][col]:
                #comenzar a arrastrar 
                self.dragged_item = self.crafting_grid[row][col]
                self.crafting_grid[row][col] = None
            #verificar receta despues de cada cambio
            self._check_recipe()

    def _handle_crafting_result_click(self, button):
        if button == 1 and self.crafting_result:  # click izquierdo y hay resultado
            if not self.dragged_item:
                #tomar resultado
                self.dragged_item = self.crafting_result
                self.crafting_result = None
                #consumir items
                for row in range(constantes.crafting_grid_size):
                    for col in range(constantes.crafting_grid_size):
                        if self.crafting_grid[row][col]:
                            if self.crafting_grid[row][col].quantity > 1:
                                self.crafting_grid[row][col].quantity -= 1
                            else:
                                self.crafting_grid[row][col] = None
                # ARREGLO: re-evaluar la receta tras consumir insumos
                self._check_recipe()

    def _check_recipe(self):
        #obtener el patron actual
        current_pattern = []
        for row in range(constantes.crafting_grid_size):
            pattern_row = []
            for col in range(constantes.crafting_grid_size):
                item = self.crafting_grid[row][col]
                pattern_row.append(item.name if item else None)
            current_pattern.append(tuple(pattern_row))

        #verificar si coincide alguna receta
        # ARREGLO: asegurar que iteramos sobre self.recipes
        for recipe_name, recipe in self.recipes.items():
            matches = True
            for row in range(constantes.crafting_grid_size):
                for col in range(constantes.crafting_grid_size):
                    expected = recipe['pattern'][row][col]
                    actual = current_pattern[row][col]
                    if expected != actual:
                        matches = False
                        break
                if not matches:
                    break
            if matches:
                self.crafting_result = InventoryItem(recipe['result'],
                                                     self.item_images[recipe['result']])
                return

        #si no hay coincidencia, limpiar el resultado
        self.crafting_result = None

