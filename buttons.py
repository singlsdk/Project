from locals import *


class MenuButton:

    def __init__(self, screen, center, font, inbox_text, number=None):
        self.center = center
        self.screen = screen
        self.font = font
        self.inbox_text = inbox_text
        self.rendered_text = self.font.render(self.inbox_text, True, Color.WHITE)
        self.text_rect = self.rendered_text.get_rect(center=self.center)
        self.number = number
        self.pressed = False

    def is_mouse_on(self):
        return self.text_rect.collidepoint((pg.mouse.get_pos()))

    def draw(self):
        self.rendered_text = self.font.render(self.inbox_text, True, Color.WHITE)
        self.text_rect = self.rendered_text.get_rect(center=self.center)
        self.screen.blit(self.rendered_text, self.text_rect)
