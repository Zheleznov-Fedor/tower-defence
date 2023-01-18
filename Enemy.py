import pygame
from Utils import load_image, TILE_SIZE, ENEMIES_INFO


class Enemy(pygame.sprite.Sprite):
    """Класс Пришельца"""
    def __init__(self, group, lvl, map_w, map_h, path, game_lose_heart, add_money):
        super().__init__(group)
        self.game_lose_heart = game_lose_heart  # Функция убирания одного сердечка
        self.add_money = add_money  # Функция добавления денег
        self.orig_image = load_image('./enemy/' + ENEMIES_INFO[lvl]['image_filename'])
        self.image = load_image('./enemy/' + ENEMIES_INFO[lvl]['image_filename'])

        height = ENEMIES_INFO[lvl]['height']
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (height * self.rect.width / self.rect.height, height))
        self.orig_image = pygame.transform.scale(self.orig_image, (height * self.rect.width / self.rect.height, height))

        self.start = (path[0][0] * 100, (1 + path[0][1]) * 100 - 50 * 0.5)  # Стартовые координаты
        self.map_w = map_w  # Ширина карты в тайлах
        self.map_h = map_h  # Длина карты в тайлах
        if path[0][0] == map_w - 1:
            self.rect.x = map_w * TILE_SIZE
        else:
            self.rect.x = -60
        self.rect.y = self.start[1]

        self.step = ENEMIES_INFO[lvl]['step']  # Шаг за один update при движении по прямой
        self.rot_speed = ENEMIES_INFO[lvl]['angle_step']  # Шаг за один update при повороте
        self.hp = ENEMIES_INFO[lvl]['hp']  # Здоровье
        self.max_hp = ENEMIES_INFO[lvl]['hp']  # Максимальное возможное здоровье
        self.needs_rotate = ENEMIES_INFO[lvl]['needs_rotate']  # Нужно ли поворачить картинку при повороте

        self.path = path  # Путь движения по карте
        self.path_pos = 1  # Индекс места пути к которому стремится
        self.grid_pos = self.path[0]  # На каком месте по пути стоит
        self.is_came_out = False  # Вышел ли из-за края карты
        self.is_rotating = False  # Поворачивается ли сейчас
        self.rotating_direction = 0  # Направление поворота (-1 - лево, 1 - право)
        self.rotating_pos = 0  # Позиция в повороте

        # Поворот картинки для правильного выхода из за края карты
        if self.path[self.path_pos][0] < self.grid_pos[0]:
            self.image = pygame.transform.rotate(self.orig_image, -180)
        elif self.path[self.path_pos][1] > self.grid_pos[1]:
            self.image = pygame.transform.rotate(self.orig_image, 90)
        elif self.path[self.path_pos][1] != self.grid_pos[1]:
            self.image = pygame.transform.rotate(self.orig_image, -90)

    def bezier(self, p0, p1, p2, t):
        """Определяет координаты положения на кривой, образованной по трём точкам, в момент времени t"""
        p0 = [p0[0] * 100, (1 + p0[1]) * 100 - 50 * 0.5]
        p1 = [p1[0] * 100, (1 + p1[1]) * 100 - 50 * 0.5]
        p2 = [p2[0] * 100, (1 + p2[1]) * 100 - 50 * 0.5]
        px = p0[0] * (1 - t) ** 2 + 2 * (1 - t) * t * p1[0] + p2[0] * t ** 2
        py = p0[1] * (1 - t) ** 2 + 2 * (1 - t) * t * p1[1] + p2[1] * t ** 2
        return px, py

    def rot_center(self, angle):
        """Поворачивает картинку на угол angle"""
        self.image = pygame.transform.rotate(self.orig_image, angle)

    def rotation_direction(self, args):
        """Определяет направление поворота по трём точкам (-1 - лево, 1 - право)"""
        x1, y1, x2, y2, x3, y3 = args
        if y2 > y1:
            if x3 > x1:
                return -1
            return 1
        elif y1 > y2:
            if x3 > x1:
                return 1
            return -1
        elif y1 == y2:
            if y3 > y1:
                return 1
            return -1

    def update(self, *args):
        if not self.is_came_out:  # Выход из-за карты
            if self.path[self.path_pos][0] > self.grid_pos[0]:
                self.rect.x += self.step
                if self.rect.x == 0:
                    self.is_came_out = True
            elif self.path[self.path_pos][0] != self.grid_pos[0]:
                self.rect.x -= self.step

                if self.rect.x == self.map_w * TILE_SIZE:
                    self.is_came_out = True
            elif self.path[self.path_pos][1] > self.grid_pos[1]:
                self.rect.y += self.step

                if self.rect.y == 0:
                    self.is_came_out = True
            elif self.path[self.path_pos][1] != self.grid_pos[1]:
                self.rect.y -= self.step

                if self.rect.h == self.map_h * TILE_SIZE:
                    self.is_came_out = True
        elif self.path_pos < len(self.path):  # Если весь путь ещё не пройден
            if self.is_rotating:  # Проверяем поворачиваемся, ли мы сейчас
                self.rect.x, self.rect.y = self.bezier(*self.path[self.path_pos:self.path_pos + 3],
                                                       round(self.rotating_pos / 90, 3))
                self.rotating_pos = round(self.rotating_pos + self.rot_speed, 3)

                if self.needs_rotate:
                    self.rot_center(-self.rotating_pos * self.rotating_direction)
                if self.rotating_pos == 90:
                    if self.needs_rotate:
                        self.orig_image = pygame.transform.rotate(self.orig_image, -90 * self.rotating_direction)
                    self.rotating_pos = 0
                    self.is_rotating = False
                    self.path_pos += 2
            elif abs(self.rect.x - self.start[0]) != 100 and abs(self.rect.y - self.start[1]) != 100:
                # Если не поворачиваемся, и не дошли до определённого места пути
                if self.path[self.path_pos][0] > self.grid_pos[0]:
                    self.rect.x += self.step
                elif self.path[self.path_pos][0] != self.grid_pos[0]:
                    self.rect.x -= self.step
                if self.path[self.path_pos][1] > self.grid_pos[1]:
                    self.rect.y += self.step
                elif self.path[self.path_pos][1] != self.grid_pos[1]:
                    self.rect.y -= self.step
            else:  # Иначе задаём, либо новую точку к которой двигаться, либо поворачиваться
                self.grid_pos = self.path[self.path_pos]
                self.path_pos += 1
                self.start = (self.rect.x, self.rect.y)

                if self.path_pos < len(self.path):
                    self.is_rotating = self.path[self.path_pos][2]
                    if self.is_rotating:
                        res = []
                        for elem in [elem[0:2] for elem in self.path[self.path_pos: self.path_pos + 3]]:
                            res.extend(elem)
                        self.rotating_direction = self.rotation_direction(res)
        else:  # Выходим за край карты, забираем сердечко и кмираем
            if self.path[-1][0] > self.path[-2][0]:
                self.rect.x += self.step

                if self.rect.x == self.map_w * TILE_SIZE + 15:
                    self.game_lose_heart()
                    self.kill()
            elif self.path[-1][0] != self.path[-2][0]:
                self.rect.x -= self.step

                if self.rect.x == -15:
                    self.game_lose_heart()
                    self.kill()
            if self.path[-1][1] > self.path[-2][1]:
                self.rect.y += self.step

                if self.rect.y == self.map_h * TILE_SIZE + 15:
                    self.game_lose_heart()
                    self.kill()
            elif self.path[-1][1] != self.path[-2][1]:
                self.rect.y -= self.step

                if self.rect.y == -15:
                    self.game_lose_heart()
                    self.kill()

    def draw(self, screen):
        """Рисует шкалу здоровья"""
        pygame.draw.rect(screen, (255, 0, 0), (self.rect.x - 5, self.rect.y - 20, 60, 10))
        pygame.draw.rect(screen, (0, 255, 0), (self.rect.x - 5, self.rect.y - 20, 60 / self.max_hp * self.hp, 10))
        pygame.draw.rect(screen, (0, 0, 0), (self.rect.x - 5, self.rect.y - 20, 60, 10), 2)

    def damage(self, value):
        """Наносит урон, если здоровье не больше 0, приносим деньги зп убийство и умираем"""
        self.hp -= value

        if self.hp <= 0:
            self.add_money(20)
            self.kill()
            return -1
