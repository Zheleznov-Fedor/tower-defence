import pygame
from Functions import load_image

MISSILES = {
    'Rocket': {
        'image_filename': 'Rocket.png',  # Название файла картинки боеприпаса
        'width_in_match': 20,  # Ширина картинки боеприпаса в матче
        'is_need_rotate': True,  # Нужен ли поворот при перемещении к цели
        'step': 10  # Скорость боеприпаса
    },
    'Bullet': {
        'image_filename': 'Bullet.png',
        'width_in_match': 40,
        'is_need_rotate': False,
        'step': 30
    }
}


class Missile(pygame.sprite.Sprite):
    def __init__(self, group, missile_name, tower, enemy):
        super().__init__(group)
        self.orig_image = load_image(f'./defense/' + MISSILES[missile_name]['image_filename'])
        self.image = load_image(f'./defense/' + MISSILES[missile_name]['image_filename'])
        self.tower = tower
        self.enemy = enemy
        size = MISSILES[missile_name]['width_in_match']
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (size, self.rect.height / self.rect.width * size))
        self.orig_image = pygame.transform.scale(self.orig_image, (size, self.rect.height / self.rect.width * size))
        self.rect = self.image.get_rect()
        self.rect.x = tower.x
        self.rect.y = tower.y
        self.is_need_rotate = MISSILES[missile_name]['is_need_rotate']
        self.step = MISSILES[missile_name]['step']

    def point_at(self, x, y):
        direction = pygame.math.Vector2(x, y) - self.rect.center
        angle = direction.angle_to((0, -1))
        self.image = pygame.transform.rotate(self.orig_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self, *args):
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

