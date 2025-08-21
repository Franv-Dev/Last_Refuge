import pygame, sys
import constantes
from personajes.players.player import Player 
from personajes.worlds import World
import random

# Inicializar pygame
pygame.init()

# Ancho y alto de pantalla
window = pygame.display.set_mode((
    constantes.window_width, constantes.window_height
))

# Nombre de la ventana
pygame.display.set_caption("juego nuevo")

# Controlador de velocidad (frame rate)
clock = pygame.time.Clock()

# Función principal
def main():
    clock = pygame.time.Clock()
    window.fill(constantes.color_blue)  # Pintar fondo
    world = World(constantes.window_width, constantes.window_height)
    player = Player(constantes.window_width // 2, constantes.window_height // 2)
    show_inventory = False

    camera_x = 0
    camera_y = 0

    status_update_timer = 0
    # Bucle de arranque
    while True:
        dt = clock.tick(60)
        # Evento de cierre
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  
                sys.exit()
            # Presionar tecla
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    player.interact(world)
                if event.key == pygame.K_i:
                    show_inventory = not show_inventory
                if event.key == pygame.K_f:
                    player.update_food(20)
                    player.update_energy(10)
                if event.key == pygame.K_t:
                    player.update_thirst(20)
                    player.update_energy(10)
            if event.type == pygame.MOUSEBUTTONDOWN:
                player.inventory.handle_click(pygame.mouse.get_pos(), event.button, show_inventory)
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                player.inventory.handle_click(pygame.mouse.get_pos(), event.button, show_inventory)

        # Configurar teclas
        dx = dy = 0
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            dx -= 5
        if keys[pygame.K_RIGHT]:
            dx += 5
        if keys[pygame.K_UP]:
            dy -= 5
        if keys[pygame.K_DOWN]:
            dy += 5
        player.is_running = keys[pygame.K_LSHIFT] and player.stamina > 0
        player.Move(dx, dy, world) 

        camera_x = player.x - constantes.window_width // 2
        camera_y = player.y - constantes.window_height // 2

        world.update_chunk(player.x, player.y)
        world.update_time(dt)
        
        status_update_timer += dt
        if status_update_timer >= constantes.status_update_interval:  
            player.update_status()
            status_update_timer = 0
        if player.energy <= 0 or player.food <= 0 or player.thirst <= 0:
            print("Game Over")
            pygame.quit()
            sys.exit()

        # Limpiar pantalla
        window.fill((0,0,0))

        # Dibujo de objetos y jugador
        world.Draw(window, camera_x, camera_y)
        player.draw(window, camera_x, camera_y)

        # Dibuja SIEMPRE la hotbar (inventario inferior)
        player.inventory.draw(window, show_inventory=False)

        # Dibuja la grilla central SOLO si show_inventory es True
        if show_inventory:
            player.inventory.draw(window, show_inventory=True)

        # Dibuja las barras de estado en la esquina superior izquierda
        player.draw_status_bars(window)

        # Actualizar visualización de la ventana
        pygame.display.flip()

if __name__ == "__main__":
    main()