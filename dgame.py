from random import randrange

import pygame
import math

from pygame import *

from maze_generator import *

class Menu:
    def __init__(self):
        self._option_surfaces = []
        self._callbacks = []
        self._current_option_index = 0

    def append_option(self, option, callback):
        self._option_surfaces.append(pygame.font.SysFont('Arial', 50).render(option, True, (255, 255, 255)))
        self._callbacks.append(callback)

    def switch(self, direction):
        # Не сможем выйти за рамки массива
        self._current_option_index = max(0, min(self._current_option_index + direction, len(self._option_surfaces) - 1))

    def select(self):
        self._callbacks[self._current_option_index]()

    def draw(self, surf, x, y, option_y_padding):
        for i, option in enumerate(self._option_surfaces):
            option_rect = option.get_rect()
            option_rect.topleft = (x, y + i * option_y_padding)
            if i == self._current_option_index:
                draw.rect(surf, (0, 100, 0), option_rect)
            surf.blit(option, option_rect)

menu = Menu()
menu.append_option('Easy', lambda: set_easy())
menu.append_option('Medium', lambda: set_medium())
menu.append_option('Hard', lambda: set_hard())

class Object:
    def __init__(self, type):
        self.type = type
        if type == 'key':
            self.img = pygame.image.load('img/object_key.png').convert_alpha()
        elif type == 'cup':
            self.img = pygame.image.load('img/object_cup.png').convert_alpha()
        elif type == 'bush':
            self.img = pygame.image.load('img/object_bush.png').convert_alpha()
        elif type == 'broken_bush':
            self.img = pygame.image.load('img/object_broken_bush.png').convert_alpha()
        elif type == 'abyss':
            self.img = pygame.image.load('img/abyss.png').convert()
        self.img = pygame.transform.scale(self.img, (TILE - 10, TILE - 10))
        self.rect = self.img.get_rect()
        self.set_pos()

    def broke_bush(self, x, y):
        self.type = 'broken_bush'
        self.img = pygame.image.load('img/object_broken_bush.png').convert_alpha()
        self.img = pygame.transform.scale(self.img, (TILE - 10, TILE - 10))
        self.rect = self.img.get_rect()
        self.rect.topleft = x, y

    #Рандомное размещение картинки
    def set_pos(self):
        self.rect.topleft = randrange(get_cols()) * TILE + 5, randrange(get_rows()) * TILE + 5

    def draw(self):
        game_surface.blit(self.img, self.rect)

def is_collide(x, y):
    tmp_rect = player_rect.move(x, y)
    if tmp_rect.collidelist(walls_collide_list) == -1:
        return False
    return True

def use_object(jump_flag):
    if (score > get_cup_score()):
        event.type = pygame.QUIT
        #gameover
    for object in object_list:
        if player_rect.collidepoint(object.rect.center):
            if object.type == 'bush' and jump_flag == 0:
                x = object.rect.topleft[0]
                y = object.rect.topleft[1]
                object.broke_bush(x, y)
                print("Куст сломан")
                return 'bush'
            elif object.type == 'abyss':
                return 'abyss'
            elif object.type == 'key':
                object.set_pos()
                return 'key'
    return False

# Проверка окончания игры, создание новой игры
def game_over():
    global time, score, record, FPS
    if score == get_cup_score():
        return 'Win'
    if get_player_health() == 0:
        return 'Health'
    if time < 0:
        pygame.time.wait(700)
        player_rect.center = TILE // 2, TILE // 2
        [object.set_pos() for object in object_list]
        set_record(record, score)
        record = get_record()
        time, score, FPS = 60, 0, 60
        return 'Time'

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

FPS = 50
pygame.init()
surface = pygame.display.set_mode((1302, 502))
clock = pygame.time.Clock()

# Картинки
bg_game = pygame.image.load('img/bg_1.jpg').convert()
bg = pygame.image.load('img/bg_main.jpg').convert()
environment_img = pygame.image.load('img/dark.png').convert()
environment_img.set_alpha(50)
dark_img = pygame.image.load('img/dark.png').convert()

player_speed = 4

font = pygame.font.SysFont('Impact', 150)

while True:
    if game_start == 0:
        surface.fill((0, 0, 0))
        for e in event.get():
            if e.type == QUIT:
                quit()
            elif e.type == KEYDOWN:
                if e.key == K_w:
                    print('w')
                    menu.switch(-1)
                if e.key == K_s:
                    print('s')
                    menu.switch(1)
                if e.key == K_SPACE:
                    menu.select()
                    maze = generate_maze()
                    surface = pygame.display.set_mode(get_res())
                    game_surface = pygame.Surface(get_res())
                    player_img = pygame.image.load('img/player.png').convert_alpha()
                    player_img = pygame.transform.scale(player_img, (
                    (TILE - 2 * maze[0].thickness) + 1, (TILE - 2 * maze[0].thickness) + 1))

                    player_jump_left_img = pygame.image.load('img/player-jump-left.png').convert_alpha()
                    player_jump_left_img = pygame.transform.scale(player_jump_left_img, (
                    TILE - 2 * maze[0].thickness, TILE - 2 * maze[0].thickness))
                    player_jump_right_img = pygame.image.load('img/player-jump-right.png').convert_alpha()
                    player_jump_right_img = pygame.transform.scale(player_jump_right_img, (
                    TILE - 2 * maze[0].thickness, TILE - 2 * maze[0].thickness))
                    player_jump_top_img = pygame.image.load('img/player-jump-top.png').convert_alpha()
                    player_jump_top_img = pygame.transform.scale(player_jump_top_img, (
                    TILE - 2 * maze[0].thickness, TILE - 2 * maze[0].thickness))
                    player_jump_bottom_img = pygame.image.load('img/player-jump-bottom.png').convert_alpha()
                    player_jump_bottom_img = pygame.transform.scale(player_jump_bottom_img, (
                    TILE - 2 * maze[0].thickness, TILE - 2 * maze[0].thickness))

                    player_move_left0_img = pygame.image.load('img/player-move-left0.png').convert_alpha()
                    player_move_left0_img = pygame.transform.scale(player_move_left0_img, (
                    TILE - 2 * maze[0].thickness, TILE - 2 * maze[0].thickness))
                    player_move_left1_img = pygame.image.load('img/player-move-left1.png').convert_alpha()
                    player_move_left1_img = pygame.transform.scale(player_move_left1_img, (
                    TILE - 2 * maze[0].thickness, TILE - 2 * maze[0].thickness))
                    player_move_left2_img = pygame.image.load('img/player-move-left2.png').convert_alpha()
                    player_move_left2_img = pygame.transform.scale(player_move_left2_img, (
                    TILE - 2 * maze[0].thickness, TILE - 2 * maze[0].thickness))

                    player_move_right0_img = pygame.image.load('img/player-move-right0.png').convert_alpha()
                    player_move_right0_img = pygame.transform.scale(player_move_right0_img, (
                    TILE - 2 * maze[0].thickness, TILE - 2 * maze[0].thickness))
                    player_move_right1_img = pygame.image.load('img/player-move-right1.png').convert_alpha()
                    player_move_right1_img = pygame.transform.scale(player_move_right1_img, (
                    TILE - 2 * maze[0].thickness, TILE - 2 * maze[0].thickness))
                    player_move_right2_img = pygame.image.load('img/player-move-right2.png').convert_alpha()
                    player_move_right2_img = pygame.transform.scale(player_move_right2_img, (
                    TILE - 2 * maze[0].thickness, TILE - 2 * maze[0].thickness))

                    player_move_top_img = pygame.image.load('img/player-move-top.png').convert_alpha()
                    player_move_top_img = pygame.transform.scale(player_move_top_img, (
                    TILE - 2 * maze[0].thickness, TILE - 2 * maze[0].thickness))

                    player_move_bottom0_img = pygame.image.load('img/player-move-bottom0.png').convert_alpha()
                    player_move_bottom0_img = pygame.transform.scale(player_move_bottom0_img, (
                    TILE - 2 * maze[0].thickness, TILE - 2 * maze[0].thickness))
                    player_move_bottom1_img = pygame.image.load('img/player-move-bottom1.png').convert_alpha()
                    player_move_bottom1_img = pygame.transform.scale(player_move_bottom1_img, (
                    TILE - 2 * maze[0].thickness, TILE - 2 * maze[0].thickness))

                    player_rect = player_img.get_rect()
                    player_rect.center = TILE // 2, TILE // 2

                    directions = {'a': (-player_speed, 0), 'd': (player_speed, 0), 'w': (0, -player_speed),
                                  's': (0, player_speed)}
                    keys = {'a': pygame.K_a, 'd': pygame.K_d, 'w': pygame.K_w, 's': pygame.K_s}
                    direction = (0, 0)

                    player_anim_right_count = 0
                    player_anim_left_count = 0
                    player_anim_jump_count = 0
                    player_anim_bottom_count = 0
                    player_anim_bottom_count_real = 0
                    player_anim_turn_count = 0

                    walk_right = [player_move_right0_img, player_move_right1_img, player_move_right2_img]
                    walk_left = [player_move_left0_img, player_move_left1_img, player_move_left2_img]
                    walk_bottom = [player_move_bottom0_img, player_move_bottom1_img]

                    # turn_left =
                    # turn_right =

                    jump_left = [player_jump_left_img, player_jump_left_img, player_jump_left_img, player_jump_left_img,
                                 player_jump_left_img,
                                 player_jump_left_img, player_jump_left_img, player_jump_left_img, player_jump_left_img,
                                 player_jump_left_img,
                                 player_jump_left_img, player_jump_left_img, player_jump_left_img, player_jump_left_img,
                                 player_jump_left_img,
                                 player_jump_left_img, player_jump_left_img, player_jump_left_img, player_jump_left_img,
                                 player_jump_left_img]
                    jump_right = [player_jump_right_img, player_jump_right_img, player_jump_right_img,
                                  player_jump_right_img, player_jump_right_img,
                                  player_jump_right_img, player_jump_right_img, player_jump_right_img,
                                  player_jump_right_img, player_jump_right_img,
                                  player_jump_right_img, player_jump_right_img, player_jump_right_img,
                                  player_jump_right_img, player_jump_right_img,
                                  player_jump_right_img, player_jump_right_img, player_jump_right_img,
                                  player_jump_right_img, player_jump_right_img]
                    jump_top = [player_jump_top_img, player_jump_top_img, player_jump_top_img, player_jump_top_img,
                                player_jump_top_img,
                                player_jump_top_img, player_jump_top_img, player_jump_top_img, player_jump_top_img,
                                player_jump_top_img,
                                player_jump_top_img, player_jump_top_img, player_jump_top_img, player_jump_top_img,
                                player_jump_top_img,
                                player_jump_top_img, player_jump_top_img, player_jump_top_img, player_jump_top_img,
                                player_jump_top_img,
                                ]
                    jump_bottom = [player_jump_bottom_img, player_jump_bottom_img, player_jump_bottom_img,
                                   player_jump_bottom_img, player_jump_bottom_img,
                                   player_jump_bottom_img, player_jump_bottom_img, player_jump_bottom_img,
                                   player_jump_bottom_img, player_jump_bottom_img,
                                   player_jump_bottom_img, player_jump_bottom_img, player_jump_bottom_img,
                                   player_jump_bottom_img, player_jump_bottom_img,
                                   player_jump_bottom_img, player_jump_bottom_img, player_jump_bottom_img,
                                   player_jump_bottom_img, player_jump_bottom_img]

                    # trophy settings
                    if get_complexity() == 'Easy':
                        object_list = [Object('key'), Object('key'), Object('key'), Object('bush'), Object('bush'), Object('abyss')]
                    elif get_complexity() == 'Medium':
                        object_list = [Object('key'), Object('key'), Object('key'), Object('bush'), Object('bush'),
                                       Object('bush'),  Object('abyss'), Object('abyss')]
                    elif get_complexity() == 'Hard':
                        object_list = [Object('key'), Object('key'), Object('key'), Object('bush'), Object('bush'),
                                       Object('bush'), Object('bush'), Object('abyss'), Object('abyss'),
                                       Object('abyss'), Object('abyss')]

                    # collision list
                    walls_collide_list = sum([cell.get_rects() for cell in maze], [])

                    # timer, score, record
                    pygame.time.set_timer(pygame.USEREVENT, 1000)
                    time = 60
                    score = 0
                    # cup_score = 5
                    record = get_record()
                    flag_cup = 0
                    jump_flag = 0
                    game_start = 1
        surface.fill((0, 0, 0))
        menu.draw(surface, 470, 100, 75)
    elif game_start == 1:
        surface.blit(bg, (get_width(), 0))
        surface.blit(game_surface, (0, 0))
        game_surface.blit(bg_game, (0, 0))

        if player_anim_right_count >= 2:
            player_anim_right_count = 0
        else:
            player_anim_right_count += 1

        if player_anim_bottom_count_real >= 1:
            player_anim_bottom_count_real = 0
        else:
            player_anim_bottom_count_real += 0.15

        player_anim_bottom_count = round(player_anim_bottom_count_real)

        if player_anim_left_count >= 2:
            player_anim_left_count = 0
        else:
            player_anim_left_count += 1

        if jump_flag == 1:
            if player_anim_jump_count >= 19:
                player_anim_jump_count = 0
                jump_flag = 0
            else:
                player_anim_jump_count += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.USEREVENT:
                time -= 1

        # draw maze
        [cell.draw(game_surface) for cell in maze]

        if use_object(jump_flag) == 'bush':
            FPS -= 5
            damage_player()
            print(get_player_health())
        if use_object(jump_flag) == 'key':
            FPS += 10
            score += 1
            if (score >= cup_score and flag_cup != 1):
                flag_cup = 1
                if get_complexity() == 'Easy':
                    object_list = [Object('bush'), Object('bush'), Object('abyss'), Object('cup')]
                elif get_complexity() == 'Medium':
                    object_list = [Object('bush'), Object('bush'), Object('bush'), Object('bush'), Object('abyss'), Object('abyss'), Object('cup')]
                elif get_complexity() == 'Hard':
                    object_list = [Object('abyss'), Object('abyss'), Object('abyss'), Object('abyss'),
                                   Object('abyss'), Object('abyss'), Object('abyss'), Object('abyss'),
                                   Object('abyss'), Object('abyss'), Object('abyss'), Object('abyss'),
                                   Object('abyss'), Object('abyss'), Object('abyss'), Object('abyss'), Object('cup')]
        if (use_object(jump_flag) == 'abyss') and (jump_flag == 0):
            player_health = 0
            print("You lose")
        game_over()

        # draw trophy
        [object.draw() for object in object_list]

        pressed_key = pygame.key.get_pressed()
        for key, key_value in keys.items():
            if (pressed_key[K_SPACE] and not is_collide(*directions[key])):
                jump_flag = 1
            elif (pressed_key[key_value] and not is_collide(*directions[key])):
                direction = directions[key]
                break
        if not is_collide(*direction):
            player_rect.move_ip(direction)
            if jump_flag == 1 and direction == (-player_speed, 0):
                game_surface.blit(jump_left[player_anim_jump_count], player_rect)
            elif jump_flag == 1 and direction == (player_speed, 0):
                game_surface.blit(jump_right[player_anim_jump_count], player_rect)
            elif jump_flag == 1 and direction == (0, player_speed):
                game_surface.blit(jump_bottom[player_anim_jump_count], player_rect)
            elif jump_flag == 1 and direction == (0, -player_speed):
                game_surface.blit(jump_top[player_anim_jump_count], player_rect)
            elif direction == (-player_speed, 0):
                game_surface.blit(walk_left[player_anim_left_count], player_rect)
            elif direction == (player_speed, 0):
                game_surface.blit(walk_right[player_anim_right_count], player_rect)
            elif direction == (0, -player_speed):
                game_surface.blit(player_move_top_img, player_rect)
            elif direction == (0, player_speed):
                game_surface.blit(walk_bottom[player_anim_bottom_count], player_rect)
        elif jump_flag == 1:
            if is_collide(-player_speed, 0):
                if (not is_collide(player_speed, 0)) and direction == (player_speed, 0):
                    game_surface.blit(jump_right[player_anim_jump_count], player_rect)
                if (not is_collide(0, player_speed)) and direction == (0, player_speed):
                    game_surface.blit(jump_bottom[player_anim_jump_count], player_rect)
                if (not is_collide(0, -player_speed)) and direction == (0, -player_speed):
                    game_surface.blit(jump_top[player_anim_jump_count], player_rect)
                elif direction == (-player_speed, 0):
                    game_surface.blit(jump_left[player_anim_jump_count], player_rect)
            if is_collide(player_speed, 0):
                if (not is_collide(-player_speed, 0)) and direction == (-player_speed, 0):
                    game_surface.blit(jump_left[player_anim_jump_count], player_rect)
                if (not is_collide(0, player_speed)) and direction == (0, player_speed):
                    game_surface.blit(jump_bottom[player_anim_jump_count], player_rect)
                if (not is_collide(0, -player_speed)) and direction == (0, -player_speed):
                    game_surface.blit(jump_top[player_anim_jump_count], player_rect)
                elif direction == (player_speed, 0):
                    game_surface.blit(jump_right[player_anim_jump_count], player_rect)
            if is_collide(0, player_speed):
                if (not is_collide(-player_speed, 0)) and direction == (-player_speed, 0):
                    game_surface.blit(jump_left[player_anim_jump_count], player_rect)
                if (not is_collide(player_speed, 0)) and direction == (player_speed, 0):
                    game_surface.blit(jump_right[player_anim_jump_count], player_rect)
                if (not is_collide(0, -player_speed)) and direction == (0, -player_speed):
                    game_surface.blit(jump_top[player_anim_jump_count], player_rect)
                elif direction == (0, player_speed):
                    game_surface.blit(jump_bottom[player_anim_jump_count], player_rect)
            if is_collide(0, -player_speed):
                if (not is_collide(-player_speed, 0)) and direction == (-player_speed, 0):
                    game_surface.blit(jump_left[player_anim_jump_count], player_rect)
                if (not is_collide(player_speed, 0)) and direction == (player_speed, 0):
                    game_surface.blit(jump_right[player_anim_jump_count], player_rect)
                if (not is_collide(0, player_speed)) and direction == (0, player_speed):
                    game_surface.blit(jump_bottom[player_anim_jump_count], player_rect)
                elif direction == (0, -player_speed):
                    game_surface.blit(jump_top[player_anim_jump_count], player_rect)
        else:
            game_surface.blit(player_img, player_rect)

        if direction == (0, 0):
            game_surface.blit(player_img, player_rect)

        # Рисуем игрока и темноту вокруг него
        game_surface.blit(environment_img, (player_rect.topleft[0] - 100, player_rect.topleft[1] - 70))
        if player_rect.topleft[1] <= 70:
            scale_img_topy = 0
        else:
            scale_img_topy = player_rect.topleft[1] - 70
        dark_img_top = pygame.transform.scale(dark_img, (get_width(), scale_img_topy))

        if player_rect.topleft[0] <= 100:
            scale_img_leftx = 0
        else:
            scale_img_leftx = player_rect.topleft[0] - 100
        dark_img_left = pygame.transform.scale(dark_img, (scale_img_leftx, get_height()))

        dark_image_right = pygame.transform.scale(dark_img, (get_width(), get_height()))
        dark_image_bottom = pygame.transform.scale(dark_img, (get_width(), get_height()))

        #game_surface.blit(dark_img_top, (0, 0))
        #game_surface.blit(dark_img_left, (0, 0))
        #game_surface.blit(dark_image_right, (player_rect.topright[0] + get_right_indent(), 0))
        #game_surface.blit(dark_image_right, (0, player_rect.bottomright[1] + get_bottom_indent()))

        # draw stats
        surface.blit(font.render(f'{time}', True, pygame.Color('cyan')), (get_width() + 70, (get_height() / 2) - 100))

    pygame.display.flip()
    clock.tick(FPS)
