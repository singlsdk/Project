from locals import *
from buttons import MenuButton
from levels import *


class Menu:

    def __init__(self, screen, title_text, buttons_text, font_of_title, font_of_text, bigger_font_of_text):
        self.screen = screen
        self.chosen_button_number = 0

        self.title_text = title_text
        self.buttons_text = buttons_text

        self.font_of_title = font_of_title
        self.font_of_text = font_of_text
        self.bigger_font_of_text = bigger_font_of_text

        self.title = MenuButton(self.screen, [WIDTH / 2, 100], self.font_of_title, self.title_text)
        self.buttons = []
        self.chosen_button_number = 0
        self.create_buttons()

    def get_deviation_from_center(self, button_number):
        return np.array([0, -100 + button_number * (2 * self.font_of_text.get_height())])

    def create_buttons(self):
        self.buttons = []
        for button_number in range(len(self.buttons_text)):
            deviation_from_center = self.get_deviation_from_center(button_number)
            button = MenuButton(self.screen, CENTER + deviation_from_center,
                                self.font_of_text, self.buttons_text[button_number], button_number)

            self.buttons.append(button)

    def update(self):
        self.draw_arrow()
        for i in range(len(self.buttons_text)):
            if self.buttons[i].number == self.chosen_button_number:
                self.buttons[i].font = self.bigger_font_of_text
            else:
                self.buttons[i].font = self.font_of_text

    def draw_arrow(self):
        deviation_from_text = 50
        chosen_button = self.buttons[self.chosen_button_number]
        right_position = [chosen_button.text_rect.left - deviation_from_text, chosen_button.center[1]]
        arrow_left = MenuButton(self.screen, right_position, self.bigger_font_of_text, '<')
        arrow_left.draw()
        left_position = [chosen_button.text_rect.right + deviation_from_text, chosen_button.center[1]]
        arrow_right = MenuButton(self.screen, left_position, self.bigger_font_of_text, '<')
        arrow_right.draw()

    def draw(self):
        self.screen.fill(Color.BLACK)
        for button in self.buttons:
            button.draw()
        self.title.draw()
        self.draw_arrow()

    def choose_button_by_mouse(self):
        for button in self.buttons:
            if button.is_mouse_on():
                self.chosen_button_number = button.number

    def press_button(self, game):
        pass

    def event(self, game, event):
        if event.type == pg.KEYDOWN:
            direction = 0
            if event.key in [Key.w, Key.arrow_up]:
                direction = -1
            if event.key in [Key.s, Key.arrow_down]:
                direction = 1

            self.chosen_button_number = \
                (self.chosen_button_number + direction) % len(MainMenu.BUTTONS)

            if event.key in [Key.enter]:
                self.press_button(game)

        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                for button in self.buttons:
                    if button.is_mouse_on():
                        self.press_button(game)

        if event.type == pg.MOUSEMOTION:
            self.choose_button_by_mouse()


class MainMenu(Menu):
    TITLE = 'Name of the Game'
    NEW_GAME = 'New Game'
    QUIT = 'Quit'

    FONT_OF_TITLE = pg.font.Font(Font.GOTHIC, 90)
    FONT_OF_TEXT = pg.font.Font(Font.GOTHIC, 60)
    BIGGER_FONT_OF_TEXT = pg.font.Font(Font.GOTHIC, 75)

    BUTTONS = [NEW_GAME, QUIT]

    def __init__(self, screen):
        super().__init__(screen, MainMenu.TITLE, MainMenu.BUTTONS,
                         MainMenu.FONT_OF_TITLE, MainMenu.FONT_OF_TEXT, MainMenu.BIGGER_FONT_OF_TEXT)

    def press_button(self, game):
        button_text = self.buttons[self.chosen_button_number].inbox_text
        if button_text == MainMenu.NEW_GAME:
            game.level = LEVEL_1
            game.state = '3D'
        if button_text == MainMenu.QUIT:
            game.finished = 1


class PauseMenu(Menu):
    TITLE = 'Game Paused'
    CONTINUE = 'Continue'
    MENU = 'Go To Menu'

    FONT_OF_TITLE = pg.font.Font(Font.GOTHIC, 90)
    FONT_OF_TEXT = pg.font.Font(Font.GOTHIC, 60)
    BIGGER_FONT_OF_TEXT = pg.font.Font(Font.GOTHIC, 75)

    BUTTONS = [CONTINUE, MENU]

    def __init__(self, screen):
        super().__init__(screen, PauseMenu.TITLE, PauseMenu.BUTTONS,
                         PauseMenu.FONT_OF_TITLE, PauseMenu.FONT_OF_TEXT, PauseMenu.BIGGER_FONT_OF_TEXT)

    def press_button(self, game):
        button_text = self.buttons[self.chosen_button_number].inbox_text
        if button_text == PauseMenu.CONTINUE:
            game.state = '3D'
        if button_text == PauseMenu.MENU:
            game.main_menu.chosen_button_number = 0
            game.state = 'MainMenu'
