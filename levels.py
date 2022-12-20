from maze_generator import generate_maze, get_walls
from objects import *


def draw_floor(screen):
    color = Color.BROWN
    pg.draw.rect(screen, color, [0, HEIGHT/2, WIDTH, HEIGHT/2])


class Level:

    def __init__(self, objects):
        self.camera = Camera(pos=np.array([200, 200]))
        self.objects = objects
        self.motion_direction = {key: 0 for key in Camera.move_keys.keys()}
        self.drawable_objects = []

    def event(self, game, event):
        if event.type == pg.KEYDOWN:
            if event.key in Camera.move_keys.keys():
                self.motion_direction[event.key] = 1

            if event.key in [Key.esc]:
                game.state = 'PauseMenu'

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

    def draw(self, screen: pg.Surface):
        screen.fill(Color.WHITE)
        draw_floor(screen)
        self.drawable_objects = []
        for obj in self.objects:
            if obj.__class__.__bases__[0].__name__ == 'StickObject':
                self.drawable_objects += obj.sticks(screen, self.camera)
            elif obj.__class__.__bases__[0].__name__ == 'DrawableObject':
                self.drawable_objects.append(obj)

        for obj in self.drawable_objects:
            obj.get_parameters(self.camera)

        draw_distance = 500
        self.drawable_objects = list(filter(lambda x: draw_distance > x.r > 0, self.drawable_objects))
        self.drawable_objects = sorted(self.drawable_objects, key=lambda x: x.r, reverse=True)
        for drawable_obj in self.drawable_objects:
            drawable_obj.draw(screen, self.camera)

maze = generate_maze()
objects_1 = get_walls(maze)
print(len(objects_1))
for wall in objects_1:
    print(wall.pos, wall.pos + wall.vec * wall.width, wall.z)
LEVEL_1 = Level(objects_1)
