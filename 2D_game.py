import pygame
from pygame import *

from maze_generator import *

#ARIAL_50 = pygame.font.SysFont('arial', 50)

#class Menu:
    #def __init__(self):
        #self._option_surfaces = []
        #self._callbacks = []
        #self._current_option_index = 0

    #def append_option(self, option, callback):
        #self._option_surfaces.append(ARIAL_50.render(option, True, (255, 255, 255)))
        #self._callbacks.append(callback)

    #def switch(self, direction):
        # Не сможем выйти за рамки массива
        #self._current_option_index = max(0, min(self._current_option_index + direction, len(self._option_surfaces) - 1))

    #def select(self):
        #self._callbacks[self._current_option_index]()

    #def draw(self, surf, x, y, option_y_padding):
        #for i, option in enumerate(self._option_surfaces):
            #option_rect = option.get_rect()
            #option_rect.topleft = {x, y + i * option_y_padding}
            #if i == self._current_option_index:
                #draw.rect(surf, (0, 100, 0), option_rect)
            #surf.blit(option, option_rect)

#menu = Menu()
#menu.append_option('Easy', lambda: print("Easy"))
#menu.append_option('Medium', lambda: print("Medium"))
#menu.append_option('Hard', lambda: print("Hard"))

# Здесь будет класс вещей, которые нужно получить
class Trophy:
    #Картинка и её ужимание, прямоугольник, полученный с помощью стандартного метода get_rect()
    #Вызов метода размещения картинки
    def __init__(self, type):
        self.type = type
        if type == 'key':
            self.img = pygame.image.load('img/trophy_key.png').convert_alpha()
        elif type == 'cup':
            self.img = pygame.image.load('img/trophy_cup.png').convert_alpha()
        #self.img = pygame.image.load('img/trophy_key.png').convert_alpha()
        self.img = pygame.transform.scale(self.img, (TILE - 10, TILE - 10))
        self.rect = self.img.get_rect()
        self.set_pos()

    #Рандомное размещение картинки
    def set_pos(self):
        self.rect.topleft = randrange(cols) * TILE + 5, randrange(rows) * TILE + 5

    #Рисуем трофей
    def draw(self):
        game_surface.blit(self.img, self.rect)

# Метод, проверяющий коллизию с трофеями и со стенами
def is_collide(x, y):
    tmp_rect = player_rect.move(x, y)
    if tmp_rect.collidelist(walls_collide_list) == -1:
        return False
    return True

# Метод, проверяющий использование трофея и создающий новый трофей
def use_trophy():
    if (score > cup_score):
        event.type = pygame.QUIT
        #gameover
    for trophy in trophy_list:
        if player_rect.collidepoint(trophy.rect.center):
            trophy.set_pos()
            return True
    return False

# Создание новой игры после окончания старой
def game_over():
    global time, score, record, FPS
    if time < 0:
        pygame.time.wait(700)
        player_rect.center = TILE // 2, TILE // 2
        [trophy.set_pos() for trophy in trophy_list]
        set_record(record, score)
        record = get_record()
        time, score, FPS = 60, 0, 60


def get_record():
    try:
        with open('record') as f:
            return f.readline()
    except FileNotFoundError:
        with open('record', 'w') as f:
            f.write('0')
            return 0


def set_record(record, score):
    rec = max(int(record), score)
    with open('record', 'w') as f:
        f.write(str(rec))


FPS = 60
pygame.init()
game_surface = pygame.Surface(RES)
surface = pygame.display.set_mode((WIDTH + 300, HEIGHT))
clock = pygame.time.Clock()

# Картинки
bg_game = pygame.image.load('img/bg_1.jpg').convert()
bg = pygame.image.load('img/bg_main.jpg').convert()
environment_img = pygame.image.load('img/dark.png').convert()
environment_img.set_alpha(100)
dark_img = pygame.image.load('img/dark.png').convert()

# get maze
maze = generate_maze()

#print(get_walls(maze, 'top'))

# player settings
player_speed = 5
player_img = pygame.image.load('img/player.png').convert_alpha()
player_img = pygame.transform.scale(player_img, (TILE - 2 * maze[0].thickness, TILE - 2 * maze[0].thickness))
#player_jump_img = pygame.image.load('img/playerjump.png').convert_alpha()
#player_jump_img = pygame.transform.scale(player_jump_img, (TILE - 2 * maze[0].thickness, TILE - 2 * maze[0].thickness))
player_rect = player_img.get_rect()
player_rect.center = TILE // 2, TILE // 2
directions = {'a': (-player_speed, 0), 'd': (player_speed, 0), 'w': (0, -player_speed), 's': (0, player_speed)}
keys = {'a': pygame.K_a, 'd': pygame.K_d, 'w': pygame.K_w, 's': pygame.K_s,} #'space': pygame.K_SPACE}
direction = (0, 0)

# trophy settings
trophy_list = [Trophy('key') for i in range(3)]

# collision list
walls_collide_list = sum([cell.get_rects() for cell in maze], [])

# timer, score, record
pygame.time.set_timer(pygame.USEREVENT, 1000)
time = 60
score = 0
cup_score = 1
record = get_record()
flag_cup = 0
flag_space = 0

# fonts
font = pygame.font.SysFont('Impact', 150)
text_font = pygame.font.SysFont('Impact', 80)
#ARIAL_50 = pygame.font.SysFont('Arial', 50)

while True:
    surface.blit(bg, (WIDTH, 0))
    surface.blit(game_surface, (0, 0))
    game_surface.blit(bg_game, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.USEREVENT:
            time -= 1

    #menu.draw(game_surface, 100, 100, 75)

    # controls and movement
    pressed_key = pygame.key.get_pressed()
    for key, key_value in keys.items():
        #if (pressed_key[key_value] == 'space'):
            #flag_space = 1
            #jump()
            #flag_space != 1 and ^
        if (key_value != 'space' and pressed_key[key_value] and not is_collide(*directions[key])):
            direction = directions[key]
            break
    if not is_collide(*direction):
        player_rect.move_ip(direction)

    # draw maze
    [cell.draw(game_surface) for cell in maze]

    # gameplay
    if use_trophy():
        FPS += 10
        score += 1
        if (score >= cup_score and flag_cup != 1):
            flag = 1
            trophy_list = [Trophy('cup') for i in range(1)]
    game_over()

    # draw trophy
    [trophy.draw() for trophy in trophy_list]

    # Рисуем игрока и темноту вокруг него
    game_surface.blit(environment_img, (player_rect.topleft[0] - 100, player_rect.topleft[1] - 70))
    if player_rect.topleft[1] <= 70:
        scale_img_topy = 0
    else:
        scale_img_topy = player_rect.topleft[1] - 70
    dark_img_top = pygame.transform.scale(dark_img, (WIDTH, scale_img_topy))

    if player_rect.topleft[0] <= 100:
        scale_img_leftx = 0
    else:
        scale_img_leftx = player_rect.topleft[0] - 100
    dark_img_left = pygame.transform.scale(dark_img, (scale_img_leftx, HEIGHT))

    dark_image_right = pygame.transform.scale(dark_img, (WIDTH, HEIGHT))
    dark_image_bottom = pygame.transform.scale(dark_img, (WIDTH, HEIGHT))

    game_surface.blit(dark_img_top, (0, 0))
    game_surface.blit(dark_img_left, (0, 0))
    game_surface.blit(dark_image_right, (player_rect.topright[0] + 50, 0))
    game_surface.blit(dark_image_right, (0, player_rect.bottomright[1] + 30))

    if (flag_space != 1):
        game_surface.blit(player_img, player_rect)

    # draw stats
    surface.blit(text_font.render('TIME', True, pygame.Color('cyan'), True), (WIDTH + 70, 30))
    surface.blit(font.render(f'{time}', True, pygame.Color('cyan')), (WIDTH + 70, 130))
    surface.blit(text_font.render('score:', True, pygame.Color('forestgreen'), True), (WIDTH + 50, 350))
    surface.blit(font.render(f'{score}', True, pygame.Color('forestgreen')), (WIDTH + 70, 430))
    surface.blit(text_font.render('record:', True, pygame.Color('magenta'), True), (WIDTH + 30, 620))
    surface.blit(font.render(f'{record}', True, pygame.Color('magenta')), (WIDTH + 70, 700))

    # print(clock.get_fps())
    pygame.display.flip()
    clock.tick(FPS)
