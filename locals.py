import numpy as np
from os import path
import pygame as pg

# TODO: make font class

"""
Defines global scope constants
"""

# Refresh rate
FPS = 30

# Screen resolution
WIDTH, HEIGHT = 1500, 750
CENTER = np.array([WIDTH/2, HEIGHT/2])


class Font:
    pg.font.init()

    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.path = path.join('fonts', self.name)
        self.font = pg.font.Font(self.path, self.size)


class Color:
    """ Defines a set of colors used in the project """

    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    GREEN = (0, 255, 0)
    MAGENTA = (255, 0, 255)
    CYAN = (0, 255, 255)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BROWN = (200, 100, 0)


class Key:

    w = 119
    a = 97
    s = 115
    d = 100

    arrow_up = 1073741906
    arrow_down = 1073741905

    enter = 13
