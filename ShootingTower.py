import pygame
from Utils import load_image, TILE_SIZE, TOWERS_INFO
from Missile import Missile


class ShootingTower(pygame.sprite.Sprite):
    def __init__(self, group, tower_name, x, y, enemies, missiles):
        super().__init__(group)
        self.missiles = missiles
        self.tower_name = tower_name

        # Кастомные настройки каждой башни (подробности в TOWERS_INFO)
        self.x_offset = TOWERS_INFO[tower_name]['x_offset']
        self.y_offset = TOWERS_INFO[tower_name]['y_offset']
        self.x_center_offset = TOWERS_INFO[tower_name]['x_center_offset']
        self.y_center_offset = TOWERS_INFO[tower_name]['y_center_offset']

        self.x = x * TILE_SIZE + self.x_offset
        self.y = y * TILE_SIZE + self.y_offset

        self.level = -1
        self.update_level()

        self.center = self.rect.center  # (self.rect.x + 0, self.rect.y + 0)

        self.enemies = enemies
        self.target = None
        self.found_time = 0
        self.last_damage = 0

    def rot(self, x, y):
        if self.x_center_offset:
            print(self.center, (self.rect.x + self.x_center_offset, self.rect.y + self.y_center_offset),
                  self.rect.width, self.rect.height)
            direction = pygame.math.Vector2(x, y) - self.center
            angle = direction.angle_to((0, -1))
            self.image = pygame.transform.rotate(self.orig_image, angle)
            self.rect = self.image.get_rect(center=self.center)
        else:
            print(self.rect.center)
            direction = pygame.math.Vector2(x, y) - self.rect.center
            angle = direction.angle_to((0, -1))
            self.image = pygame.transform.rotate(self.orig_image, angle)
            self.rect = self.image.get_rect(center=self.rect.center)

    def point_at(self, x, y):
        direction = pygame.math.Vector2(x, y) - self.rect.center
        angle = direction.angle_to((0, -1))
        self.image = pygame.transform.rotozoom(self.orig_image, angle, 1)
        offset_rotated = pygame.math.Vector2(self.x_center_offset, self.y_center_offset).rotate(angle)
        self.rect = self.image.get_rect(center=self.center + offset_rotated)

    def check_visibility(self, other):
        return (other.rect.x - self.rect.x) ** 2 / self.visible_radius ** 2 + \
            (other.rect.y - self.rect.y) ** 2 / self.visible_radius ** 2 < 1

    def find_target(self):
        for enemy in self.enemies:
            if self.check_visibility(enemy):
                self.target = enemy
                self.found_time = pygame.time.get_ticks()
                break

    def update(self, *args):
        if self.target and self.target.hp > 0:
            if self.check_visibility(self.target):
                self.point_at(self.target.rect.x, self.target.rect.y)
                if pygame.time.get_ticks() - self.last_damage >= self.shoot_delay:
                    self.last_damage = pygame.time.get_ticks()
                    Missile(self.missiles, self.missile_type, self, self.target)
            else:
                self.find_target()
        else:
            self.find_target()

    def update_level(self):
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

        return TOWERS_INFO[self.tower_name]['levels'][self.level - 1].get('update_price', 0)

    def delete(self):
        self.kill()

    def is_updateable(self):
        return len(TOWERS_INFO[self.tower_name]['levels']) - 1 > self.level

    def coords(self):
        return (self.x, self.y)

    def size(self):
        return (self.rect.width, self.rect.height)

    def price(self):
        return int(TOWERS_INFO[self.tower_name]['price'] / 2 + sum(
            [TOWERS_INFO[self.tower_name]['levels'][i]['update_price'] / 2
             for i in range(len(TOWERS_INFO[self.tower_name]['levels']))
             if i < self.level]))
