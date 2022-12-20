import pygame
from objects import *
from locals import *
from game import *

# TODO: refactoring
#   TODO: change imports in all files (remove *)
#   TODO: rename classes and vars to avoid difference only in letter cases
#   TODO: remove screen and camera from args


def main():
    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    game = Game(screen)

    clock = pygame.time.Clock()
    finished = False

    while not finished:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            else:
                game.events(event)

        game.update()
        pygame.display.update()

    pygame.quit()

if __name__ == '__main__':
    main()
