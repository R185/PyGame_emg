import pygame
import os
import sys

chicken_red_up_gif = []
chicken_red_down_gif = []
chicken_blue_up_gif = []
chicken_blue_down_gif = []


def gif_chickens():
    # ChickenRed up
    chicken_red_up_stay = pygame.transform.scale(load_image('ChickenRed-up_stay.png'), (40, 50))  # motion animation
    chicken_red_up_run = pygame.transform.scale(load_image('ChickenRed-up_run.png'), (40, 50))  # motion animation
    chicken_red_up_gif.append(chicken_red_up_stay)
    chicken_red_up_gif.append(chicken_red_up_run)

    # ChickenRed down
    chicken_red_down_stay = pygame.transform.scale(load_image('ChickenRed-down_stay.png'), (40, 50))  # motion animation
    chicken_red_down_run = pygame.transform.scale(load_image('ChickenRed-down_run.png'), (40, 50))  # motion animation
    chicken_red_down_gif.append(chicken_red_down_stay)
    chicken_red_down_gif.append(chicken_red_down_run)

    # ChickenBlue up
    chicken_blue_up_stay = pygame.transform.scale(load_image('ChickenBlue-up_stay.png'), (40, 50))  # motion animation
    chicken_blue_up_run = pygame.transform.scale(load_image('ChickenBlue-up_run.png'), (40, 50))  # motion animation
    chicken_blue_up_gif.append(chicken_blue_up_stay)
    chicken_blue_up_gif.append(chicken_blue_up_run)

    # ChickenBlue down
    chicken_blue_down_stay = pygame.transform.scale(load_image('ChickenBlue-down_stay.png'), (40, 50))  # motion animation
    chicken_blue_down_run = pygame.transform.scale(load_image('ChickenBlue-down_run.png'), (40, 50))  # motion animation
    chicken_blue_down_gif.append(chicken_blue_down_stay)
    chicken_blue_down_gif.append(chicken_blue_down_run)


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

