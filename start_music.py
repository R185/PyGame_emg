import pygame
pygame.init()
start = pygame.mixer.Channel(0)
fon = pygame.mixer.Channel(1)
jump_hero = pygame.mixer.Channel(2)
hero_in_air = pygame.mixer.Channel(3)
arrow = pygame.mixer.Channel(5)
win = pygame.mixer.Channel(6)
menu_musfon = pygame.mixer.Channel(1)
start_go = pygame.mixer.Sound('music/3, 2, 1.wav')
fon_music = pygame.mixer.Sound('music/fon.wav')
jump = pygame.mixer.Sound('music/jump.wav')
in_air = pygame.mixer.Sound('music/hero_in_air.wav')
arrow_player = pygame.mixer.Sound('music/arrow.wav')
winner_mus = pygame.mixer.Sound('music/winner.wav')
menu_musfon = pygame.mixer.Sound("music/menu_fon.mp3")

def mixers_music():

    global fon_music
    global start
    global fon
    fon_music.set_volume(0.3)
    start.play(start_go)
    fon.play(fon_music)

def menu_music():

    pygame.mixer.stop()
    menu_musfon.play(loops=-1, fade_ms=30)
    menu_musfon.set_volume(0.5)
