import pygame
import ctypes
import datetime as dt
import os
import sys


def end_game(time):
    def load_image(name, colorkey=None):  # функция для загрузки изображения
        fullname = os.path.join('project', name)
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

    def animate_buttons():
        nonlocal text_y_2
        text_y_2 = height // 2 - text_2.get_height() // 2 + 195 * off_y if \
            text_y_2 == height // 2 - text_2.get_height() // 2 + 205 * off_y else height // 2 - text_2.get_height() // 2 + 205 * off_y

    user32 = ctypes.windll.user32  # получаем разрешения компьютера для создания окна
    user32.SetProcessDPIAware()
    width, height = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]

    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((0, 0))

    EXIT = False
    off_x, off_y = width / 1920, height / 1080
    song = pygame.mixer.Sound('project/end menu 1.mp3')
    cursor = pygame.transform.scale(load_image('cursor.png'), (40 * off_x, 40 * off_y))
    song.set_volume(0.5)
    NOW = dt.datetime.now()
    color_static = [(100, 255, 100), (0, 255, 0)]
    color_focused = [(255, 255, 255), (100, 100, 100)]

    screen.fill((0, 0, 0))
    font_2 = pygame.font.Font(None, int(100 * min(off_x, off_y)))
    text_2 = font_2.render("Выйти в главное меню", True, color_static[0])
    text_x_2 = width // 2 - text_2.get_width() // 2
    text_y_2 = height // 2 - text_2.get_height() // 2 + 195 * off_y
    text_w_2 = text_2.get_width()
    text_h_2 = text_2.get_height()
    screen.blit(text_2, (text_x_2, text_y_2))
    pygame.draw.rect(screen, color_static[1], (text_x_2 - 10 * off_x, text_y_2 - 10 * off_y,
                                               text_w_2 + 20 * off_x, text_h_2 + 20 * off_y), 1)

    screen.fill((0, 0, 0))
    font_1 = pygame.font.Font(None, int(100 * min(off_x, off_y)))
    text_1 = font_1.render("Ваше время:", True, color_static[0])
    text_x_1 = width // 2 - text_1.get_width() // 2
    text_y_1 = height // 2 - text_1.get_height() // 2 - 300 * off_y
    text_w_1 = text_1.get_width()
    text_h_1 = text_1.get_height()
    screen.blit(text_1, (text_x_1, text_y_1))
    pygame.draw.rect(screen, pygame.Color(0, 0, 0), (text_x_1 - 50 * off_x, text_y_1 - 50 * off_y,
                                                    text_w_1 + 100 * off_x, text_h_1 + 100 * off_y), 1)

    screen.fill((0, 0, 0))
    font_3 = pygame.font.Font(None, int(100 * min(off_x, off_y)))
    text_3 = font_3.render(time.__str__(), True, color_static[0])
    text_x_3 = width // 2 - text_3.get_width() // 2
    text_y_3 = height // 2 - text_3.get_height() // 2 - 100 * off_y
    text_w_3 = text_3.get_width()
    text_h_3 = text_3.get_height()
    screen.blit(text_3, (text_x_3, text_y_3))

    pygame.display.flip()
    song.play(-1)

    mouse_x, mouse_y = width // 2, height // 2
    pygame.mouse.set_visible(False)

    while True:

        moment = dt.datetime.now()

        if (moment - NOW).microseconds >= 799999:
            NOW = moment
            animate_buttons()

        for event in pygame.event.get():

            if event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = event.pos

                if text_x_2 - 10 * off_x <= event.pos[0] <= text_x_2 + text_w_2 + 20 * off_x and \
                        text_y_2 - 10 * off_y <= event.pos[1] <= text_y_2 + text_h_2 + 20 * off_y and not EXIT:
                    EXIT = True
                elif not (text_x_2 - 10 * off_x <= event.pos[0] <= text_x_2 + text_w_2 + 20 * off_x and
                          text_y_2 - 10 * off_y <= event.pos[1] <= text_y_2 + text_h_2 + 20 * off_y) and EXIT:
                    EXIT = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:

                    if text_x_2 - 10 * off_x <= event.pos[0] <= text_x_2 + text_w_2 + 20 * off_x and \
                            text_y_2 - 10 * off_y <= event.pos[1] <= text_y_2 + text_h_2 + 20 * off_y:
                        pygame.mixer.quit()
                        return False

        screen.fill((0, 0, 0))

        text_2 = font_2.render('Выйти в главное меню', True,
                               color_focused[0] if EXIT else color_static[0])
        screen.blit(text_2, (text_x_2, text_y_2))
        pygame.draw.rect(screen, color_focused[1] if EXIT else color_static[1],
                         (text_x_2 - 10 * off_x, text_y_2 - 10 * off_y, text_w_2 + 20 * off_x, text_h_2 + 20 * off_y), 1)

        text_1 = font_1.render("Ваше время:", True, color_static[0])
        screen.blit(text_1, (text_x_1, text_y_1))
        pygame.draw.rect(screen, color_static[1], (text_x_1 - 50 * off_x, text_y_1 - 50 * off_y,
                                                   text_w_1 + 100 * off_x, text_h_1 + 100 * off_y), 1)

        text_3 = font_3.render(time.__str__(), True, color_static[0])
        screen.blit(text_3, (text_x_3, text_y_3))

        screen.blit(cursor, (mouse_x, mouse_y))

        pygame.display.flip()


if __name__ == '__main__':
    if end_game(dt.timedelta(hours=10, minutes=159, seconds=63)):
        print('Game has just started!')
    else:
        print('Goodbye!')
