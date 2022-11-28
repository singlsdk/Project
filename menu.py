from locals import *
from buttons import Button


class Menu:

    def __init__(self, screen):
        self.screen = screen
        self.chosen_button_number = 0

        self.title_text = None
        self.buttons_text = None

        self.title = self.get_title()
        self.buttons = []
        self.chosen_button = None
        # self.update()

    def get_title(self):
        font_name = "OldLondon.ttf"
        font_size = 50
        font = Font(font_name, font_size).font
        return Button(self.screen, [WIDTH / 2, 100], font, self.title_text)

    def update(self):

        self.buttons = []
        font_name = "OldLondon.ttf"
        font_size = 50
        font_main = Font(font_name, font_size).font
        font_bigger = Font(font_name, int(font_size * 1.5)).font
        for button_number in range(len(self.buttons_text)):
            deviation_from_center = np.array([0, -100 + button_number * (1.5 * font_size)])
            if button_number != self.chosen_button_number:
                self.buttons.append(Button(self.screen, CENTER + deviation_from_center,
                                           font_main, self.buttons_text[button_number]))
            else:
                self.chosen_button = Button(self.screen, CENTER + deviation_from_center,
                                            font_bigger, self.buttons_text[button_number])
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


class MainMenu(Menu):
    TITLE = 'Name of the Game'
    NEW_GAME = 'New Game'
    QUIT = 'Quit'
    BUTTONS = [NEW_GAME, QUIT]

    def __init__(self, screen):
        super().__init__(screen)
        self.title_text = MainMenu.TITLE
        self.title = self.get_title()
        self.buttons_text = MainMenu.BUTTONS
