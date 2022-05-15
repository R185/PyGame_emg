import pygame
import os
import sys
import datetime
import time
from PIL import Image, ImageFilter

import menu_scr
from gif_chikens import *
import loading_map
import start_music
import emg1
from menu_scr import first_time


count_UP1 = 0
count_DOWN = 0
count_UP = 0
count_DOWN1 = 0
winner = 0
lose = 0
finish = 0

def game1(map, players, click_red_chicken, click_blue_chicken, emg):
    global finish
    global winner
    # define game variables
    pygame.init()

    lose = 0
    finish = 0
    screen_width = 864
    screen_height = 760
    screen = pygame.display.set_mode((screen_width, screen_height))

    fps = 30

    pygame.display.set_caption('Chicken-Run')

    if map == 1:
        bg = pygame.image.load('data/BG1.png')
    elif map == 2:
        bg = pygame.image.load('data/BG2.png')

    def load_image(name, colorkey=None):
        fullname = os.path.join('data', name)
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            sys.exit()
        image = pygame.image.load(fullname)
        if colorkey is not None:
            image = image.convert()
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        else:
            image = image.convert_alpha()
        return image

    tile_width = tile_height = 50

    gif_chickens()

    up_earth_group = pygame.sprite.Group()
    low_earth_group = pygame.sprite.Group()
    up_barrier_box_group = pygame.sprite.Group()
    low_barrier_box_group = pygame.sprite.Group()
    start_group = pygame.sprite.Group()
    finish_group = pygame.sprite.Group()
    arrows_group = pygame.sprite.Group()
    waters_group = pygame.sprite.Group()
    chick_red_group = pygame.sprite.Group()
    chick_blue_group = pygame.sprite.Group()

    tile_images = {
        'wall': load_image('ground.png'),
        'barrier': pygame.transform.scale(load_image('box.png'), (40, 40)),
        'arrow': pygame.transform.scale(load_image('arrow.png'), (85, 60))
    }

    class UpperEarth(pygame.sprite.Sprite):
        def __init__(self, tile_type, pos_x, pos_y):
            super().__init__(up_earth_group)
            self.image = tile_images[tile_type]
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect().move(
                tile_width * pos_x, tile_height * pos_y)

    class LowerEarth(pygame.sprite.Sprite):
        def __init__(self, tile_type, pos_x, pos_y):
            super().__init__(low_earth_group)
            self.image = tile_images[tile_type]
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect().move(
                tile_width * pos_x, tile_height * pos_y)

    class UpperBarrierBox(pygame.sprite.Sprite):
        def __init__(self, pos_x, pos_y):
            super().__init__(up_barrier_box_group)
            self.image = pygame.transform.scale(load_image('box.png'), (40, 40))
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect().move(
                tile_width * pos_x, tile_height * pos_y + 30)

    class LowerBarrierBox(pygame.sprite.Sprite):
        def __init__(self, pos_x, pos_y):
            super().__init__(low_barrier_box_group)
            self.image = pygame.transform.scale(load_image('box.png'), (40, 40))
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect().move(
                tile_width * pos_x, tile_height * pos_y - 30)

    class Barrier(pygame.sprite.Sprite):
        def __init__(self, tile_types, pos_x, pos_y):
            self.image = tile_images[tile_types]
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect().move(
                tile_width * pos_x, tile_height * pos_y)
            if tile_types == 'water':
                super().__init__(waters_group)
            elif tile_types == 'arrow':
                super().__init__(arrows_group)

    class Finish_line(pygame.sprite.Sprite):
        def __init__(self, tile_type, pos_x, pos_y):
            super().__init__(finish_group)
            self.image = pygame.transform.scale(load_image('Finish-line.png'), (95, 230))
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect().move(
                tile_width * pos_x + 60, tile_height * pos_y)

    class ChickenRed(pygame.sprite.Sprite):
        def __init__(self, sheet, level):
            super().__init__(chick_red_group)
            self.frames = []
            self.image = sheet
            self.x = 0
            self.y = 0
            self.vel = 10
            self.rect = self.image.get_rect()
            if players == 2:
                for y in range(len(level)):
                    for x in range(len(level[y])):
                            if level[y][x] == '$':
                                self.y = y * tile_height
                                self.x = x * tile_width
            else:
                self.y = -100
                self.x = -100

        def update(self):
            global finish
            global winner

            if start == 0:
                self.x += 0.4
            if pygame.sprite.spritecollideany(self, up_barrier_box_group):
                self.x -= 5

            if pygame.sprite.spritecollideany(self, low_barrier_box_group):
                self.x -= 5
            self.rect = self.image.get_rect().move(self.x, self.y)

            if click_red_chicken == 'up':
                draw_chicken_red_up()
            if not pygame.sprite.spritecollideany(self, low_earth_group) and click_red_chicken == 'down':
                if chicken_red.y >= chicken_blue.y or not pygame.sprite.spritecollideany(self,
                                                                                             chick_blue_group) and click_red_chicken == 'down':
                    if not pygame.sprite.spritecollideany(self, low_barrier_box_group) and click_red_chicken == 'down':
                        self.y += self.vel
                    else:
                        self.x += 5
            if not pygame.sprite.spritecollideany(self, up_earth_group) and click_red_chicken == 'up':
                if chicken_red.y <= chicken_blue.y or not pygame.sprite.spritecollideany(self,
                                                                                         chick_blue_group) and click_red_chicken == 'up':
                    if not pygame.sprite.spritecollideany(self, up_barrier_box_group) and click_red_chicken == 'up':
                        self.y -= self.vel
                    else:
                        self.x += 5
            if pygame.sprite.spritecollideany(self, finish_group):
                start_music.fon_music.set_volume(0)
                finish = 1
                if winner == 0:
                    winner = 'chicken_red'
            if pygame.sprite.spritecollideany(self, arrows_group):
                start_music.arrow.play(start_music.arrow_player)
                self.x += 240

    class ChickenBlue(pygame.sprite.Sprite):
        def __init__(self, sheet, level):
            super().__init__(chick_blue_group)
            self.frames = []
            self.image = sheet
            self.x = 0
            self.y = 0
            self.vel = 10
            self.rect = self.image.get_rect()
            for y in range(len(level)):
                for x in range(len(level[y])):
                    if level[y][x] == '@':
                        self.y = y * tile_height
                        self.x = x * tile_width

        def update(self):
            global finish
            global winner
            if start == 0:
                self.x += 0.4
            if pygame.sprite.spritecollideany(self, up_barrier_box_group):
                self.x -= 5

            if pygame.sprite.spritecollideany(self, low_barrier_box_group):
                self.x -= 5
            self.rect = self.image.get_rect().move(self.x, self.y)

            if click_blue_chicken == 'up':
                draw_chicken_blue_up()

            if not pygame.sprite.spritecollideany(self, low_earth_group) and click_blue_chicken == 'down':
                if chicken_blue.y >= chicken_red.y or not pygame.sprite.spritecollideany(self,
                                                                                         chick_red_group) and click_blue_chicken == 'down':
                    if not pygame.sprite.spritecollideany(self, low_barrier_box_group) and click_blue_chicken == 'down':
                        self.y += self.vel
                    else:
                        self.x += 5

            if not pygame.sprite.spritecollideany(self, up_earth_group) and click_blue_chicken == 'up':
                if chicken_blue.y <= chicken_red.y or not pygame.sprite.spritecollideany(self,
                                                                                         chick_red_group) and click_blue_chicken == 'up':
                    if not pygame.sprite.spritecollideany(self, up_barrier_box_group) and click_blue_chicken == 'up':
                        self.y -= self.vel
                    else:
                        self.x += 5

            if pygame.sprite.spritecollideany(self, finish_group):
                start_music.fon_music.set_volume(0)
                finish = 1
                if winner == 0:
                    winner = 'chicken_blue'
            if pygame.sprite.spritecollideany(self, arrows_group):
                start_music.arrow.play(start_music.arrow_player)
                self.x += 240

    class Start_line(pygame.sprite.Sprite):
        def __init__(self, sheet, level):
            super().__init__(start_group)
            self.image = sheet
            self.x = 0
            self.y = 0
            self.vel = 10
            self.rect = self.image.get_rect()
            for y in range(len(level)):
                for x in range(len(level[y])):
                    if level[y][x] == '/':
                        self.y = y * tile_height - 110
                        self.x = x * tile_width - 80

        def update(self):
            self.rect = self.image.get_rect().move(self.x, self.y)

    class Button:
        def __init__(self, x, y, image):
            self.image = image
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.clicked = False

        def draw(self):
            action = False

            # get mouse position
            pos = pygame.mouse.get_pos()

            # check mouseover and clicked conditions
            if self.rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                    action = True
                    self.clicked = True

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            screen.blit(self.image, self.rect)

            return action

    def draw_chicken_red_up():  # motion animation
        global count_UP
        if count_UP == 4:
            count_UP = 0
        chicken_red.image = chicken_red_up_gif[count_UP // 2]
        count_UP += 1

    def draw_chicken_red_down():  # motion animation
        global count_DOWN
        if count_DOWN == 4:
            count_DOWN = 0
        chicken_red.image = chicken_red_down_gif[count_DOWN // 2]
        count_DOWN += 1

    def draw_chicken_blue_up():  # motion animation
        global count_UP1
        if count_UP1 == 4:
            count_UP1 = 0
        chicken_blue.image = chicken_blue_up_gif[count_UP1 // 2]
        count_UP1 += 1

    def draw_chicken_blue_down():  # motion animation
        global count_DOWN1
        if count_DOWN1 == 4:
            count_DOWN1 = 0
        chicken_blue.image = chicken_blue_down_gif[count_DOWN1 // 2]
        count_DOWN1 += 1

    def generate_level(level, c):
        a = 0
        new_player, x, y = None, None, None
        for y in range(len(level)):
            for x in range(len(level[y])):
                if level[y][x] == '#':
                    if a <= 40:
                        UpperEarth('wall', x - c, y)  # upper blocks
                        a += 1
                    else:
                        LowerEarth('wall', x - c, y)  # lower blocks
                elif level[y][x] == '|':
                    Finish_line('finish-line', x - c, y)
                elif level[y][x] == '~':
                    Barrier('water', x - c, y)
                elif level[y][x] == '!':
                    if a <= 40:
                        UpperEarth('wall', x - c, y)
                        UpperBarrierBox(x - c, y)  # upper barriers
                        a += 1
                    else:
                        LowerEarth('wall', x - c, y)
                        LowerBarrierBox(x - c, y)  # lower barriers
                elif level[y][x] == '>':
                    Barrier('arrow', x - c, y)

        # we will return the player, as well as the size of the field in cells
        return new_player, x, y

    level_map = loading_map.load_level('map.txt')
    chicken_red = ChickenRed(pygame.transform.scale(load_image('ChickenRed-down_stay.png'), (20, 30)), level_map)
    chicken_blue = ChickenBlue(pygame.transform.scale(load_image('ChickenBlue-down_stay.png'), (20, 30)), level_map)
    start_line = Start_line(
        pygame.transform.rotate(pygame.transform.scale(load_image('Start-line.png'), (170, 150)), 90),
        level_map)
    chick_red_group.add(chicken_red)
    chick_blue_group.add(chicken_blue)
    start_group.add(start_line)

    map_speed = 10
    start = 1  # start line close
    run = True
    lose = 0
    restart_img = pygame.transform.scale(pygame.image.load('data/restart.png'), (95, 95))
    home_img = pygame.transform.scale(pygame.image.load('data/home.png'), (110, 110))
    restart_button = Button(screen_width // 2 + 30, screen_height // 2 - 80, restart_img)
    home_button = Button(screen_width // 2 - 120, screen_height // 2 - 90, home_img)

    w = 0

    start_music.mixers_music()  # GAME MUSIC

    def in_air_game_over():
        global lose
        global finish
        start_music.hero_in_air.play(start_music.in_air)  # GAME OVER MUSIC
        start_music.fon_music.set_volume(0)
        lose = 1
        finish = 1

    while run:
        clock = pygame.time.Clock()
        clock.tick(fps)
        if finish == 0:

            if players == 2:
                if chicken_red.x < -40 or chicken_red.y <= -40 or chicken_red.y >= 904 and lose == 0:
                    in_air_game_over()  # GAME OVER
                    winner = 'chicken_blue'
                    finish = 1

            if chicken_blue.x < -40 or chicken_blue.y <= -40 or chicken_blue.y >= 904 and lose == 0:
                in_air_game_over()  # GAME OVER
                winner = 'chicken_red'
                finish = 1

            chicken_red.update()
            chicken_blue.update()

            if click_blue_chicken == 'down':
                draw_chicken_blue_down()  # gif blue chicken

            if click_red_chicken == 'down':  # gif red chicken
                draw_chicken_red_down()
            # draw background
            up_earth_group = pygame.sprite.Group()  # upper blocks
            low_earth_group = pygame.sprite.Group()  # lower blocks
            up_barrier_box_group = pygame.sprite.Group()  # upper barriers
            low_barrier_box_group = pygame.sprite.Group()  # lower barriers
            finish_group = pygame.sprite.Group()  # lower barriers
            arrows_group = pygame.sprite.Group()  # lower barriers
            waters_group = pygame.sprite.Group()  # lower barriers
            screen.blit(bg, (0, 0))
            hero, level_x, level_y = generate_level(level_map, map_speed)

            #            update_create_sprites.update()  # UPDATE SPRITES
            up_earth_group.draw(screen)
            up_earth_group.update()
            low_earth_group.draw(screen)
            low_earth_group.update()
            up_barrier_box_group.draw(screen)
            up_barrier_box_group.update()
            low_barrier_box_group.draw(screen)
            low_barrier_box_group.update()
            finish_group.draw(screen)
            finish_group.update()
            chick_red_group.draw(screen)
            chick_red_group.update()
            chick_blue_group.draw(screen)
            chick_blue_group.update()
            arrows_group.draw(screen)
            arrows_group.update()
            waters_group.draw(screen)
            waters_group.update()
        start_group.draw(screen)
        start_group.update()

        if start == 0:  # run after start line
            map_speed += 0.5
            start_line.update()
        from menu_scr import first_time
        second_time = datetime.datetime.now()
        delta = second_time - first_time
        if '03' == str(delta).split(':')[2].split('.')[0]:  # 3 seconds stop
            start = 0  # start line open
            start_line.x = -100
            start_line.y = 0

        if finish == 1:

            restart_button.draw()  # RESTART BUTTON
            home_button.draw()  # HOME BUTTON
            win_baner = pygame.transform.scale(pygame.image.load('data/win_baner.png'), (250, 100))
            screen.blit(win_baner, (310, 80))
            if players == 2:
                if winner == 'chicken_red':
                    flapp = pygame.transform.scale(pygame.image.load('data/ChickenRed-down_stay.png'), (40, 50))
                    screen.blit(flapp, (415, 150))

            if winner == 'chicken_blue':
                flapp = pygame.transform.scale(pygame.image.load('data/ChickenBlue-down_stay.png'), (40, 50))
                screen.blit(flapp, (415, 150))
            if w == 0:
                start_music.win.play(start_music.winner_mus)
                w += 1
            winner = 0
            chicken_red = 0
            chicken_blue = 0
        if emg == 1:
            emg_signal = emg1.ser.read(emg1.ser.in_waiting)
            emg_signal = str(emg_signal)
            print(emg_signal)
            if "1.1" in emg_signal and click_blue_chicken == 'down' and finish == 0 :
                start_music.jump_hero.play(start_music.jump)
                click_blue_chicken = 'up'
            elif "1.0" in emg_signal and click_blue_chicken == 'up' and finish == 0 :
                start_music.jump_hero.play(start_music.jump)
                click_blue_chicken = 'down'
            if players == 2:
                if "2.1" in emg_signal and click_red_chicken == 'down' and finish == 0 :
                    start_music.jump_hero.play(start_music.jump)
                    click_red_chicken = 'up'
                elif "2.0" in emg_signal and click_red_chicken == 'up' and finish == 0 :
                    start_music.jump_hero.play(start_music.jump)
                    click_red_chicken = 'down'

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            key = pygame.key.get_pressed()
            if players == 2:
                if key[pygame.K_w] and click_red_chicken == 'down' and finish == 0 :
                    start_music.jump_hero.play(start_music.jump)
                    click_red_chicken = 'up'
                elif key[pygame.K_s] and click_red_chicken == 'up' and finish == 0 :
                    start_music.jump_hero.play(start_music.jump)
                    click_red_chicken = 'down'
            if key[pygame.K_UP] and click_blue_chicken == 'down' and finish == 0 :
                start_music.jump_hero.play(start_music.jump)
                click_blue_chicken = 'up'
            elif key[pygame.K_DOWN] and click_blue_chicken == 'up' and finish == 0 :
                start_music.jump_hero.play(start_music.jump)
                click_blue_chicken = 'down'

            if event.type == pygame.MOUSEBUTTONDOWN and finish == 1:
                if 562 >= event.pos[0] >= 462 and 300 <= event.pos[1] <= 400:
                    pygame.mixer.stop()
                    finish = 0
                    chick_red_group = pygame.sprite.Group()
                    chick_blue_group = pygame.sprite.Group()
                    level_map = loading_map.load_level('map.txt')
                    chicken_red = ChickenRed(pygame.transform.scale(load_image('ChickenRed-down_stay.png'), (40, 50)),
                                             level_map)
                    chicken_blue = ChickenBlue(
                        pygame.transform.scale(load_image('ChickenBlue-down_stay.png'), (40, 50)),
                        level_map)
                    start_line = Start_line(
                        pygame.transform.rotate(pygame.transform.scale(load_image('Start-line.png'), (170, 150)), 90),
                        level_map)
                    chick_red_group.add(chicken_red)
                    chick_blue_group.add(chicken_blue)
                    start_group.add(start_line)

                    map_speed = 1
                    start = 1  # start line close
                    # run = True
                    lose = 0
                    restart_img = pygame.transform.scale(pygame.image.load('data/restart.png'), (95, 95))
                    home_img = pygame.transform.scale(pygame.image.load('data/home.png'), (110, 110))
                    restart_button = Button(screen_width // 2 + 30, screen_height // 2 - 80, restart_img)
                    home_button = Button(screen_width // 2 - 120, screen_height // 2 - 90, home_img)

                    w = 0
                    menu_scr.first_time = datetime.datetime.now()

                    start_music.mixers_music()  # GAME MUSIC

                    run = True  # RESTART
                elif 462 >= event.pos[0] >= 320 and 300 <= event.pos[1] <= 400:
                    finish = 0
                    chick_red_group = pygame.sprite.Group()
                    chick_blue_group = pygame.sprite.Group()
                    level_map = loading_map.load_level('map.txt')
                    chicken_red = ChickenRed(pygame.transform.scale(load_image('ChickenRed-down_stay.png'), (40, 50)),
                                             level_map)
                    chicken_blue = ChickenBlue(
                        pygame.transform.scale(load_image('ChickenBlue-down_stay.png'), (40, 50)),
                        level_map)
                    start_line = Start_line(
                        pygame.transform.rotate(pygame.transform.scale(load_image('Start-line.png'), (170, 150)), 90),
                        level_map)
                    chick_red_group.add(chicken_red)
                    chick_blue_group.add(chicken_blue)
                    start_group.add(start_line)

                    map_speed = 1
                    start = 1  # start line close
                    lose = 0
                    restart_img = pygame.transform.scale(pygame.image.load('data/restart.png'), (95, 95))
                    home_img = pygame.transform.scale(pygame.image.load('data/home.png'), (110, 110))
                    restart_button = Button(screen_width // 2 + 30, screen_height // 2 - 80, restart_img)
                    home_button = Button(screen_width // 2 - 120, screen_height // 2 - 90, home_img)

                    w = 0
                    start_music.mixers_music()  # GAME MUSIC
                    menu_scr.main()
                    return

                    #             return
        pygame.display.update()
    return
