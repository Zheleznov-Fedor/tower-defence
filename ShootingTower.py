import pygame
from Functions import load_image, TILE_SIZE
from Missile import Missile

TOWERS_INFO = {  # Настройки каждой башни
    'Solider':  # У Мити опечатка, правильно Soldier
        {
            'image_filename': 'Solider2.png',  # Название файла картинки башни
            'price': 200,  # Цена внутри матча
            'place_type': 'default',  # Тип места размещения
            'x_offset': 0,  # Сдвиг по горизонтали, для правильного размещения
            'y_offset': 0,  # Сдвиг по вертикали, для правильного размещения
            'visible_radius': 250,  # Радиус на котором башня видит противников
            'shoot_delay': 400,  # Время перезарядки
            'shoot_damage': 15,  # Урон выстрела
            'x_center_offset': 0,  # Сдвиг центра по горизонтали, для правильного поворота
            'y_center_offset': 0,  # Сдвиг центра по вертикали, для правильного поворота
            'missile_type': 'Rocket',  # Тип боеприпаса
            'max_size_in_match': 80,  # Максимальный размер картинки башни в матче
        },
    'Gun':
        {
            'image_filename': 'Gun2.png',
            'price': 300,
            'place_type': 'default',
            'x_offset': 0,
            'y_offset': 0,
            'visible_radius': 250,
            'shoot_delay': 400,
            'shoot_damage': 15,
            'x_center_offset': 0,
            'y_center_offset': 0,
            'missile_type': 'Bullet',
            'max_size_in_match': 80
        },
    'Plane':
        {
            'image_filename': 'Plane2.png',
            'price': 400,
            'place_type': 'default',
            'x_offset': 0,
            'y_offset': 0,
            'visible_radius': 250,
            'shoot_delay': 400,
            'shoot_damage': 15,
            'x_center_offset': 0,
            'y_center_offset': 0,
            'missile_type': 'Rocket',
            'max_size_in_match': 80
        },
    'Laser':
        {
            'image_filename': 'Laser2.png',
            'price': 500,
            'place_type': 'default',
            'x_offset': 0,
            'y_offset': 0,
            'visible_radius': 250,
            'shoot_delay': 400,
            'shoot_damage': 15,
            'x_center_offset': 0,
            'y_center_offset': 0,
            'missile_type': 'Rocket',
            'max_size_in_match': 80
        },
    'Farm':
        {
            'image_filename': 'Farm2.png',
            'price': 750,
            'place_type': 'farm',
            'x_offset': 37,
            'y_offset': 10,
            'max_size_in_match': 25,
            'income': 300  # Доход приносимый фермой в начале каждой волны
        },
}


class ShootingTower(pygame.sprite.Sprite):
    def __init__(self, group, tower_name, x, y, enemies, missiles):
        super().__init__(group)
        self.image = load_image('./defense/' + TOWERS_INFO[tower_name]['image_filename'])
        self.orig_image = load_image('./defense/' + TOWERS_INFO[tower_name]['image_filename'])
        size = TOWERS_INFO[tower_name]['max_size_in_match']
        self.missiles = missiles
        self.rect = self.image.get_rect()
        if self.rect.height / self.rect.width * size < size:
            self.image = pygame.transform.scale(self.image, (size, self.rect.height / self.rect.width * size))
            self.orig_image = pygame.transform.scale(self.orig_image, (size, self.rect.height / self.rect.width * size))
        else:
            self.image = pygame.transform.scale(self.image, (self.rect.width / self.rect.height * size, size))
            self.orig_image = pygame.transform.scale(self.orig_image, (self.rect.width / self.rect.height * size, size))

        # Кастомные настройки каждой башни (подробности в TOWERS_INFO)
        self.x_offset = TOWERS_INFO[tower_name]['x_offset']
        self.y_offset = TOWERS_INFO[tower_name]['y_offset']
        self.visible_radius = TOWERS_INFO[tower_name]['visible_radius']
        self.shoot_delay = TOWERS_INFO[tower_name]['shoot_delay']
        self.shoot_damage = TOWERS_INFO[tower_name]['shoot_damage']
        self.x_center_offset = TOWERS_INFO[tower_name]['x_center_offset']
        self.y_center_offset = TOWERS_INFO[tower_name]['y_center_offset']
        self.missile_type = TOWERS_INFO[tower_name]['missile_type']

        self.x = x * TILE_SIZE + self.x_offset
        self.y = y * TILE_SIZE + self.y_offset
        self.rect.x = x * TILE_SIZE + self.x_offset
        self.rect.y = y * TILE_SIZE + self.y_offset

        self.enemies = enemies
        self.target = None
        self.found_time = 0
        self.last_damage = 0

    def point_at(self, x, y):
        direction = pygame.math.Vector2(x, y) - (self.rect.x + self.x_center_offset, self.rect.y + self.y_center_offset)
        angle = direction.angle_to((0, -1))
        self.image = pygame.transform.rotate(self.orig_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

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
