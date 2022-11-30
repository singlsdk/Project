from objects import *
from locals import *
import pygame as pg
from buttons import Button
from levels import *
from menu import *

# TODO: use mouse in menu


class Game:
    STATES = ['MainMenu', '3D', '2D']

    def __init__(self, screen: pg.Surface):
        self.state = 'MainMenu'
        self.objects = []
        self.screen = screen
        self.level = None
        self.main_menu = MainMenu(self.screen)

    def update(self):

        if self.state == 'MainMenu':
            pg.mouse.set_visible(True)
            self.main_menu.update()
            self.main_menu.draw()

        if self.state == '3D':
            pg.mouse.set_visible(False)
            self.level.update()
            self.level.draw(self.screen)

    def events(self, event):
        if self.state == 'MainMenu':

            if event.type == pg.KEYDOWN:
                direction = 0
                if event.key in [Key.w, Key.arrow_up]:
                    direction = -1
                if event.key in [Key.s, Key.arrow_down]:
                    direction = 1

                self.main_menu.chosen_button_number =\
                    (self.main_menu.chosen_button_number + direction) % len(MainMenu.BUTTONS)

                if event.key in [Key.enter]:
                    button = MainMenu.BUTTONS[self.main_menu.chosen_button_number]
                    if button == MainMenu.NEW_GAME:
                        self.level = LEVEL_1
                        self.state = '3D'
                    if button == MainMenu.QUIT:
                        pass

        if self.state == '3D':
            self.level.event(event)

