import pygame as pg
from locals import *
from sprites import *
from sys import getsizeof

# TODO: fix 3D color
# TODO: fix gaps in walls
# TODO: make collisions
# TODO: calculate number of sticks


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


class Line2D:

    def __init__(self, pos1, pos2):
        self.pos1 = pos1
        self.pos2 = pos2
        self.vec = pos2 - pos1
        self.length = np.linalg.norm(self.vec)
        self.vec = self.vec / np.linalg.norm(self.vec)
        self.perpendicular_vec = rotated(self.vec, np.pi/2)

    def point_collides(self, pos, collision_distance: float = 30.0):
        vector1 = pos - self.pos1
        vector2 = pos - self.pos2
        vector_1_len = np.linalg.norm(vector1)
        vector_2_len = np.linalg.norm(vector2)
        if vector_1_len <= collision_distance:
            return vector1 / vector_1_len
        elif vector_2_len <= collision_distance:
            return vector2 / vector_2_len
        elif abs(np.dot(vector1, self.perpendicular_vec)) <= collision_distance and\
                0 <= np.dot(vector1, self.vec) <= self.length:
            return self.perpendicular_vec
        else:
            return None


class Camera:
    move_keys = {Key.w: 0.0, Key.a: -np.pi / 2,
                 Key.s: np.pi, Key.d: np.pi / 2}

    def __init__(self, r_0: float = 1000.0, l_0: float = 1000.0, height: float = 100.0,
                 pos: np.ndarray[int] = np.array([0, 0]), velocity: float = 12.0,
                 view_vector: np.ndarray = np.array([1.0, 0.0])):
        self.r_0 = r_0
        self.l_0 = l_0
        self.height = height
        self.pos = pos
        self.velocity_value = velocity
        self.view_vec = view_vector
        self.velocity_vec = self.view_vec * self.velocity_value
        self.screen_vec = rotated(self.view_vec, np.pi / 2)
        self.angle_of_vision = np.arctan(self.l_0 / self.r_0)

    def move(self, velocity):
        deviation = np.array(list(map(lambda x: int(x), velocity.round())))
        self.pos += deviation

    def rotate(self):
        angle_velocity = 0.001
        self.view_vec = rotated(self.view_vec, pg.mouse.get_rel()[0] * angle_velocity)
        pg.mouse.set_pos(CENTER)
        self.screen_vec = rotated(self.view_vec, np.pi / 2)

    def update(self, objects):
        velocity = np.array([0.0, 0.0])
        keys_pressed = pg.key.get_pressed()
        for key in self.move_keys.keys():
            if keys_pressed[key]:
                velocity += self.velocity_value * rotated(self.view_vec, Camera.move_keys[key])
        print(velocity)
        if np.linalg.norm(velocity) > 1.0:
            velocity = velocity * (self.velocity_value / np.linalg.norm(velocity))
        self.move(velocity)

        motion_possible = True
        perp_block_lines = []
        for obj in objects:
            perp_block_line = obj.line.point_collides(self.pos)
            if perp_block_line is not None:
                perp_block_lines.append(perp_block_line)
                motion_possible = False

        if not motion_possible:
            possible_velocity = velocity.copy()
            for perp in perp_block_lines:
                possible_velocity -= perp * np.dot(perp, possible_velocity)
                print(possible_velocity)
            self.move(- (velocity - possible_velocity))
        self.rotate()
        print()


class Object:

    def update(self, camera: Camera):
        pass


class DrawableObject(Object):

    MINIMAL_DRAWING_DISTANCE = 10.0

    def __init__(self, pos):
        self.pos = pos
        self.k = None
        self.t = None
        self.angle = None
        self.r = None

    def get_parameters(self, camera):
        l_vec = self.pos - camera.pos
        self.r = np.dot(l_vec, camera.view_vec)
        if self.r > DrawableObject.MINIMAL_DRAWING_DISTANCE:
            self.k = (camera.r_0 / self.r)
        else:
            self.k = - (camera.r_0 / self.r)
            self.angle = np.pi
        self.t = self.k * np.dot(camera.screen_vec, l_vec)
        self.angle = np.arccos(self.r / np.linalg.norm(l_vec))

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
        if self.r > 0.0:
            h_down = self.z[0] - camera.height
            h_up = self.z[1] - camera.height
            line_down = CENTER + np.array([self.t, - h_down * self.k])
            line_up = CENTER + np.array([self.t, - h_up * self.k])

            color = list(map(lambda x: int(x * np.exp(-0.5 * self.r/camera.r_0)), self.color))
            line_width = int(10*camera.r_0 / self.r)
            pg.draw.line(screen, color, line_down, line_up, line_width)


class Wall(StickObject):

    def __init__(self, pos: np.ndarray, vec: np.ndarray, z: list, width: float, color):
        self.pos = pos
        self.vec = vec
        self.z = z
        self.width = width
        self.color = color

        self.line = Line2D(self.pos, self.pos + self.vec * width)

    def sticks(self, screen, camera):
        lines_n = 50
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

        self.line = Line2D(self.pos - self.vec * self.radius, self.pos + self.vec * self.radius)

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

        self.image = None
        self.line = Line2D(self.pos, self.pos)

    def update(self, camera: Camera):
        self.get_parameters(camera)
        if self.r > DrawableObject.MINIMAL_DRAWING_DISTANCE:
            reversed_vec = camera.pos - self.pos
            angle = angle_between_two_vectors(reversed_vec, self.vec)
            angle_of_sprite = Sprite.STEP_OF_ANGLE * int(np.floor(0.5 + angle / Sprite.STEP_OF_ANGLE))

            original_image = self.sprite_set[angle_of_sprite]

            self.image = pg.transform.scale(original_image, (original_image.get_rect().width*self.k,
                                                             original_image.get_rect().height*self.k))

            half_width_vec = camera.screen_vec * original_image.get_rect().width / 2
            self.line = Line2D(self.pos - half_width_vec,
                               self.pos + half_width_vec)

    def draw(self, screen: pg.Surface, camera: Camera):
        screen.blit(self.image,
                    self.image.get_rect(center=CENTER + np.array([self.t, self.k * (self.z - camera.height)])))
