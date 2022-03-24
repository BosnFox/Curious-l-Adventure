import pygame
import sys
import os
import ctypes
from random import randint


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


def middle_scene():
    user32 = ctypes.windll.user32  # получаем разрешения компьютера для создания окна
    user32.SetProcessDPIAware()
    width, height = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]

    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((0, 0))

    running = True
    FPS = 90
    off_x = width / 1920
    off_y = height / 1080
    clock = pygame.time.Clock()
    story_song = pygame.mixer.Sound('project/fairy tale.mp3')
    story_song.set_volume(0.5)
    text = pygame.transform.scale(load_image('press key.png'), (800 * off_x, 200 * off_y))
    alpha = 255
    x, y = width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2
    half = True

    story_song.play(-1)

    pygame.display.flip()
    pygame.mouse.set_visible(False)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                pygame.mixer.quit()
                return

        screen.fill((0, 0, 0))
        screen.blit(text, (x, y))

        text.set_alpha(alpha)

        if alpha < 0:
            half = True
            y = randint(height // 4, height // 4 * 3)
            x = randint(int(50 * off_x), int(width - text.get_width() - 50 * off_y))
        elif alpha > 255:
            half = False

        alpha += 5 if half else -5

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    print('Hello!')
