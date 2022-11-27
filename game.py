from objects import *
from locals import *
import pygame as pg
from buttons import Button
from levels import *

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
        self.chosen_button = None
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
                self.chosen_button = Button(self.screen, CENTER + deviation_from_center,
                                            font_bigger, Menu.BUTTONS[button_number])
                self.buttons.append(self.chosen_button)

    def draw_arrow(self):
        font_name = "OldLondon.ttf"
        font_size = 50
        font = Font(font_name, font_size).font
        deviation_from_text = 50
        right_position = [self.chosen_button.text_rect.left - deviation_from_text, self.chosen_button.center[1]]
        arrow_left = Button(self.screen, right_position, font, '<')
        arrow_left.draw()
        left_position = [self.chosen_button.text_rect.right + deviation_from_text, self.chosen_button.center[1]]
        arrow_right = Button(self.screen, left_position, font, '<')
        arrow_right.draw()

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
        self.level = None
        self.menu = Menu(self.screen)

    def update(self):

        if self.state == 'Menu':
            self.menu.update()
            self.menu.draw()

        if self.state == '3D':
            self.level.update()
            self.level.draw(self.screen, self.level.camera)

    def events(self, event):
        if self.state == 'Menu':

            if event.type == pg.KEYDOWN:
                direction = 0
                if event.key in [Key.w, Key.arrow_up]:
                    direction = -1
                if event.key in [Key.s, Key.arrow_down]:
                    direction = 1

                self.menu.chosen_button_number = (self.menu.chosen_button_number + direction) % len(Menu.BUTTONS)

                if event.key in [Key.enter]:
                    button = Menu.BUTTONS[self.menu.chosen_button_number]
                    if button == Menu.NEW_GAME:
                        self.level = LEVEL_1
                        self.state = '3D'
                    if button == Menu.QUIT:
                        pass

        if self.state == '3D':
            self.level.event(event)

