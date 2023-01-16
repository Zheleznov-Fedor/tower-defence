import pygame
from Functions import load_image, TILE_SIZE
from ShootingTower import TOWERS_INFO


class FarmTower(pygame.sprite.Sprite):
    def __init__(self, group, x, y, add_money):
        super().__init__(group)
        self.add_money = add_money
        self.image = load_image('./defense/' + TOWERS_INFO['Farm']['image_filename'])
        size = TOWERS_INFO['Farm']['max_size_in_match']

        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (size, self.rect.height / self.rect.width * size))

        # Кастомные настройки каждой башни
        self.x_offset = TOWERS_INFO['Farm']['x_offset']
        self.y_offset = TOWERS_INFO['Farm']['y_offset']
        self.income = TOWERS_INFO['Farm']['income']

        self.rect.x = x * TILE_SIZE + self.x_offset
        self.rect.y = y * TILE_SIZE + self.y_offset

    def give_money(self):
        self.add_money(self.income)
