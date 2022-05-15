import pygame
import os
import sys
import datetime
import tkinter.messagebox as mb
import emg1
import game_settings
import game
menu_musfon = pygame.mixer.Sound("music/menu_fon.mp3")
first_time = datetime.datetime.now()


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


class Button:
    def __init__(self, x, y, image, image2=None):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False
        self.first_image = image
        self.checkbox = False
        if image2:
            self.image2 = image2
            self.checkbox = True
            self.first_image2 = image2

    def draw(self):
        action = False
        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            self.image = load_image('Button.png')
            if self.checkbox:
                self.image2 = load_image('Button.png')
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        if not self.rect.collidepoint(pos):
            self.image = self.first_image
            if self.checkbox:
                self.image2 = self.first_image2
        if self.checkbox:
            if game_settings.emg == 1:
                game_settings.screen.blit(self.image2, self.rect)
            else:
                game_settings.screen.blit(self.image, self.rect)
        else:
            game_settings.screen.blit(self.image, self.rect)
        return action


import loading_game
loading_game.start_screen()


def main():
    global first_time
    global first_time
    import start_music
    start_music.menu_music()
    menu_bg = pygame.transform.scale(load_image('Menu-Fon.png'), (864, 760))
    Start_button_img = load_image("Start-Button.png")
    emg_on_Button_img = load_image("emg_button_on.png")
    emg_off_Button_img = load_image("emg_button_off.png")
    Exit_Button_img = load_image("Exit-Button.png")
    Settings_Button_img = load_image('Settings-Button.png')
    start = Button(game_settings.screen_width // 2, game_settings.screen_height // 2 - 150, Start_button_img)
    exit = Button(game_settings.screen_width // 2, game_settings.screen_height // 2 + 150, Exit_Button_img)
    emg = Button(game_settings.screen_width // 2, game_settings.screen_height // 2 + 50, emg_off_Button_img, emg_on_Button_img)
    settings = Button(game_settings.screen_width // 2, game_settings.screen_height // 2 - 50, Settings_Button_img)
    while True:
        game_settings.screen.blit(menu_bg, (0, 0))
        start.draw()
        emg.draw()
        exit.draw()
        settings.draw()

        if start.clicked:
            first_time = datetime.datetime.now()
            pygame.mixer.stop()
            game.game1(game_settings.map, game_settings.players, game_settings.click_red_chicken, game_settings.click_blue_chicken, game_settings.emg)

        if exit.clicked:
            pygame.quit()
            sys.exit()

        if emg.clicked:
            if game_settings.emg == 0:
                emg1.make_conn()
                if emg1.con_done == False:
                    msg = "EMG не подключен!"
                    mb.showerror("Ошибка", msg)
                else:
                    game_settings.emg = 1
            else:
                game_settings.emg = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()


if __name__ == "__main__":
    main()

