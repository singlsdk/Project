import pygame as pg
from os import path
from locals import *

pg.init()
_ = pg.display.set_mode([WIDTH, HEIGHT])


crop_rectangles = {
    'skull.png': [[0, 0, 39, 31], [50, 0, 30, 31], [89, 0, 23, 31], [122, 0, 30, 31], [158, 0, 39, 31]],
    'cacodemon.png': [[0, 0, 70, 70], [70, 0, 70, 70], [140, 0, 76, 70], [216, 0, 70, 70], [286, 0, 70, 70]]
}


def get_sprite_set(file_name, height=100):

    pth = path.join('sprites', file_name)

    sheet = pg.image.load(pth)

    sprite_set = {}

    for i in range(5):
        rect = pg.Rect(crop_rectangles[file_name][i])
        image = pg.Surface(rect.size).convert()
        image.blit(sheet, (0, 0), rect)
        image.set_colorkey(Color.CYAN)
        width = height * image.get_width() / image.get_height()
        image = pg.transform.scale(image, (width, height))
        sprite_set[45*i] = image
        flipped_image = pg.transform.flip(image, True, False)
        sprite_set[- 45 * i] = flipped_image

    return sprite_set


