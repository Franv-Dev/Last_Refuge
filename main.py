import pygame,sys
import constantes
from personajes.players.player import Player 
from personajes.worlds import World

#inicializar pygame
pygame.init()

#ancho y alto de pantalla
window = pygame.display.set_mode(((
    constantes.window_width,constantes.window_height
    )))

#nombre 
pygame.display.set_caption("juego nuevo")

#definir movimiento
mov_left,mov_right,mov_up,mov_down = False,False,False,False


#controlador de velocidad(frame rate)

clock = pygame.time.Clock()

#funcion principal
def main():
    window.fill(constantes.color_blue)#pintar fondo
    world = World(constantes.window_width,constantes.window_height)
    player = Player(constantes.window_width//2,constantes.window_height//2)
    
    show_inventory = False
    
    
    status_update_timer = 0
    #bucle de arranque
    while True:
        dt = clock.tick(constantes.fps)
        #evento de cierre
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  
                sys.exit()
            #presionar tecla
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    player.interact(world)
                if event.key == pygame.K_i:
                    show_inventory = not show_inventory
                if event.key == pygame.K_f:
                    player.update_food(20)
                if event.key == pygame.K_t:
                    player.update_thirst(20)

        #configurar teclas
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            player.Move(-constantes.speed,0,world) #llamar el metodo del movimiento
        if keys[pygame.K_RIGHT]:
            player.Move(constantes.speed,0,world)
        if keys[pygame.K_UP]:
            player.Move(0,-constantes.speed,world)
        if keys[pygame.K_DOWN]:
            player.Move(0,constantes.speed,world)
        
        status_update_timer += dt #actualiza timer
        if status_update_timer >= constantes.status_update_interval:  
            player.update_status()  # disminuir status
            status_update_timer = 0
        if player.energy <= 0 or player.food <= 0 or player.thirst <= 0:
            print("Game Over")
            pygame.quit()
            sys.exit()

        #dibujo de objetos y jugador
        world.Draw(window)
        player.Draw(window)
        if show_inventory:
            player.draw_inventory(window)
        
        font= pygame.font.Font(None, 24)
        energy_text = font.render(f"Energy:{int(player.energy)}", True, constantes.color_white)
        food_text = font.render(f"Food: {int(player.food)}", True, constantes.color_white)
        thirst_text = font.render(f"Thirst: {int(player.thirst)}", True, constantes.color_white)

        window.blit(energy_text, (10,constantes.window_height - 70))
        window.blit(food_text, (10,constantes.window_height - 45))
        window.blit(thirst_text, (10,constantes.window_height - 20))

        #actualizar visualizacion de la ventana
        pygame.display.flip()
        


if __name__ == "__main__":
    main()