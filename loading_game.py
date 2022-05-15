import pygame
import os
import sys
from game_settings import screen, clock
start_music = pygame.mixer.Sound("music/Start_music.mp3")


def terminate():
    pygame.quit()
    sys.exit()


def loading():
    loading_fons = []
    loading = 0
    loading_time = 0
    fon1 = pygame.transform.scale(load_image('Loading1.png'), (864, 760))
    loading_fons.append(fon1)
    fon2 = pygame.transform.scale(load_image('Loading2.png'), (864, 760))
    loading_fons.append(fon2)
    while loading_time < 40:
        screen.blit(loading_fons[loading], (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        pygame.display.flip()
        if loading <= 1:
            clock.tick(10)
            loading += 1
        if loading == 2:
            loading = 0
        loading_time += 1


def start_screen():
    start_music.play()
    start_music.set_volume(0.3)
    loading_use = 0
    count_fon = 0
    start_fons = []
    fon0 = pygame.transform.scale(load_image('START1.png'), (864, 760))
    start_fons.append(fon0)
    fon2 = pygame.transform.scale(load_image('Chicken_anim_fon1.png'), (864, 760))
    start_fons.append(fon2)
    fon3 = pygame.transform.scale(load_image('Chicken_anim_fon2.png'), (864, 760))
    start_fons.append(fon3)
    fon4 = pygame.transform.scale(load_image('Chicken_anim_fon3.png'), (864, 760))
    start_fons.append(fon4)
    fon5 = pygame.transform.scale(load_image('Chicken_anim_fon4.png'), (864, 760))
    start_fons.append(fon5)

    while True:
        screen.blit(start_fons[count_fon], (0, 0))
        for event in pygame.event.get():
            if count_fon > 1:
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    return
        pygame.display.flip()
        if count_fon <= 1:
            clock.tick(0.5)
            count_fon += 1
        if loading_use < 1:
            clock.tick(0.5)
            loading()
            loading_use += 1
        if count_fon > 1:
            clock.tick(2)
            count_fon += 1
        if count_fon > 4:
            count_fon = 2


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
