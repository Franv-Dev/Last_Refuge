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
    #bucle de arranque
    while True:
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

        #dibujo de objetos y jugador
        world.Draw(window)
        player.Draw(window)
        if show_inventory:
            player.draw_inventory(window)
        else:
            world.draw_inventory(window,player)

        #actualizar visualizacion de la ventana
        pygame.display.flip()
        clock.tick(constantes.fps)


if __name__ == "__main__":
    main()