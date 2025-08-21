windows_width_player,height_player = 50,50 # personaje principal

window_width,window_height= 1280, 720 # pantalla principal



#tamaño objetos del mapa
player = 100
grass = 64 # cesped
tree = 70 # arboles
small_stone = 20 # piedras pequeñas

# animaciones
basic_frames= 6

idle_down  = 0
idle_right = 1
idle_up    = 2
walk_down  = 3
walk_right = 4
walk_up    = 5
frame_size = 32
animation_delay= 100
running_animation_delay = 50
#----
fps = 60

#colores
color_blue = (0,0,255)
color_green = (0,255,0)
color_red =(255,0,0)
color_black = (0,0,0)
color_white = (255,255,255)
color_orange = (255,128,0)
color_brown = (139,69,19)
color_transp = (0,0,0,128)

#barra de estados
max_energy = 100
max_food = 100
max_thirst = 100
max_stamina = 100

#colores para las barras de estado
energy_color = (255, 215, 0)  # amarillo
food_color = (255, 165, 0)  # naranja
thirst_color = (0, 191, 255)  # azul claro
stamina_color = (34, 139, 34)  # verde
bar_background = (100, 100, 100)  # color de fondo de la barra gris oscuro
#velocidad
speed = 2

#intervalo de tiempos
status_update_interval = 1000  # en milisegundos
#sistema dia/noche
day_length = 72000       # 24.000 * 3
dawn_time = 18000        # 6:00
morning_time = 24000     # 8:00
dusk_time = 54000        # 18:00
midnight = 72000         # 24:00
max_darkness = 210

#colores para iluminacion
night_color = (20, 20, 50)  # azul oscuro para la noche
day_color = (255, 255, 225)  # blanco dia
dawn_dusk_color = (255, 193, 137)  # color anaranjado para el amanecer y el atardecer

# velocidades de disminucion de estados
food_decrease_rate = 0.01  # tasa de disminución de comida
thirst_decrease_rate = 0.02  # tasa de disminución de sed
energy_decrease_rate = 0.005  # tasa de disminución de energía
energy_increase_rate = 0.001  # tasa de aumento de energía
movement_energy_cost = 0.001  # costo de energía por movimiento

#constantes correr nuevas
walk_Speed = 5
run_speed = 8
stamina_decrease_rate = 0.05  # tasa de disminución de resistencia al correr
stamina_increase_rate = 0.02  # tasa de aumento de resistencia al no correr
run_food_decrease_multiplier = 2.0  # multiplicador de disminución de comida al correr
run_thirst_decrease_multiplier = 2.0  # multiplicador de disminución de sed al correr