import pygame
from objects import *
from locals import *


def main():
    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    clock = pygame.time.Clock()
    finished = False

    camera = Camera()
    objects = []

    while not finished:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True

        draw(objects, screen, camera)
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
