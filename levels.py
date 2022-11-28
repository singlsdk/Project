from objects import *


def draw_floor(screen):
    color = Color.BROWN
    pg.draw.rect(screen, color, [0, HEIGHT/2, WIDTH, HEIGHT/2])


class Level:

    def __init__(self, objects):
        self.camera = Camera()
        self.objects = objects
        self.motion_direction = {key: 0 for key in Camera.move_keys.keys()}

    def event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key in Camera.move_keys.keys():
                self.motion_direction[event.key] = 1
        if event.type == pg.KEYUP:
            self.motion_direction = {key: 0 for key in Camera.move_keys.keys()}

    def update(self):
        self.camera.update(self.motion_direction)
        for obj in self.objects:
            obj.update()

    def get_sticks_from_objects(self, screen):
        sticks = []
        for obj in self.objects:
            sticks += obj.sticks(screen, self.camera)
        return sticks

    def draw(self, screen: pg.Surface, camera: Camera):
        screen.fill(Color.WHITE)
        draw_floor(screen)
        sticks = self.get_sticks_from_objects(screen)
        sticks = list(filter(lambda x: abs(x.angle) <= camera.angle_of_vision, sticks))
        sticks = sorted(sticks, key=lambda x: x.r, reverse=True)
        for stick in sticks:
            stick.draw_3d()
