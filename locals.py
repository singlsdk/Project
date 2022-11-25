import numpy as np

# TODO: make font

"""
Defines global scope constants
"""

# Refresh rate
FPS = 30

# Screen resolution
WIDTH, HEIGHT = 1500, 750
CENTER = np.array([WIDTH/2, HEIGHT/2])


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


class Text:
    """ Stores game text messages as static variables """
