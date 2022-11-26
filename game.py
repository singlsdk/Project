from objects import *
from locals import *
import pygame as pg
from buttons import Button

# TODO: use mouse in menu


class Menu:
    TITLE = 'Name of the Game'
    NEW_GAME = 'New Game'
    QUIT = 'Quit'
    BUTTONS = [NEW_GAME, QUIT]

    def __init__(self, screen):
        self.screen = screen
        self.chosen_button_number = 0

        self.title = self.title()
        self.buttons = []
        self.update()

    def title(self):
        font_name = "OldLondon.ttf"
        font_size = 50
        font = Font(font_name, font_size).font
        return Button(self.screen, [WIDTH / 2, 100], font, Menu.TITLE)

    def update(self):

        self.buttons = []
        font_name = "OldLondon.ttf"
        font_size = 50
        font_main = Font(font_name, font_size).font
        font_bigger = Font(font_name, int(font_size * 1.5)).font
        for button_number in range(len(Menu.BUTTONS)):
            deviation_from_center = np.array([0, -100 + button_number * (1.5 * font_size)])
            if button_number != self.chosen_button_number:
                self.buttons.append(Button(self.screen, CENTER + deviation_from_center,
                                           font_main, Menu.BUTTONS[button_number]))
            else:
                self.buttons.append(Button(self.screen, CENTER + deviation_from_center,
                                           font_bigger, Menu.BUTTONS[button_number]))

    def draw_arrow(self):
        pass

    def draw(self):
        self.screen.fill(Color.BLACK)
        for button in self.buttons:
            button.draw()
        self.title.draw()
        self.draw_arrow()


class Game:
    STATES = ['Menu', '3D', '2D']

    def __init__(self, screen):
        self.state = 'Menu'
        self.objects = []
        self.screen = screen
        self.camera = Camera()
        self.menu = Menu(self.screen)

    def update(self):

        if self.state == 'Menu':
            self.menu.update()
            self.menu.draw()

        if self.state == '3D':
            draw(self.objects, self.screen, self.camera)

    def events(self, event):
        if self.state == 'Menu':

            if event.type == pg.KEYDOWN:
                if event.key in [Key.w, Key.arrow_up]:
                    if self.menu.chosen_button_number > 0:
                        self.menu.chosen_button_number -= 1
                if event.key in [Key.s, Key.arrow_down]:
                    if self.menu.chosen_button_number < len(Menu.BUTTONS) - 1:
                        self.menu.chosen_button_number += 1

                if event.key in [Key.enter]:
                    button = Menu.BUTTONS[self.menu.chosen_button_number]
                    if button == Menu.NEW_GAME:
                        pass
                    if button == Menu.QUIT:
                        pass
