# Tamaño del personaje principal
windows_width_player, height_player = 50, 50

# Tamaño de la pantalla principal
window_width, window_height = 1280, 720

# Tamaño objetos del mapa
player = 100
grass = 64      # césped
tree = 70       # árboles
small_stone = 20  # piedras pequeñas

# Animaciones
basic_frames = 6
idle_down  = 0
idle_right = 1
idle_up    = 2
walk_down  = 3
walk_right = 4
walk_up    = 5
frame_size = 32
action_frame_size = 48  # ARREGLO: tamaño de frame para sprites de ACCIÓN (hacha) 
animation_delay = 100
running_animation_delay = 50
fps = 60

# Colores
color_blue   = (0, 0, 255)
color_green  = (0, 255, 0)
color_red    = (255, 0, 0)
color_black  = (0, 0, 0)
color_white  = (255, 255, 255)
color_orange = (255, 128, 0)
color_brown  = (139, 69, 19)
color_transp = (0, 0, 0, 128)

# Barras de estado
max_energy = 100
max_food   = 100
max_thirst = 100
max_stamina = 100

# Colores barras
energy_color  = (255, 215, 0)   # amarillo
food_color    = (255, 165, 0)   # naranja
thirst_color  = (0, 191, 255)   # azul claro
stamina_color = (34, 139, 34)   # verde
bar_background = (100, 100, 100)  # gris oscuro

# Velocidad
speed = 2

# Intervalo de actualización de estados
status_update_interval = 1000  # ms

# Sistema día/noche
day_length   = 72000
dawn_time    = 18000
morning_time = 24000
dusk_time    = 54000
midnight     = 72000
max_darkness = 210

# Colores para iluminación
night_color     = (20, 20, 50)
day_color       = (255, 255, 225)
dawn_dusk_color = (255, 193, 137)

# Velocidades de disminución de estados
food_decrease_rate   = 0.01
thirst_decrease_rate = 0.02
energy_decrease_rate = 0.005
energy_increase_rate = 0.001
movement_energy_cost = 0.001

# Constantes correr
walk_Speed = 5
run_speed = 8
stamina_decrease_rate = 0.05
stamina_increase_rate = 0.02
run_food_decrease_multiplier   = 2.0
run_thirst_decrease_multiplier = 2.0

# Inventario
slot_size = 64
hotbar_slots = 8
inventory_rows = 4
inventory_cols = 5
margin = 10

# Hotbar (centrada abajo)
hotbar_x = (window_width - (slot_size * hotbar_slots)) // 2
hotbar_y = window_height - slot_size - margin

# Inventario principal (centrado)
inventory_x = (window_width - (slot_size * inventory_cols)) // 2
inventory_y = (window_height - (slot_size * inventory_rows)) // 2

# Crafting
crafting_grid_size = 2
crafting_result_slot_x = inventory_x + (slot_size * (inventory_cols + 1))
crafting_result_slot_y = inventory_y
crafting_grid_x = inventory_x + (slot_size * (inventory_cols + 1))
crafting_grid_y = inventory_y + slot_size + 2

# Hand slots (izq / der)
left_hand_slot_x  = hotbar_x - slot_size - margin   # ARREGLO: constantes de slots de mano 
left_hand_slot_y  = hotbar_y
right_hand_slot_x = hotbar_x + (slot_size * hotbar_slots) + margin
right_hand_slot_y = hotbar_y

# Animación del hacha
axe_cols = 2                  # ARREGLO: añadidos para animación hacha 
axe_frames = 2
axe_animation_delay = 200

# Colores inventario
slot_color  = (139, 139, 139)
slot_border = (100, 100, 100)
slot_hover  = (160, 160, 160)
