import pygame
from Utils import load_image, TILE_SIZE, TOWERS_INFO
from Missile import Missile


class ShootingTower(pygame.sprite.Sprite):
    """Класс стреляющей башни"""
    def __init__(self, group, tower_name, x, y, enemies, missiles):
        super().__init__(group)
        self.missiles = missiles
        self.tower_name = tower_name

        # Кастомные настройки каждой башни (подробности в TOWERS_INFO)
        self.x_offset = TOWERS_INFO[tower_name]['x_offset']
        self.y_offset = TOWERS_INFO[tower_name]['y_offset']

        self.x = x * TILE_SIZE + self.x_offset
        self.y = y * TILE_SIZE + self.y_offset

        self.level = -1
        self.update_level()

        self.center = self.rect.center

        self.enemies = enemies
        self.target = None
        self.found_time = 0
        self.last_damage = 0

    def rotate_to_point(self, x, y):
        """Поворачивает башню к точке"""
        direction = pygame.math.Vector2(x, y) - self.center
        angle = direction.angle_to((0, -1))
        self.image = pygame.transform.rotate(self.orig_image, angle)
        self.rect = self.image.get_rect(center=self.center)

    def check_visibility(self, other):
        """Проверяет виден ли для башни пришелец"""
        return (other.rect.x - self.rect.x) ** 2 / self.visible_radius ** 2 + \
            (other.rect.y - self.rect.y) ** 2 / self.visible_radius ** 2 < 1

    def find_target(self):
        """Ищет новую цель"""
        for enemy in self.enemies:
            if self.check_visibility(enemy):
                self.target = enemy
                self.found_time = pygame.time.get_ticks()
                break

    def update(self, *args):
        if self.target and self.target.hp > 0:  # если цель есть и её здоровье больше 0
            if self.check_visibility(self.target):  # если она до сих пор её видит
                self.rotate_to_point(self.target.rect.x, self.target.rect.y)
                if pygame.time.get_ticks() - self.last_damage >= self.shoot_delay:  # и если она успела перезарядиться
                    self.last_damage = pygame.time.get_ticks()
                    Missile(self.missiles, self.missile_type, self, self.target)  # выпускаем боеприпас
            else:
                self.find_target()  # иначе поиск новой цели
        else:
            self.find_target()  # иначе поиск новой цели

    def update_price(self):
        """Возвращает цену обновления"""
        return TOWERS_INFO[self.tower_name]['levels'][self.level - 1].get('update_price', 0)

    def update_level(self):
        """Обновляет уровень и сопутсвующие харрактеристики"""
        self.level += 1

        self.image = load_image('./defense/' + TOWERS_INFO[self.tower_name]['levels'][self.level]['image_filename'])
        self.orig_image = load_image(
            './defense/' + TOWERS_INFO[self.tower_name]['levels'][self.level]['image_filename'])
        size = TOWERS_INFO[self.tower_name]['max_size_in_match']

        self.rect = self.image.get_rect()
        if self.rect.height / self.rect.width * size < size:
            self.image = pygame.transform.scale(self.image, (size, self.rect.height / self.rect.width * size))
            self.orig_image = pygame.transform.scale(self.orig_image, (size, self.rect.height / self.rect.width * size))
        else:
            self.image = pygame.transform.scale(self.image, (self.rect.width / self.rect.height * size, size))
            self.orig_image = pygame.transform.scale(self.orig_image, (self.rect.width / self.rect.height * size, size))

        self.rect.x = self.x
        self.rect.y = self.y

        self.visible_radius = TOWERS_INFO[self.tower_name]['levels'][self.level]['visible_radius']
        self.shoot_delay = TOWERS_INFO[self.tower_name]['levels'][self.level]['shoot_delay']
        self.shoot_damage = TOWERS_INFO[self.tower_name]['levels'][self.level]['shoot_damage']
        self.missile_type = TOWERS_INFO[self.tower_name]['levels'][self.level]['missile_type']

    def delete(self):
        """Удалить башню"""
        self.kill()

    def is_updateable(self):
        """Проверяет обновляема ли башня"""
        return len(TOWERS_INFO[self.tower_name]['levels']) - 1 > self.level

    def coords(self):
        """Возвращает координаты башни"""
        return (self.x, self.y)

    def size(self):
        """Возвращает размер башни"""
        return (self.rect.width, self.rect.height)

    def price(self):
        """Возвращает сколько денег вернётся за её удаление"""
        return int(TOWERS_INFO[self.tower_name]['price'] / 2 + sum(
            [TOWERS_INFO[self.tower_name]['levels'][i]['update_price'] / 2
             for i in range(len(TOWERS_INFO[self.tower_name]['levels']))
             if i < self.level]))
