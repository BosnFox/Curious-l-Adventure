import pygame
import ctypes
from StartMenu import load_game
from FairyTale import middle_scene
import datetime as dt
from Description import *
from EndMenu import end_game


def collide_group(sprite, group):
    for elem in group:
        if pygame.sprite.collide_mask(sprite, elem):
            return True
    return False


class Message(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = message
        self.rect = self.image.get_rect()
        self.rect.x = width // 2 - self.rect.w // 2
        self.rect.y = 750 * off_y
        self.text = ''
        self.is_hide = True

    def set_text(self, text):
        self.text = text

    def show(self):
        message_group.add(self)
        self.is_hide = False

    def hide(self):
        message_group.remove(self)
        self.is_hide = True

    def receive(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.x <= event.pos[0] <= self.rect.x + self.rect.w and \
                    self.rect.y <= event.pos[1] <= self.rect.y + self.rect.h and not self.is_hide:
                self.hide()

    def update(self):
        if not self.is_hide:
            x = self.rect.x + 70 * off_x
            x1, y1 = x, self.rect.y + 40 * off_y
            x2 = self.rect.x + self.rect.w - 250 * off_x
            for word in self.text.split():
                font = pygame.font.Font(pygame.font.match_font('Lucida Console'), int(35 * min(off_x, off_y)))
                text = font.render(word + ' ', True, (0, 0, 0))
                text_x = x1
                text_y = y1
                if x1 + text.get_width() > x2:
                    x1 = x
                    y1 += 50 * off_y
                else:
                    x1 += text.get_width()
                screen.blit(text, (text_x, text_y))


class InteractiveObject(pygame.sprite.Sprite):
    def __init__(self, text, image, pos, group, used_text=''):
        super().__init__(all_sprites, group)
        self.was_used = False
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.text = text
        self.used_text = used_text

    def receive(self, event):
        x1, y1 = self.rect.x + self.rect.w // 2, self.rect.y + self.rect.h // 2
        x2, y2 = men.rect.x + men.rect.w // 2, men.rect.y + men.rect.h // 2
        length = (x1 - x2) ** 2 + (y1 - y2) ** 2
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and length <= 22500 and self.rect.x <= \
                    event.pos[0] <= self.rect.x + self.rect.w and \
                    self.rect.y <= event.pos[1] <= self.rect.y + self.rect.h:
                text_message.set_text(
                    self.text if not self.was_used or self.used_text == '' else self.used_text)
                text_message.show()
                self.was_used = True
                return True
        return False


class AnimatedObject(InteractiveObject):
    def __init__(self, text, image1, image2, sound1, sound2, pos, group, targets, check,
                 action_text='', used_text='', ghost_text=''):
        super().__init__(text, image1, pos, group, used_text)
        self.other_image = image2
        self.targets = targets
        self.check = check
        self.action_text = action_text
        self.ghost_text = ghost_text
        self.sound = sound1
        self.action_sound = sound2

    def receive(self, event):
        x1, y1 = self.rect.x + self.rect.w // 2, self.rect.y + self.rect.h // 2
        x2, y2 = men.rect.x + men.rect.w // 2, men.rect.y + men.rect.h // 2
        length = (x1 - x2) ** 2 + (y1 - y2) ** 2
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and length <= 22500 and self.rect.x <= \
                    event.pos[0] <= self.rect.x + self.rect.w and \
                    self.rect.y <= event.pos[
                1] <= self.rect.y + self.rect.h and text_message.is_hide:
                if not self.was_used and all(list(bag.have(elem) for elem in self.check)):
                    self.image = self.other_image
                    self.take()
                    for name, sprite in self.targets:
                        bag.add_item(name, sprite)
                    self.was_used = True
                    text_message.set_text(self.action_text)
                    self.action_sound.play()
                elif bot in ghost_group:
                    text_message.set_text(self.ghost_text)
                elif self.was_used:
                    text_message.set_text(self.used_text)
                    self.sound.play()
                else:
                    text_message.set_text(self.text)
                    self.sound.play()
                text_message.show()
                return True
        return False

    def take(self):
        if self.check is not None:
            for key in self.check:
                if bag.have(key):
                    bag.clear_item(key)


class ExitDoor(AnimatedObject):
    def __init__(self, text, image1, image2, sound1, sound2, sound3, pos, group, targets, check,
                 action_text='', ghost_text=''):
        super().__init__(text, image1, image2, sound1, sound2, pos, group, targets, check,
                         action_text, ghost_text)
        self.sound3 = sound3
        self.ghost_text = text_exit_door[-1]

    def receive(self, event):
        global END_GAME
        x1, y1 = self.rect.x + self.rect.w // 2, self.rect.y + self.rect.h // 2
        x2, y2 = men.rect.x + men.rect.w // 2, men.rect.y + men.rect.h // 2
        length = (x1 - x2) ** 2 + (y1 - y2) ** 2
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and length <= 22500 and self.rect.x <= \
                    event.pos[0] <= self.rect.x + self.rect.w and \
                    self.rect.y <= event.pos[
                1] <= self.rect.y + self.rect.h and text_message.is_hide:
                if not self.was_used and all(list(bag.have(elem) for elem in self.check)):
                    self.image = self.other_image
                    self.take()
                    for name, sprite in self.targets:
                        bag.add_item(name, sprite)
                    self.was_used = True
                    text_message.set_text(self.action_text)
                    self.action_sound.play()
                elif bot in ghost_group:
                    text_message.set_text(self.ghost_text)
                    END_GAME = True
                    self.sound3.play()
                elif self.was_used:
                    text_message.set_text(self.ghost_text)
                    self.sound.play()
                else:
                    text_message.set_text(self.text)
                    self.sound.play()
                text_message.show()
                return True
        return False


class MoveObject(InteractiveObject):
    def __init__(self, text, image1, image2, image3, image4, pos, group):
        super().__init__('', image1, pos, group, '')
        self.image = image1
        self.image1 = image1
        self.image2 = image2
        self.image3 = image3
        self.image4 = image4
        self.phrases = text
        self.is_alpha = False
        self.alpha = 0
        self.now = dt.datetime.now()
        self.teleport = False
        self.animated = False
        self.view = True
        self.phrase_now = 0

    def receive(self, event):
        x1, y1 = self.rect.x + self.rect.w // 2, self.rect.y + self.rect.h // 2
        x2, y2 = men.rect.x + men.rect.w // 2, men.rect.y + men.rect.h // 2
        length = (x1 - x2) ** 2 + (y1 - y2) ** 2
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and length <= 22500 and self.rect.x <= \
                    event.pos[0] <= self.rect.x + self.rect.w and \
                    self.rect.y <= event.pos[
                1] <= self.rect.y + self.rect.h and text_message.is_hide:
                if self.phrase_now < len(self.phrases):
                    text_message.set_text(self.phrases[self.phrase_now])
                    text_message.show()
                    self.phrase_now += 1
                return True

        return False

    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def update(self):
        if bag.have(text_key) and self not in ghost_group:
            ghost_group.add(self)
            self.set_position(men.rect.x + 75, men.rect.y - 50)
            ghost_music.play()
        if self in ghost_group:
            if bag.have(text_key) and not self.is_alpha:
                if self.alpha < 255:
                    self.alpha += 3
                    self.image1.set_alpha(self.alpha)
                    self.image2.set_alpha(self.alpha)
                    self.image3.set_alpha(self.alpha)
                    self.image4.set_alpha(self.alpha)
                elif self.alpha == 255 and not self.is_alpha:
                    self.is_alpha = True

            if self.teleport:
                if self.alpha < 255:
                    self.alpha += 5
                    self.image1.set_alpha(self.alpha)
                    self.image2.set_alpha(self.alpha)
                    self.image3.set_alpha(self.alpha)
                    self.image4.set_alpha(self.alpha)
                elif self.alpha == 255:
                    self.teleport = False

            if self.animated:
                if self.alpha > 0:
                    self.alpha -= 5
                    self.image1.set_alpha(self.alpha)
                    self.image2.set_alpha(self.alpha)
                    self.image3.set_alpha(self.alpha)
                    self.image4.set_alpha(self.alpha)
                elif self.alpha == 0:
                    self.set_position(men.rect.x, men.rect.y - 40)
                    self.teleport = True
                    self.animated = False

            if self.rect.x < men.rect.x:
                self.view = True
            elif self.rect.x > men.rect.x:
                self.view = False

            moment = dt.datetime.now()
            if (moment - self.now).seconds >= 1:
                if self.view:
                    self.image = self.image2 if self.image == self.image1 else self.image1
                else:
                    self.image = self.image4 if self.image == self.image3 else self.image3
                self.now = moment

            length = 150
            x1, y1 = self.rect.x + self.rect.w // 2, self.rect.y + self.rect.h // 2
            x2, y2 = men.rect.x + men.rect.w // 2, men.rect.y + men.rect.h // 2
            leng = (x1 - x2) ** 2 + (y1 - y2) ** 2

            if leng >= 90000 and not self.animated:
                self.animated = True

            if self.rect.x < men.rect.x - length:
                self.rect.x += men.speed
                if pygame.sprite.spritecollide(self, ground_group, False):
                    self.rect.x -= men.speed
            if self.rect.x > men.rect.x + length:
                self.rect.x -= men.speed
                if pygame.sprite.spritecollide(self, ground_group, False):
                    self.rect.x += men.speed
            if self.rect.y < men.rect.y - length:
                self.rect.y += men.speed
                if pygame.sprite.spritecollide(self, ground_group, False):
                    self.rect.y -= men.speed
            if self.rect.y > men.rect.y + length:
                self.rect.y -= men.speed
                if pygame.sprite.spritecollide(self, ground_group, False):
                    self.rect.y += men.speed


class ButtonExit(pygame.sprite.Sprite):
    def __init__(self, **kwargs):
        super().__init__(button_group)
        self.image = close_button
        self.rect = self.image.get_rect()
        self.rect.x = width - 300 * off_x
        self.rect.y = 100 * off_y

    def receive(self, event):
        global running
        if event.type == pygame.MOUSEMOTION:
            if self.rect.x <= event.pos[0] <= self.rect.x + self.rect.w and \
                    self.rect.y <= event.pos[1] <= self.rect.y + self.rect.h and \
                    self.image != close_button_mirror:
                self.image = close_button_mirror
            elif not (self.rect.x <= event.pos[0] <= self.rect.x + self.rect.w and
                      self.rect.y <= event.pos[1] <= self.rect.y + self.rect.h) and \
                    self.image != close_button:
                self.image = close_button
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if 100 * off_y <= event.pos[1] <= 150 * off_y and width - 300 * off_x <= event.pos[0] <= width - 100 * off_x:
                    running = False


class Player(pygame.sprite.Sprite):
    # класс главного героя
    def __init__(self, pos):
        super().__init__(player_group)
        self.width = 223 / 3 * off_x
        self.height = 296 / 3 * off_y
        self.left_side = pygame.transform.scale(character, (self.width, self.height))
        self.right_side = pygame.transform.scale(character_1, (self.width, self.height))
        self.relax_1 = pygame.transform.scale(character_eyes, (self.width, self.height))
        self.relax_2 = pygame.transform.scale(character_eyes_1, (self.width, self.height))
        self.left_move = pygame.transform.scale(character_move, (259 / 3 * off_x, self.height - 2 * off_y))
        self.right_move = pygame.transform.scale(character_move_1, (259 / 3 * off_x, self.height - 2 * off_y))
        self.image = self.left_side
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos[0] - self.width // 2, pos[1] - self.height // 2
        self.left, self.right, self.up, self.down = False, False, False, False
        self.speed = int(3 * (off_x * off_x + off_y * off_y) ** 0.5)
        self.check_inventory = False
        self.now = dt.datetime.now()
        self.run = dt.datetime.now()
        self.view = True
        self.in_move = False
        self.step_time = dt.datetime.now()

    def receive(self, event):
        # здесь обрабатываются события, происходящие на компьютере
        if bag.chosen is None and text_message.is_hide:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.up = True
                if event.key == pygame.K_s:
                    self.down = True
                if event.key == pygame.K_a:
                    self.left = True
                    self.image = self.left_side
                    self.view = True
                if event.key == pygame.K_d:
                    self.right = True
                    self.image = self.right_side
                    self.view = False
                if (self.up or self.down or self.right or self.left) and not self.in_move:
                    self.in_move = True
                    self.run = dt.datetime.now()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.up = False
                    self.now = dt.datetime.now()
                if event.key == pygame.K_s:
                    self.down = False
                    self.now = dt.datetime.now()
                if event.key == pygame.K_a:
                    self.left = False
                    self.now = dt.datetime.now()
                if event.key == pygame.K_d:
                    self.right = False
                    self.now = dt.datetime.now()
                if not (self.up or self.down or self.right or self.left) and self.in_move:
                    self.in_move = False
                    self.image = self.relax_1 if (self.image == self.left_side or
                                                  self.image == self.left_move) else self.relax_2
        else:
            self.left, self.right, self.up, self.down = False, False, False, False

    def update(self):
        # функция обрабатывает то, что будет происходить с игроком в любой момент времени
        if bag.chosen is not None or not (self.up or self.down or self.right or self.left):
            moment = dt.datetime.now()
            if (moment - self.now).microseconds >= 800000:
                if self.view:
                    self.image = self.relax_1 if self.image == self.left_side else self.left_side
                else:
                    self.image = self.relax_2 if self.image == self.right_side else self.right_side
                self.now = moment
        if text_message.is_hide and bag.chosen is None:
            if self.up or self.down or self.right or self.left:
                moment = dt.datetime.now()
                if (moment - self.step_time).microseconds >= 600000:
                    step.play()
                    self.step_time = moment
                if (moment - self.run).microseconds >= 300000:
                    if self.view:
                        self.image = self.left_move if self.image == self.left_side else self.left_side
                    else:
                        self.image = self.right_move if self.image == self.right_side else self.right_side
                    self.run = moment
            for elem in all_sprites:
                if self.up:
                    elem.rect.y += self.speed
            if pygame.sprite.spritecollide(men, ground_group, False) or collide_group(men,
                                                                                      interior_group):
                for elem in all_sprites:
                    if self.up:
                        elem.rect.y -= self.speed
            for elem in all_sprites:
                if self.down:
                    elem.rect.y -= self.speed
            if pygame.sprite.spritecollide(men, ground_group, False) or collide_group(men,
                                                                                      interior_group):
                for elem in all_sprites:
                    if self.down:
                        elem.rect.y += self.speed
            for elem in all_sprites:
                if self.right:
                    elem.rect.x -= self.speed
            if pygame.sprite.spritecollide(men, ground_group, False) or collide_group(men,
                                                                                      interior_group):
                for elem in all_sprites:
                    if self.right:
                        elem.rect.x += self.speed
            for elem in all_sprites:
                if self.left:
                    elem.rect.x += self.speed
            if pygame.sprite.spritecollide(men, ground_group, False) or collide_group(men,
                                                                                      interior_group):
                for elem in all_sprites:
                    if self.left:
                        elem.rect.x -= self.speed


class Inventory(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(inventory_group)
        self.image = back_pack[0]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
        self.rect.x *= off_x
        self.rect.y *= off_y
        self.items = dict()
        self.chosen = None

    def receive(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos[0] - self.rect.x, event.pos[1] - self.rect.y
            if 17 * off_x <= y <= 100 * off_x and int(x // (100 * off_x)) < 6:
                i = int(x // (100 * off_x))
                if 0 <= i <= 5:
                    if self.chosen == i:
                        self.image = back_pack[0]
                        self.chosen = None
                    else:
                        self.image = back_pack[i + 1]
                        self.chosen = i

    def update(self):
        x, y = self.rect.x + 16 * off_x, self.rect.y
        for name in self.items:
            rect = self.items[name].get_rect()
            screen.blit(self.items[name], (x + 85 // 2 * off_x - rect.w // 2, y + 50 * off_y - rect.h // 2))
            x += 96 * off_x
        if self.chosen is not None:
            rect = description.get_rect()
            screen.blit(description, ((17 + self.chosen * 100) * off_x, (17 + 100) * off_y))
            default = (self.chosen * 100 + 45) * off_x
            x, y = default, 210 * off_y
            border = self.chosen * 100 * off_x + rect.w - 130 * off_x
            if self.chosen < len(self.items.keys()):
                for word in list(self.items.keys())[self.chosen].split():
                    font = pygame.font.Font(pygame.font.match_font('Lucida Console'), int(20 * min(off_x, off_y)))
                    text = font.render(word + ' ', True, (255, 255, 255))
                    text_x, text_y = x, y
                    if x + text.get_width() > border:
                        x = default
                        y += 25 * off_y
                    else:
                        x += text.get_width()
                    screen.blit(text, (text_x, text_y))
            else:
                for word in 'В этой ячейке нет предмета'.split():
                    font = pygame.font.Font(pygame.font.match_font('Lucida Console'), int(20 * min(off_x, off_y)))
                    text = font.render(word + ' ', True, (255, 255, 255))
                    text_x, text_y = x, y
                    if x + text.get_width() > border:
                        x = default
                        y += 50 * off_y
                    else:
                        x += text.get_width()
                    screen.blit(text, (text_x, text_y))

    def add_item(self, name, item):
        self.items[name] = item

    def clear_item(self, name):
        self.items.pop(name)

    def have(self, name):
        if name in self.items:
            return True
        return False


def generate_room(x, y, image):
    # функция для создания пола в коридоре или в комнате
    block = pygame.sprite.Sprite(all_sprites, floor_group)
    block.image = image
    block.rect = block.image.get_rect()
    block.rect.x = width // 2 + x * 100 * off_x
    block.rect.y = height // 2 + y * 100 * off_y
    walk.append((x, y))


def generate_mini_wall(x, y, image):
    # функция для создания мини-стен
    block = pygame.sprite.Sprite(all_sprites, mini_floor_group)
    block.image = image
    block.rect = block.image.get_rect()
    block.rect.x = width // 2 + x * 100 * off_x
    block.rect.y = height // 2 + y * 100 * off_y
    walk.append((x, y))


def generate_wall(x, y, image):
    # функция для создания стен
    block = pygame.sprite.Sprite(all_sprites, floor_group)
    block.image = image
    block.rect = block.image.get_rect()
    block.rect.x = width // 2 + x * 100 * off_x
    block.rect.y = height // 2 + y * 100 * off_y
    walk.append((x, y))


def init_level():
    global walk
    for i in range(-8, -3):
        # левая верхняя комната
        for j in range(-7, -2):
            generate_room(i, j, floor)

    for i in range(2, 8):
        # правая верхняя комната
        for j in range(-8, -1):
            generate_room(i, j, floor)

    for i in range(-9, -2):
        # левая нижняя комната
        for j in range(4, 9):
            generate_room(i, j, floor)

    ball = [(3, 5), (4, 4), (5, 3), (6, 3), (7, 4), (8, 5), (8, 6), (7, 7), (6, 8), (5, 8), (4, 7),
            (3, 6), (4, 5), (5, 5), (6, 5), (7, 5), (4, 6), (5, 6), (6, 6), (7, 6), (5, 4), (6, 4),
            (5, 7), (6, 7)]

    for i, j in ball:
        # правая нижняя комната
        generate_room(i, j, floor)

    for i in range(-3, 2):
        # верхний коридор
        for j in range(-6, -4):
            generate_room(i, j, corridor)

    for i in range(-7, -5):
        # левый коридор
        for j in range(-2, 4):
            generate_room(i, j, corridor)

    for i in range(-2, 3):
        # нижний коридор
        for j in range(5, 7):
            generate_room(i, j, corridor)

    for i in range(5, 7):
        # правый коридор
        for j in range(-1, 3):
            generate_room(i, j, corridor)

    for i in range(-8, -3):
        # верхняя стена левой верхней комнаты
        generate_wall(i, -8, wall_room)

    for i in range(2, 8):
        # верхняя стена правой верхней комнаты
        generate_room(i, -9, wall_room)

    for i in [-9, -8, -5, -4, -3]:
        # верхняя стена левой нижней комнаты
        generate_wall(i, 3, wall_room)

    for i, j in [(3, 4), (4, 3), (7, 3), (8, 4)]:
        # верхняя стена правой нижней комнаты
        generate_wall(i, j, wall_room)

    for i in [-8, -5, -4]:
        # нижняя стена левой верхней комнаты
        generate_mini_wall(i, -2.5, wall_room_mini)

    for i in range(-9, -2):
        # нижняя стена левой нижней комнаты
        generate_mini_wall(i, 8.5, wall_room_mini)

    for i in [2, 3, 4, 7]:
        # нижняя стена правой верхней комнаты
        generate_mini_wall(i, -1.5, wall_room_mini)

    for i, j in [(3, 6.5), (4, 7.5), (7, 7.5), (5, 8.5), (6, 8.5),
                 (8, 6.5)]:
        # нижняя стена правой нижней комнаты
        generate_mini_wall(i, j, wall_room_mini)

    for i in range(-3, 2):
        # верхняя стена верхнего коридора
        generate_wall(i, -7, wall_corridor if i != -1 else easter_egg)

    for i in range(-3, 2):
        # нижняя стена верхнего коридора
        generate_mini_wall(i, -4.5, wall_corridor_mini)

    for i in range(-2, 3):
        # верхняя стена нижнего коридора
        generate_wall(i, 4, wall_corridor)

    for i in range(-2, 3):
        # нижняя стена нижнего коридора
        generate_mini_wall(i, 6.5, wall_corridor_mini)

    for i in range(-10, 10):
        # отрисовка травы, основная текстура пространства
        for j in range(-10, 10):
            if (i, j) not in walk:
                block = pygame.sprite.Sprite(all_sprites, ground_group)
                block.image = grass
                block.rect = block.image.get_rect()
                block.rect.x = width // 2 + i * 100 * off_x
                block.rect.y = height // 2 + j * 100 * off_y

    for j in range(3, 9):
        # левая боковая стена левой нижней комнаты
        generate_wall(-9, j, wall_side)

    for j in [3, 7, 8]:
        # правая боковая стена левой нижней комнаты
        generate_wall(-2, j, wall_side)

    for i, j in [(4, 3), (8, 3), (9, 4), (9, 5), (9, 6), (8, 7), (7, 8), (5, 8),
                 (4, 7)]:
        # боковые стены круглой комнаты
        generate_wall(i, j, wall_side)

    for j in range(-9, -1):
        # правая боковая стена правой верхней комнаты
        generate_wall(8, j, wall_side)

    for j in [-9, -8, -4, -3, -2]:
        # левая боковая стена правой верхней комнаты
        generate_wall(2, j, wall_side)

    for j in range(-8, -2):
        # левая боковая стена левой верхней комнаты
        generate_wall(-8, j, wall_side)

    for j in [-8, -4, -3]:
        # правая боковая стена левой верхней комнаты
        generate_wall(-3, j, wall_side)

    # боковые стены левого коридора
    generate_wall(-7, -2.5, pygame.transform.scale(wall_corridor_side, (5, 50)))
    generate_wall(-5.05, -2.5, pygame.transform.scale(wall_corridor_side, (5, 59)))
    for j in range(-2, 4):
        generate_wall(-7, j, wall_corridor_side)
        generate_wall(-5.05, j, wall_corridor_side)

    # боковые стены правого коридора
    generate_wall(5, -1.5, pygame.transform.scale(wall_corridor_side, (5, 50)))
    generate_wall(6.95, -1.5, pygame.transform.scale(wall_corridor_side, (5, 50)))
    for j in range(-1, 3):
        generate_wall(5, j, wall_corridor_side)
        generate_wall(6.95, j, wall_corridor_side)

    clue = pygame.sprite.Sprite(all_sprites, no_clip_group)
    clue.image = tip
    clue.rect = clue.image.get_rect()
    clue.rect.x, clue.rect.y = width // 2 + 5 * 100 * off_x, height // 2 - 9 * 100 * off_y

    desk = pygame.sprite.Sprite(all_sprites, interior_group)
    desk.image = table
    desk.rect = desk.image.get_rect()
    desk.rect.x, desk.rect.y = width // 2 + 7 * 100 * off_x, height // 2 + (6 * 100 + 50) * off_y

    for elem in all_sprites:
        elem.rect.x += -600 * off_x
        elem.rect.y += -575 * off_y

    walk.clear()


if __name__ == '__main__':
    has_seen = False
    while True:
        if load_game():
            if not has_seen:
                middle_scene()
                has_seen = True
            user32 = ctypes.windll.user32
            # получаем разрешения компьютера для создания окна
            user32.SetProcessDPIAware()
            width, height = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]

            pygame.init()
            pygame.display.set_caption("Curious l'Adventure")
            screen = pygame.display.set_mode((0, 0))
            clock = pygame.time.Clock()
            mouse_x, mouse_y = width // 2, height // 2

            FPS = 90
            screen.fill((0, 0, 0))
            running = True
            END_GAME = False
            walk = []
            TIME = dt.datetime.now()
            off = max(width / 1920, height / 1080)

            all_sprites = pygame.sprite.Group()
            ground_group = pygame.sprite.Group()
            floor_group = pygame.sprite.Group()
            player_group = pygame.sprite.Group()
            mini_floor_group = pygame.sprite.Group()
            button_group = pygame.sprite.Group()
            message_group = pygame.sprite.Group()
            interior_group = pygame.sprite.Group()
            no_clip_group = pygame.sprite.Group()
            inventory_group = pygame.sprite.Group()
            ghost_group = pygame.sprite.Group()

            bag = Inventory([30, 30])
            men = Player([width // 2, height // 2])
            button = ButtonExit()
            exit_door = ExitDoor(text_exit_door[0], door, door, no, end_music, exit_door_music,
                                 (width // 2 + 6 * 100 * off_x, height // 2 - 9 * 100 * off_y), no_clip_group,
                                 [], [text_key], text_exit_door[1], text_exit_door[2])

            friendly_note = InteractiveObject(text_friendly_note[0], note,
                                              (
                                                  width // 2 + (7 * 100 + 25) * off_x,
                                                  height // 2 + (6 * 100 + 65) * off_y),
                                              no_clip_group, text_friendly_note[1])

            chair = AnimatedObject(text_chair[0], armchair_glass, armchair, no, take,
                                   (width // 2 - 3.5 * 100 * off_x, height // 2 + 3.5 * 100 * off_y),
                                   interior_group, [(text_glasses, glasses)], [],
                                   text_chair[1], text_chair[2], text_chair[3])

            bookshelf = AnimatedObject(text_bookshelf[0], bookcase, bookcase_used, no, take_book,
                                       (width // 2 - 2.80 * 100 * off_x, height // 2 + (7 * 100 - 10) * off_y),
                                       interior_group, [(text_451_book, book)], [text_glasses],
                                       text_bookshelf[1], text_bookshelf[2], text_bookshelf[3])

            safe = AnimatedObject(text_safe[0], safe_box, safe_box_used, no, numpad,
                                  (width // 2 + 1 * 100 * off_x, height // 2 + 4 * 100 * off_y),
                                  no_clip_group, [(text_crowbar, crowbar)], [text_451_book],
                                  text_safe[1], text_safe[2], text_safe[3])

            hole_floor = AnimatedObject(text_hole_floor[0], fake_floor, opened_fake_floor, no,
                                        take_necronomicon,
                                        (width // 2 + 4 * 100 * off_x, height // 2 + 4 * 100 * off_y),
                                        no_clip_group,
                                        [(text_necronomicon, necronomicon), (text_crowbar, crowbar)],
                                        [text_crowbar],
                                        text_hole_floor[1], text_hole_floor[2], text_hole_floor[3])

            crafttable = AnimatedObject(text_crafttable[0], toolbox, toolbox, no, take_instrument,
                                        (width // 2 + (2 * 100 + 5) * off_x, height // 2 - 8.5 * 100 * off_y),
                                        interior_group,
                                        [(text_hacksaw, hacksaw), (text_crowbar, crowbar)],
                                        [text_crowbar],
                                        text_crafttable[1], text_crafttable[2], text_crafttable[3])

            knife_case = AnimatedObject(text_knife_case[0], dressing_case, dressing_case_used, no,
                                        sawing,
                                        (width // 2, height // 2 - 6.75 * 100 * off_y),
                                        no_clip_group, [(text_knife, knife)], [text_hacksaw],
                                        text_knife_case[1], text_knife_case[2], text_knife_case[3])

            eating_table = AnimatedObject(text_eating_table[0], kitchen_table_used, kitchen_table,
                                          no, take_book,
                                          (width // 2 - (8 * 100 - 5) * off_x, height // 2 - 7.5 * 100 * off_y),
                                          interior_group, [(text_cook_book, cook_book)], [],
                                          text_eating_table[1], text_eating_table[2],
                                          text_eating_table[3])

            fridge = AnimatedObject(text_fridge[0], refridgerator, refridgerator, opening_fridge,
                                    active_fridge,
                                    (width // 2 - 4.1 * 100 * off_x, height // 2 - 8 * 100 * off_y),
                                    interior_group, [(text_meat, meat), (text_cook_book, cook_book)],
                                    [text_cook_book],
                                    text_fridge[1], text_fridge[2], text_fridge[3])

            cookcase = AnimatedObject(text_cookcase[0], cookshelf, cookshelf, no, take_spices,
                                      (width // 2 - (7 * 100 - 30) * off_x, height // 2 - 7.7 * 100 * off_y),
                                      interior_group,
                                      [(text_spices, spices), (text_cook_book, cook_book)],
                                      [text_cook_book],
                                      text_cookcase[1], text_cookcase[2], text_cookcase[3])

            gas_oven = AnimatedObject(text_gas_oven[0], oven, oven, no, take_meat,
                                      (width // 2 - 5.5 * 100 * off_x, height // 2 - 7.5 * 100 * off_y),
                                      interior_group, [(text_bone, bone)], [text_cook_book,
                                                                            text_meat, text_spices],
                                      text_gas_oven[1], text_gas_oven[2], text_gas_oven[3])

            shrine = AnimatedObject(text_shrine[0], altar, altar_used, no, take,
                                    (width // 2 - 9 * 100 * off_x, height // 2 + 4 * 100 * off_y),
                                    interior_group, [(text_key, key)], [text_bone, text_necronomicon,
                                                                        text_knife, text_crowbar],
                                    text_shrine[1], text_shrine[2], text_shrine[3])

            bot = MoveObject(ghost_phrases, ghost_1, ghost_2, ghost_3, ghost_4, (0, 0),
                             all_sprites)

            text_message = Message()
            text_message.set_text('Невзирая на головную боль, Вы просыпаетесь и, наверное, сильно'
                                  ' удивляетесь...')
            text_message.show()

            init_level()

            pygame.mouse.set_visible(False)

            r, g, b = 100, 100, 255

            while running:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEMOTION:
                        mouse_x, mouse_y = event.pos
                    men.receive(event)
                    button.receive(event)
                    bag.receive(event)

                    if not friendly_note.receive(event) and not exit_door.receive(event) and \
                            not chair.receive(event) and not bookshelf.receive(event) and \
                            not safe.receive(event) and not hole_floor.receive(event) and \
                            not crafttable.receive(event) and not knife_case.receive(event) and \
                            not eating_table.receive(event) and not fridge.receive(event) and \
                            not cookcase.receive(event) and not gas_oven.receive(event) and \
                            not shrine.receive(event) and not bot.receive(event):
                        text_message.receive(event)

                screen.fill((r, g, b))

                ground_group.draw(screen)
                floor_group.draw(screen)
                interior_group.draw(screen)
                no_clip_group.draw(screen)
                ghost_group.draw(screen)
                player_group.draw(screen)
                mini_floor_group.draw(screen)
                button_group.draw(screen)
                inventory_group.draw(screen)
                message_group.draw(screen)

                men.update()
                text_message.update()
                bag.update()
                bot.update()

                screen.blit(cursor, (mouse_x, mouse_y))

                if END_GAME and text_message.is_hide:
                    screen.fill((r, g, b))
                    r = int(r * 0.9)
                    g = int(g * 0.9)
                    b = int(b * 0.9)
                if r == b == g == 0:
                    TIME = dt.datetime.now() - TIME
                    break
                pygame.display.flip()
                clock.tick(FPS)
            if END_GAME:
                end_game(TIME)
        else:
            break
