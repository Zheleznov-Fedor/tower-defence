import pygame
from Utils import load_image, TILE_SIZE
from ShootingTower import TOWERS_INFO


class FarmTower(pygame.sprite.Sprite):
    def __init__(self, group, x, y, add_money):
        super().__init__(group)
        self.add_money = add_money

        # Кастомные настройки каждой башни
        self.x_offset = TOWERS_INFO['Farm']['x_offset']
        self.y_offset = TOWERS_INFO['Farm']['y_offset']

        self.x = x * TILE_SIZE + self.x_offset
        self.y = y * TILE_SIZE + self.y_offset
        self.level = -1
        self.update_level()

    def give_money(self):
        self.add_money(self.income)

    def update_level(self):
        self.level += 1

        self.image = load_image('./defense/' + TOWERS_INFO['Farm']['levels'][0]['image_filename'])
        size = TOWERS_INFO['Farm']['max_size_in_match']
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (size, self.rect.height / self.rect.width * size))

        self.rect.x = self.x
        self.rect.y = self.y

        self.income = TOWERS_INFO['Farm']['levels'][0]['income']

        return TOWERS_INFO['Farm']['levels'][self.level - 1].get('update_price', 0)

    def delete(self):
        self.kill()

    def coords(self):
        return (self.x, self.y)

    def size(self):
        return (self.rect.width, self.rect.height)

    def is_updateable(self):
        return len(TOWERS_INFO['Farm']['levels']) - 1 > self.level

    def price(self):
        return int(TOWERS_INFO['Farm']['price'] / 2 + sum([TOWERS_INFO['Farm']['levels'][i]['update_price'] / 2
                                                       for i in range(len(TOWERS_INFO['Farm']['levels']))
                                                       if i < self.level]))
