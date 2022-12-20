import pygame
import numpy as np
from random import choice, randrange, randint

from locals import Color
from objects import Wall

global RES
global HEIGHT, WIDTH
global TILE
TILE = 50
global right_indent, bottom_indent
global cup_score, game_start
game_start = 0
global cols, rows
global player_health

# Алгоритм "Recursive Backtracker"

#Задаем размеры окна и размер одной клетки
#RES = WIDTH, HEIGHT = 1002, 502#RES[0], RES[1]
#TILE = 50
#cols, rows = WIDTH // TILE, HEIGHT // TILE

def set_easy():
    global RES
    RES = [1002, 502]
    global WIDTH
    WIDTH = 1002
    global HEIGHT
    HEIGHT = 502
    global cols
    cols = WIDTH // TILE
    global rows
    rows = HEIGHT // TILE
    global right_indent
    right_indent = 50
    global bottom_indent
    bottom_indent = 30
    global cup_score
    cup_score = 3
    global game_start
    game_start = 1
    global player_health
    player_health = 3

def set_medium():
    global RES
    RES = [1302, 702]
    global WIDTH
    WIDTH = 1302
    global HEIGHT
    HEIGHT = 702
    global cols
    cols = WIDTH // TILE
    global rows
    rows = HEIGHT // TILE
    global right_indent
    right_indent = 50
    global bottom_indent
    bottom_indent = 30
    global cup_score
    cup_score = 3
    global game_start
    game_start = 1
    global player_health
    player_health = 2

def set_hard():
    global RES
    RES = [1402, 802]
    global WIDTH
    WIDTH = 1402
    global HEIGHT
    HEIGHT = 802
    global cols
    cols = WIDTH // TILE
    global rows
    rows = HEIGHT // TILE
    global right_indent
    right_indent = 50
    global bottom_indent
    bottom_indent = 30
    global cup_score
    cup_score = 3
    global game_start
    game_start = 1
    global player_health
    player_health = 1

def get_complexity():
    if WIDTH == 1402:
        return 'Hard'
    elif WIDTH == 1302:
        return 'Medium'
    elif WIDTH == 1002:
        return 'Easy'
def get_res():
    return RES

def get_right_indent():
    return right_indent

def get_bottom_indent():
    return bottom_indent

def get_player_health():
    return player_health

def damage_player():
    global player_health
    player_health -= 1

def get_cols():
    return cols

def get_rows():
    return rows

def get_width():
    return WIDTH

def get_height():
    return HEIGHT

def get_cup_score():
    return cup_score

class Cell:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False
        self.thickness = 4

    def draw(self, sc):
        x, y = self.x * TILE, self.y * TILE

        if self.walls['top']:
            pygame.draw.line(sc, pygame.Color('darkorange'), (x, y), (x + TILE, y), self.thickness)
        if self.walls['right']:
            pygame.draw.line(sc, pygame.Color('darkorange'), (x + TILE, y), (x + TILE, y + TILE), self.thickness)
        if self.walls['bottom']:
            pygame.draw.line(sc, pygame.Color('darkorange'), (x + TILE, y + TILE), (x , y + TILE), self.thickness)
        if self.walls['left']:
            pygame.draw.line(sc, pygame.Color('darkorange'), (x, y + TILE), (x, y), self.thickness)

    def get_rects(self):
        rects = []
        x, y = self.x * TILE, self.y * TILE
        if self.walls['top']:
            rects.append(pygame.Rect((x, y), (TILE, self.thickness)))
        if self.walls['right']:
            rects.append(pygame.Rect((x + TILE, y), (self.thickness, TILE)))
        if self.walls['bottom']:
            rects.append(pygame.Rect((x, y + TILE), (TILE , self.thickness)))
        if self.walls['left']:
            rects.append(pygame.Rect((x, y), (self.thickness, TILE)))
        return rects

    def check_cell(self, x, y):
        find_index = lambda x,y:  x + y * cols
        if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
            return False
        return self.grid_cells[find_index(x, y)]

    def check_neighbors(self, grid_cells):
        self.grid_cells = grid_cells
        neighbors = []
        top = self.check_cell(self.x, self.y - 1)
        right = self.check_cell(self.x + 1, self.y)
        bottom = self.check_cell(self.x, self.y + 1)
        left = self.check_cell(self.x - 1, self.y)
        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if left and not left.visited:
            neighbors.append(left)
        return choice(neighbors) if neighbors else False

#Fixed
def get_walls(grid_cells):
    walls = []
    for cell in grid_cells:
        if cell.walls['top']:
            walls.append(Wall(np.array([cell.x * TILE, cell.y * TILE]), np.array([1, 0]), [0, 200], TILE, Color.GREEN))
        if cell.walls['bottom']:
            walls.append(Wall(np.array([cell.x * TILE, (cell.y + 1) * TILE]), np.array([1, 0]), [0, 200], TILE, Color.GREEN))
        if cell.walls['right']:
            walls.append(Wall(np.array([(cell.x + 1) * TILE, cell.y * TILE]), np.array([0, 1]), [0, 200], 10*TILE , Color.GREEN))
        if cell.walls['left']:
            walls.append(Wall(np.array([cell.x * TILE, cell.y * TILE]), np.array([0, 1]), [0, 200], TILE, Color.GREEN))
    return walls


def remove_walls(current, next):
    dx = current.x - next.x
    if dx == 1:
        current.walls['left'] = False
        next.walls['right'] = False
    elif dx == -1:
        current.walls['right'] = False
        next.walls['left'] = False
    dy = current.y - next.y
    if dy == 1:
        current.walls['top'] = False
        next.walls['bottom'] = False
    elif dy == -1:
        current.walls['bottom'] = False
        next.walls['top'] = False

def generate_maze():
    grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)]
    current_cell = grid_cells[0]
    array = []
    break_count = 1

    while break_count != len(grid_cells):
        current_cell.visited = True
        next_cell = current_cell.check_neighbors(grid_cells)
        if next_cell:
            next_cell.visited = True
            break_count += 1
            array.append(current_cell)
            remove_walls(current_cell, next_cell)
            current_cell = next_cell
        elif array:
            current_cell = array.pop()
    return grid_cells