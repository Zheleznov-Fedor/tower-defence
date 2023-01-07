import pygame
from Functions import load_image, TILE_SIZE
from math import atan2, degrees, pi


class Tower(pygame.sprite.Sprite):
    def __init__(self, group, type,  x, y, enemies):
        super().__init__(group)
        self.orig_image = load_image('./defense/' + type)
        self.image = load_image('./defense/' + type)
        size = 80
        self.image = pygame.transform.scale(self.image, (size, size))
        self.orig_image = pygame.transform.scale(self.orig_image, (size, size))
        self.rect = self.image.get_rect()
        self.x = x * TILE_SIZE + 10
        self.y = y * TILE_SIZE + 2
        self.rect.x = x * TILE_SIZE + 10
        self.rect.y = y * TILE_SIZE + 2
        self.enemies = enemies
        self.target = None
        self.found_time = 0
        self.last_damage = 0

    def point_at(self, x, y):
        direction = pygame.math.Vector2(x, y) - self.rect.center
        angle = direction.angle_to((0, -1))
        self.image = pygame.transform.rotate(self.orig_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def check_visibility(self, other):
        return (other.rect.x - self.rect.x) ** 2 / 200 ** 2 + (other.rect.y - self.rect.y) ** 2 / 200 ** 2 < 1

    def find_target(self):
        for enemy in self.enemies:
            if self.check_visibility(enemy):
                self.target = enemy
                self.found_time = pygame.time.get_ticks()

    def update(self, *args):
        if self.target:
            if self.check_visibility(self.target):
                self.point_at(self.target.rect.x + 10, self.target.rect.y + 20)
                if pygame.time.get_ticks() - self.found_time >= 150 and \
                        pygame.time.get_ticks() - self.last_damage >= 750:
                    self.last_damage = pygame.time.get_ticks()
                    if self.target.damage(25):
                        self.find_target()
            else:
                self.find_target()
        else:
            self.find_target()
