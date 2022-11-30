import pygame as pg
from locals import *
from sprites import *

# TODO: remove screen, camera from args
# TODO: fix 3D color
# TODO: fix gaps in walls
# TODO: make collisions


def rotated(vec: np.ndarray, angle: float):
    """
    :param vec: 2D vector
    :param angle: angle of rotation in radians
    :return: vector rotated on angle
    """
    rotation_matrix = np.array([[np.cos(angle), -np.sin(angle)],
                                [np.sin(angle), np.cos(angle)]])

    vec = np.matmul(vec, np.transpose(rotation_matrix))
    return vec


def distance_from_line(pos, point, vec):
    return abs(np.dot(point - pos, rotated(vec, np.pi/2)))


def angle_between_two_vectors(vec1, vec2):
    vec1 = vec1 / np.linalg.norm(vec1)
    vec2 = vec2 / np.linalg.norm(vec2)
    angle = np.arccos(np.dot(vec1, vec2))
    if vec1[0]*vec2[1] - vec1[1]*vec2[0] >= 0:
        angle = - angle

    return angle * 180 / np.pi


class Camera:
    move_keys = {Key.w: 0.0, Key.a: -np.pi / 2,
                 Key.s: np.pi, Key.d: np.pi / 2}

    def __init__(self, r_0: float = 1000.0, l_0: float = 1000.0, height: float = 100.0,
                 pos: np.ndarray[int] = np.array([0, 0]), velocity: float = 40.0,
                 view_vector: np.ndarray = np.array([1.0, 0.0])):
        self.r_0 = r_0
        self.l_0 = l_0
        self.height = height
        self.pos = pos
        self.velocity = velocity
        self.view_vec = view_vector
        self.screen_vec = rotated(self.view_vec, np.pi / 2)
        self.angle_of_vision = np.arctan(self.l_0 / self.r_0)
        self.motion_direction = {key: 0 for key in Camera.move_keys.keys()}

    def move(self):
        # TODO: make collisions with objects
        # TODO: change motion direction
        for i in self.motion_direction.keys():
            if self.motion_direction[i] == 1:
                self.pos += np.array(
                    list(map(lambda x: int(x),
                             (self.velocity * rotated(self.view_vec, Camera.move_keys[i])).round())))

    def rotate(self):
        angle_velocity = 0.001
        self.view_vec = rotated(self.view_vec, pg.mouse.get_rel()[0] * angle_velocity)
        pg.mouse.set_pos(CENTER)
        self.screen_vec = rotated(self.view_vec, np.pi / 2)

    def update(self, motion_direction):
        self.motion_direction = motion_direction
        self.move()
        self.rotate()

    def no_collisions(self, walls):
        collision_distance = 20
        for wall in walls:
            if (np.linalg.norm(self.pos - wall.pos) < collision_distance**2) or \
                    (np.linalg.norm(self.pos - (wall.pos + wall.width * wall.vec)) < collision_distance ** 2) or \
                    (distance_from_line(self.pos, wall.pos, wall.vec) < collision_distance):
                return False

        return True


class Object:

    def update(self):
        pass


class DrawableObject(Object):

    def __init__(self, pos):
        self.pos = pos
        self.k = None
        self.t = None
        self.angle = None
        self.r = None

    def get_parameters(self, camera):
        l_vec = self.pos - camera.pos
        self.r = np.dot(l_vec, camera.view_vec)
        if self.r > 0.0:
            self.k = (camera.r_0 / self.r)
            self.t = self.k * np.dot(camera.screen_vec, l_vec)
            self.angle = np.arccos(self.r / np.linalg.norm(l_vec))
        else:
            self.r = -1.0
            self.angle = np.pi

    def draw(self, screen: pg.Surface, camera: Camera):
        pass


class StickObject(Object):

    def sticks(self, screen, camera):
        pass


class Stick(DrawableObject):

    def __init__(self, pos: np.ndarray[int], z: list, color):
        self.z = z  # z[0] is bottom point and z[1] is top point
        self.color = color
        super().__init__(pos)

    def draw(self, screen: pg.Surface, camera: Camera):
        if self.r > 0:
            h_down = self.z[0] - camera.height
            h_up = self.z[1] - camera.height
            line_down = CENTER + np.array([self.t, - h_down * self.k])
            line_up = CENTER + np.array([self.t, - h_up * self.k])
            # color = self.color
            color = list(map(lambda x: int(x * np.exp(-0.5 * self.r/camera.r_0)), self.color))
            line_width = int(3*camera.r_0 / self.r)
            pg.draw.line(screen, color, line_down, line_up, line_width)


class Wall(StickObject):

    def __init__(self, pos: np.ndarray, vec: np.ndarray, z: list, width: float, color):
        self.pos = pos
        self.vec = vec
        self.z = z
        self.width = width
        self.color = color

    def sticks(self, screen, camera):
        lines_n = 500
        sticks = []
        for pos in np.linspace(self.pos, self.pos + self.width * self.vec, lines_n):
            stick = Stick(np.array(list(map(lambda x: int(x), pos.round()))), self.z, self.color)
            sticks.append(stick)

        return sticks


class Circle(StickObject):

    def __init__(self, pos: np.ndarray, vec: np.ndarray, z_of_center: float, radius: float, color):
        self.pos = pos
        self.vec = vec
        self.z_of_center = z_of_center
        self.radius = radius
        self.color = color

    def sticks(self, screen, camera):
        lines_n = 500
        sticks = []
        for pos in np.linspace(self.pos - self.radius * self.vec, self.pos + self.radius * self.vec, lines_n):
            z = (self.radius**2 - np.linalg.norm(pos - self.pos)**2)**0.5
            stick = Stick(np.array(list(map(lambda x: int(x), pos.round()))),
                          [self.z_of_center - z, self.z_of_center + z], self.color)
            sticks.append(stick)

        return sticks


class Sprite(DrawableObject):

    STEP_OF_ANGLE = 45

    def __init__(self, pos, z: float, path_of_sprite_set, vec, height):
        self.sprite_set = get_sprite_set(path_of_sprite_set, height)
        self.vec = vec
        self.z = z
        super().__init__(pos)

    def draw(self, screen: pg.Surface, camera: Camera):

        reversed_vec = camera.pos - self.pos
        angle = angle_between_two_vectors(reversed_vec, self.vec)
        angle_of_sprite = Sprite.STEP_OF_ANGLE * int(np.floor(0.5 + angle / Sprite.STEP_OF_ANGLE))

        image = self.sprite_set[angle_of_sprite]

        image = pg.transform.scale(image, (image.get_rect().width*self.k, image.get_rect().height*self.k))
        screen.blit(image, image.get_rect(center=CENTER + np.array([self.t, self.k * (self.z - camera.height)])))

