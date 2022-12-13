from objects import *
from locals import *
import pygame as pg
from levels import *
from menu import *


class Game:
    STATES = ['MainMenu', 'PauseMenu', '3D']

    def __init__(self, screen: pg.Surface):
        self.state = 'MainMenu'
        self.objects = []
        self.screen = screen
        self.level = None
        self.main_menu = MainMenu(self.screen)
        self.pause_menu = PauseMenu(self.screen)
        self.finished = 0

    def update(self):

        if self.finished == 1:
            pg.quit()

        if self.state == 'MainMenu':
            pg.mouse.set_visible(True)
            self.main_menu.update()
            self.main_menu.draw()

        if self.state == 'PauseMenu':
            pg.mouse.set_visible(True)
            self.pause_menu.update()
            self.pause_menu.draw()

        if self.state == '3D':
            pg.mouse.set_visible(False)
            self.level.update()
            self.level.draw(self.screen)

    def events(self, event):
        if self.state == 'MainMenu':
            self.main_menu.event(self, event)

        if self.state == 'PauseMenu':
            self.pause_menu.event(self, event)

        if self.state == '3D':
            self.level.event(self, event)

