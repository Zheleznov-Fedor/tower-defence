import pygame
from Utils import load_image, MISSILES_INFO


class Missile(pygame.sprite.Sprite):
    def __init__(self, group, missile_name, tower, enemy):
        super().__init__(group)
        self.orig_image = load_image(f'./defense/' + MISSILES_INFO[missile_name]['image_filename'])
        self.image = load_image(f'./defense/' + MISSILES_INFO[missile_name]['image_filename'])
        self.tower = tower
        self.enemy = enemy
        size = MISSILES_INFO[missile_name]['width_in_match']
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (size, self.rect.height / self.rect.width * size))
        self.orig_image = pygame.transform.scale(self.orig_image, (size, self.rect.height / self.rect.width * size))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = tower.rect.center
        self.is_need_rotate = MISSILES_INFO[missile_name]['is_need_rotate']
        self.step = MISSILES_INFO[missile_name]['step']

    def point_at(self, x, y):
        direction = pygame.math.Vector2(x, y) - self.rect.center
        angle = direction.angle_to((0, -1))
        self.image = pygame.transform.rotate(self.orig_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self, *args):
        if self.enemy.alive():
            if not pygame.sprite.collide_mask(self, self.enemy):
                if self.enemy.rect.x > self.rect.x:
                    self.rect.x += self.step
                elif self.enemy.rect.x != self.rect.x:
                    self.rect.x -= self.step
                if self.enemy.rect.y > self.rect.y:
                    self.rect.y += self.step
                elif self.enemy.rect.y != self.rect.y:
                    self.rect.y -= self.step

                if self.is_need_rotate:
                    self.point_at(self.enemy.rect.x, self.enemy.rect.y)
            else:
                if self.enemy.damage(self.tower.shoot_damage):
                    self.tower.find_target()
                self.kill()
        else:
            self.kill()
