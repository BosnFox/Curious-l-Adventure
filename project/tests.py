import pygame
import ctypes
import datetime as dt
from random import randint


def animate_buttons():
    global text_y_2, text_y_1, height, text_2, text_1
    text_y_2 = height // 2 - text_2.get_height() // 2 + 195 if \
        text_y_2 == height // 2 - text_2.get_height() // 2 + 205 else height // 2 - text_2.get_height() // 2 + 205
    text_y_1 = height // 2 - text_1.get_height() // 2 - 205 if \
        text_y_1 == height // 2 - text_1.get_height() // 2 - 195 else height // 2 - text_1.get_height() // 2 - 195


def animate_text():
    global letters
    for i in range(len(letters)):
        char, x1, y1, color, under = letters[i]
        if under:
            y1 += 3
        else:
            y1 -= 3
        if y1 > 150:
            under = False
        elif y1 < 100:
            under = True
        letters[i] = char, x1, y1, color, under


def start_menu():
    user32 = ctypes.windll.user32  # получаем разрешения компьютера для создания окна
    user32.SetProcessDPIAware()
    width, height = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]

    pygame.init()
    screen = pygame.display.set_mode((0, 0))

    first_scene = True
    second_scene = False
    FOCUS = False
    EXIT = False
    NOW = dt.datetime.now()
    color_static = [(100, 255, 100), (0, 255, 0)]
    color_focused = [(255, 255, 255), (100, 100, 100)]


    screen.fill((0, 0, 0))
    font_1 = pygame.font.Font(None, 100)
    text_1 = font_1.render("Запустить", True, color_static[0])
    text_x_1 = width // 2 - text_1.get_width() // 2
    text_y_1 = height // 2 - text_1.get_height() // 2 - 195
    text_w_1 = text_1.get_width()
    text_h_1 = text_1.get_height()
    screen.blit(text_1, (text_x_1, text_y_1))
    pygame.draw.rect(screen, color_static[1], (text_x_1 - 10, text_y_1 - 10,
                                               text_w_1 + 20, text_h_1 + 20), 1)

    screen.fill((0, 0, 0))
    font_2 = pygame.font.Font(None, 100)
    text_2 = font_2.render("Выйти", True, color_static[0])
    text_x_2 = width // 2 - text_2.get_width() // 2
    text_y_2 = height // 2 - text_2.get_height() // 2 + 195
    text_w_2 = text_2.get_width()
    text_h_2 = text_2.get_height()
    screen.blit(text_2, (text_x_2, text_y_2))
    pygame.draw.rect(screen, color_static[1], (text_x_2 - 10, text_y_2 - 10,
                                               text_w_2 + 20, text_h_2 + 20), 1)

    letters = []
    x = 500
    y = 100
    UNDER = True
    for let in "Curious l'Adventure":
        letters.append([let, x, y, (randint(100, 255), randint(100, 255), randint(100, 255)), UNDER])
        x += 50
        if UNDER:
            y += 10
        else:
            y -= 10
        if y > 150:
            UNDER = False
        elif y < 100:
            UNDER = True
    TEXT_TIME = dt.datetime.now()

    pygame.display.flip()

    while first_scene:

        moment = dt.datetime.now()

        if (moment - NOW).microseconds >= 799999:
            NOW = moment
            animate_buttons()

        if (moment - TEXT_TIME).microseconds >= 10000:
            TEXT_TIME = moment
            animate_text()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                first_scene = False

            if event.type == pygame.MOUSEMOTION:

                if text_x_1 - 10 <= event.pos[0] <= text_x_1 + text_w_1 + 20 and \
                        text_y_1 - 10 <= event.pos[1] <= text_y_1 + text_h_1 + 20 and not FOCUS:
                    FOCUS = True
                elif not (text_x_1 - 10 <= event.pos[0] <= text_x_1 + text_w_1 + 20 and
                          text_y_1 - 10 <= event.pos[1] <= text_y_1 + text_h_1 + 20) and FOCUS:
                    FOCUS = False

                if text_x_2 - 10 <= event.pos[0] <= text_x_2 + text_w_2 + 20 and \
                        text_y_2 - 10 <= event.pos[1] <= text_y_2 + text_h_2 + 20 and not EXIT:
                    EXIT = True
                elif not (text_x_2 - 10 <= event.pos[0] <= text_x_2 + text_w_2 + 20 and
                          text_y_2 - 10 <= event.pos[1] <= text_y_2 + text_h_2 + 20) and EXIT:
                    EXIT = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:

                    if text_x_2 - 10 <= event.pos[0] <= text_x_2 + text_w_2 + 20 and \
                            text_y_2 - 10 <= event.pos[1] <= text_y_2 + text_h_2 + 20:
                        first_scene = False

                    if text_x_1 - 10 <= event.pos[0] <= text_x_1 + text_w_1 + 20 and \
                            text_y_1 - 10 <= event.pos[1] <= text_y_1 + text_h_1 + 20:
                        first_scene = False
                        second_scene = True



        screen.fill((0, 0, 0))
        text_1 = font_1.render("Запустить", True, color_focused[0] if FOCUS else color_static[0])
        screen.blit(text_1, (text_x_1, text_y_1))
        pygame.draw.rect(screen, color_focused[1] if FOCUS else color_static[1],
                         (text_x_1 - 10, text_y_1 - 10, text_w_1 + 20, text_h_1 + 20), 1)

        text_2 = font_2.render('Выйти', True, color_focused[0] if EXIT else color_static[0])
        screen.blit(text_2, (text_x_2, text_y_2))
        pygame.draw.rect(screen, color_focused[1] if EXIT else color_static[1],
                         (text_x_2 - 10, text_y_2 - 10, text_w_2 + 20, text_h_2 + 20), 1)

        for char, x1, y1, color, under in letters:
            char_font = pygame.font.Font(None, 100).render(char, True, color)
            screen.blit(char_font, (x1, y1))
        pygame.display.flip()

start_menu()