import pygame, sys
import constantes
from personajes.players.player import Player
from personajes.worlds import World

# Inicializar pygame
pygame.init()

# Ventana
window = pygame.display.set_mode((constantes.window_width, constantes.window_height))
pygame.display.set_caption("juego nuevo")

clock = pygame.time.Clock()

# --------------------------
# Helpers UI (centrado texto)
# --------------------------
def draw_centered_text(surface, text, y, size=48, color=constantes.color_white, bold=False):
    font = pygame.font.Font(None, size)
    if bold:
        font.set_bold(True)
    render = font.render(text, True, color)
    rect = render.get_rect(center=(constantes.window_width // 2, y))
    surface.blit(render, rect)

def draw_title_screen(surface):
    surface.fill((15, 30, 40))
    draw_centered_text(surface, "TU JUEGO DE SUPERVIVENCIA", constantes.window_height // 2 - 80, size=64, bold=True)
    draw_centered_text(surface, "Moverse: Flechas  |  Correr: Shift  |  Interactuar: E", constantes.window_height // 2, size=32)
    draw_centered_text(surface, "Inventario: I  |  Talá con hacha  |  Ará con azada", constantes.window_height // 2 + 40, size=28)
    draw_centered_text(surface, "Presioná ENTER para jugar  —  ESC para salir", constantes.window_height // 2 + 100, size=32, color=(200, 230, 255))

def draw_game_over(surface, survive_ms):
    surface.fill((30, 10, 10))
    draw_centered_text(surface, "GAME OVER", constantes.window_height // 2 - 80, size=72, color=(255, 100, 100), bold=True)

    # Tiempo sobrevivido
    secs_total = max(0, survive_ms // 1000)
    mins = secs_total // 60
    secs = secs_total % 60
    draw_centered_text(surface, f"Sobreviviste: {mins:02d}:{secs:02d}", constantes.window_height // 2, size=40, color=(255, 220, 220))

    draw_centered_text(surface, "R para reiniciar  —  ESC para salir", constantes.window_height // 2 + 80, size=32, color=(255, 200, 200))

# --------------------------
# Estados de juego
# --------------------------
STATE_MENU = "menu"
STATE_PLAYING = "playing"
STATE_GAMEOVER = "gameover"

def new_run():
    """Crea un mundo y jugador nuevos para cada partida."""
    world = World(constantes.window_width, constantes.window_height)
    player = Player(constantes.window_width // 2, constantes.window_height // 2)
    return world, player

def main():
    state = STATE_MENU
    world = None
    player = None

    show_inventory = False
    camera_x = 0
    camera_y = 0
    status_update_timer = 0

    # métricas de partida
    survive_timer_ms = 0   # acumulado de la partida en curso

    while True:
        dt = clock.tick(constantes.fps)

        # --------------------------
        # Estado: MENÚ INICIAL
        # --------------------------
        if state == STATE_MENU:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit(); sys.exit()
                    if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        # Iniciar nueva partida
                        world, player = new_run()
                        show_inventory = False
                        camera_x = camera_y = 0
                        status_update_timer = 0
                        survive_timer_ms = 0
                        state = STATE_PLAYING

            draw_title_screen(window)
            pygame.display.flip()
            continue

        # --------------------------
        # Estado: GAME OVER
        # --------------------------
        if state == STATE_GAMEOVER:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit(); sys.exit()
                    if event.key == pygame.K_r:
                        # Reiniciar — volver a menú para arrancar limpio con ENTER
                        state = STATE_MENU

            draw_game_over(window, survive_timer_ms)
            pygame.display.flip()
            continue

        # --------------------------
        # Estado: JUGANDO
        # --------------------------
        survive_timer_ms += dt

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if event.type == pygame.KEYDOWN:
                # no permitir interactuar con E si el inventario está abierto
                if event.key == pygame.K_e and not show_inventory:
                    player.interact(world)              # recolección / talado / (arada con azada)
                elif event.key == pygame.K_i:
                    show_inventory = not show_inventory # abrir/cerrar inventario
                elif event.key == pygame.K_f:
                    player.update_food(20); player.update_energy(10)
                elif event.key == pygame.K_t:
                    player.update_thirst(20); player.update_energy(10)
                elif event.key == pygame.K_ESCAPE:
                    # Volver al menú (opcional). Si preferís pausar, se puede cambiar.
                    state = STATE_MENU

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

        # Condición de Game Over (sin salir del juego)
        if player.energy <= 0 or player.food <= 0 or player.thirst <= 0:
            state = STATE_GAMEOVER

        # ---------- DIBUJO ----------
        window.fill((0, 0, 0))
        world.Draw(window, camera_x, camera_y)
        player.draw(window, camera_x, camera_y)

        # Hotbar SIEMPRE + inventario si está abierto
        player.inventory.draw(window, show_inventory)

        pygame.display.flip()

if __name__ == "__main__":
    main()
