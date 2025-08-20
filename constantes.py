width_player,height_player = 50,50 # personaje principal

window_width,window_height=800,600 # pantalla principal



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
#colores para las barras de estado
energy_color = (255, 215, 0)  # amarillo
food_color = (255, 165, 0)  # naranja
thirst_color = (0, 191, 255)  # azul claro
bar_background = (100, 100, 100)  # color de fondo de la barra gris oscuro
#velocidad
speed = 5
#intervalo de tiempos
status_update_interval = 1000  # en milisegundos
#sistema dia/noche
day_length = 72000 # (ajustar duracion del dia)
dawn_time = 18000 # amanecer a las 6:00
morning_time = 24000 # mañana a las 8:00
dusk_time = 54000 # atardecer a las 18:00
midnight = 72000 # medianoche a las 00:00
max_darkness = 210  # (ajustar nivel maximo de oscuridad)(0-255)
#colores para iluminacion
night_color = (20, 20, 50)  # azul oscuro para la noche
day_color = (255, 255, 225)  # blanco dia
dawn_dusk_color = (255, 193, 137)  # color anaranjado para el amanecer y el atardecer