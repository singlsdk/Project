from locals import *


class Button:

    def __init__(self, screen, center, font, inbox_text):
        self.center = center
        self.screen = screen
        self.font = font
        self.inbox_text = inbox_text
        self.rendered_text = self.font.render(self.inbox_text, True, Color.WHITE)
        self.text_rect = self.rendered_text.get_rect(center=self.center)

    def draw(self):
        self.screen.blit(self.rendered_text, self.text_rect)
