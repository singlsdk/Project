from locals import *


class Button:

    def __init__(self, screen, center, font, text):
        self.center = center
        self.screen = screen
        self.font = font
        self.text = text

    def draw(self):
        text = self.font.render(self.text, True, Color.WHITE)
        text_rect = text.get_rect(center=self.center)
        self.screen.blit(text, text_rect)
