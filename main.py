import pygame, sys
import constantes
from personajes.players.player import Player
from personajes.worlds import World
import random

# Inicializar pygame
pygame.init()

# Ventana
window = pygame.display.set_mode((constantes.window_width, constantes.window_height))
pygame.display.set_caption("juego nuevo")

clock = pygame.time.Clock()

def main():
    clock = pygame.time.Clock()
    window.fill(constantes.color_blue)
    world = World(constantes.window_width, constantes.window_height)
    player = Player(constantes.window_width // 2, constantes.window_height // 2)
    show_inventory = False

    camera_x = 0
    camera_y = 0
    status_update_timer = 0

    while True:
        dt = clock.tick(60)

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # ARREGLO: no permitir interactuar con E si el inventario está abierto
                if event.key == pygame.K_e and not show_inventory:
                    player.interact(world)              # recolección / talado

                elif event.key == pygame.K_i:
                    show_inventory = not show_inventory # abrir/cerrar inventario

                elif event.key == pygame.K_f:
                    player.update_food(20)
                    player.update_energy(10)

                elif event.key == pygame.K_t:
                    player.update_thirst(20)
                    player.update_energy(10)

            if event.type == pygame.MOUSEBUTTONDOWN:
                player.inventory.handle_click(pygame.mouse.get_pos(), event.button, show_inventory)
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                player.inventory.handle_click(pygame.mouse.get_pos(), event.button, show_inventory)

        # Movimiento
        dx = dy = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:  dx -= 5
        if keys[pygame.K_RIGHT]: dx += 5
        if keys[pygame.K_UP]:    dy -= 5
        if keys[pygame.K_DOWN]:  dy += 5
        player.is_running = keys[pygame.K_LSHIFT] and player.stamina > 0
        player.move(dx, dy, world)

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

        # ---------- DIBUJO ----------
        window.fill((0, 0, 0))
        world.Draw(window, camera_x, camera_y)
        player.draw(window, camera_x, camera_y)

        # Hotbar SIEMPRE + inventario si está abierto
        player.inventory.draw(window, show_inventory)

        pygame.display.flip()
        #este si funciona

if __name__ == "__main__":
    main()
