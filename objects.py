import pygame as pg
from locals import *

# TODO: remove screen, camera from args


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


class Camera:
    move_keys = {Key.w: 0.0, Key.a: -np.pi / 2,
                 Key.s: np.pi, Key.d: np.pi / 2}

    def __init__(self, r_0: float = 500.0, l_0: float = 500.0, height: float = 100.0,
                 pos: np.ndarray[int] = np.array([0, 0]), velocity: float = 10.0,
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
                print(type(self.pos[0]))
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


class Object:

    def __init__(self):
        pass

    def update(self):
        pass


class Stick(Object):

    def __init__(self, screen: pg.Surface, camera: Camera, pos: np.ndarray[int], z: list):
        super().__init__()
        self.screen = screen
        self.camera = camera
        self.pos = pos
        self.z = z  # z[0] is bottom point and z[1] is top point

        l_vec = self.pos - self.camera.pos
        self.r = np.dot(l_vec, self.camera.view_vec)
        if self.r > 0.0:
            self.k = (self.camera.r_0 / self.r)
            self.t = self.k * np.dot(self.camera.screen_vec, l_vec)
            self.angle = np.arccos(self.r / np.linalg.norm(l_vec))
        else:
            self.r = 0.0
            self.angle = np.pi

    def draw_3d(self):
        if self.r > 0:
            h_down = self.z[0] - self.camera.height
            h_up = self.z[1] - self.camera.height
            line_down = CENTER + np.array([self.t, - h_down * self.k])
            line_up = CENTER + np.array([self.t, - h_up * self.k])
            color = Color.GREEN
            line_width = 1
            pg.draw.line(self.screen, color, line_down, line_up, line_width)


class Wall(Object):

    def __init__(self, pos: np.ndarray, vec: np.ndarray, z: list, width: float):
        super().__init__()
        self.pos = pos
        self.vec = vec
        self.z = z
        self.width = width

    def sticks(self, screen, camera):
        lines_n = 1000
        sticks = []
        for pos in np.linspace(self.pos, self.pos + self.width * self.vec, lines_n):
            stick = Stick(screen, camera, np.array(list(map(lambda x: int(x), pos.round()))), self.z)
            sticks.append(stick)

        return sticks
