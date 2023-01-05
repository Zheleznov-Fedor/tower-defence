import os
import sys
import pygame
import csv


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()

    return image


def parse_tile(code):
    types = {
        'R': '/road',
        'D': '/decor',
        'P': '/place'
    }
    biomes = {
        'gg': '/grassgrass',
        'dd': '/desertdesert',
        'ss': '/stonestone',
        'rr': '/redred',
        'gd': '/grassdesert',
        'gs': '/desertstone',
        'gr': '/stonered',
        'dg': '/desertgrass',
        'ds': '/desertstone',
        'dr': '/desertred',
        'sg': '/stonegrass',
        'sd': '/stonedesert',
        'sr': '/stonered',
        'rg': '/redgrass',
        'rd': '/reddesert',
        'rs': '/redstone'
    }
    materials = {
        's': '/stone',
        'g': '/grass'
    }
    place_materials = {
        'gf': '/grassfill',
        'gd': '/grassdirty',
        'df': '/desertfill',
        'dd': '/desertdirty'
    }

    if code[0] == 'R':
        return types[code[0]] + biomes[code[1:3]] + '/' + str(int(code[3:5])) + '.png'
    elif code[0] == 'D':
        return types[code[0]] + materials[code[1]] + '/' + str(int(code[2:4])) + '.png'
    elif code[0] == 'P':
        return types[code[0]] + place_materials[code[1:3]] + '/' + str(int(code[3:5])) + '.png'


def load_map(filname):
    with open(filname, encoding="utf8") as file:
        reader = csv.reader(file, delimiter=';', quotechar='"')
        res = {
            'land': [],
            'decor': []}
        r = list(reader)
        w, h = map(int, r[0])

        for i in range(1, h + 1):
            res['land'].append(r[i + 1])

        for elem in r[h + 2:]:
            res['decor'].append({
                'code': elem[0],
                'x': float(elem[1]),
                'y': float(elem[2]),
            })

        return res


def build_map(filename, sprite_group):
    map = load_map(filename)
    land = map['land']
    decor = map['decor']

    for y in range(len(land)):
        for x in range(len(land[0])):
            Tile(sprite_group, land[y][x], x, y)

    for elem in decor:
        Tile(sprite_group, elem['code'], elem['x'], elem['y'])


class Tile(pygame.sprite.Sprite):
    def __init__(self, group, code, x, y):
        super().__init__(group)
        self.image = load_image('.' + parse_tile(code))
        size = 100
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect()
        self.rect.x = size * x
        self.rect.y = size * y

    def update(self, *args):
        pass


class Enemy(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.orig_image = load_image('./enemy/0.png')
        self.image = load_image('./enemy/0.png')
        height = 50
        self.image = pygame.transform.scale(self.image, (48 * height / 56, height))
        self.orig_image = pygame.transform.scale(self.orig_image, (48 * height / 56, height))
        self.rect = self.image.get_rect()

        self.start = (-36, 100 - 50 * 0.5)
        self.rect.x = self.start[0]
        self.rect.y = self.start[1]
        self.rect.w = 30
        self.rect.width = 30

        self.path = [(1, 0, 0), (2, 0, 0), (3, 0, 0), (3, 0, 1), (4, 0, 0), (4, 1, 0), (4, 1, 1), (4, 2, 0), (3, 2, 0), (2, 2, 0), (1, 2, 0), (0, 2, 0)]
        self.path_pos = 0
        self.grid_pos = (0, 0)
        self.is_came_out = True
        self.is_rotating = False
        self.rotating_direction = 0
        self.rotating_pos = 0

    def bezier(self, p0, p1, p2, t):
        p0 = [64 + (p0[0] - 1) * 100, 75 + (p0[1]) * 100]
        p1 = [64 + (p1[0] - 1) * 100, 75 + (p1[1]) * 100]
        p2 = [64 + (p2[0] - 1) * 100, 75 + (p2[1]) * 100]
        print(p0, p1, p2)
        px = p0[0] * (1 - t) ** 2 + 2 * (1 - t) * t * p1[0] + p2[0] * t ** 2
        py = p0[1] * (1 - t) ** 2 + 2 * (1 - t) * t * p1[1] + p2[1] * t ** 2
        return px, py

    def rot_center(self, angle):
        self.image = pygame.transform.rotate(self.orig_image, angle)

    def update(self, *args):
        if not self.is_came_out:
            if self.path[0][0] > self.grid_pos[0]:
                self.rect.x += 1

                if self.rect.x == 0:
                    self.is_came_out = True
            elif self.path[0][0] != self.grid_pos[0]:
                self.rect.x -= 1
            elif self.path[0][1] > self.grid_pos[1]:
                self.rect.y += 1

                if self.rect.y == 0:
                    self.is_came_out = True
            elif self.path[0][1] != self.grid_pos[1]:
                self.rect.y -= 1
        elif self.path_pos < len(self.path):
            if self.is_rotating:
                self.rect.x, self.rect.y = self.bezier(*self.path[self.path_pos:self.path_pos + 3],
                                                       round(self.rotating_pos / 180, 3))
                self.rotating_pos = round(self.rotating_pos + 0.9, 3)
                self.rot_center(-self.rotating_pos / 2 * self.rotating_direction)
                if self.rotating_pos == 180:
                    self.orig_image = pygame.transform.rotate(self.orig_image, -90 * self.rotating_direction)
                    self.rotating_pos = 0
                    self.is_rotating = False
                    self.path_pos += 2
            elif self.rect.x - self.start[0] != 100 and self.rect.y - self.start[1] != 100:
                if self.path[self.path_pos][0] > self.grid_pos[0]:
                    self.rect.x += 1
                elif self.path[self.path_pos][0] != self.grid_pos[0]:
                    self.rect.x -= 1
                if self.path[self.path_pos][1] > self.grid_pos[1]:
                    self.rect.y += 1
                elif self.path[self.path_pos][1] != self.grid_pos[1]:
                    self.rect.y -= 1
            else:
                self.grid_pos = self.path[self.path_pos]
                self.path_pos += 1
                self.start = (self.rect.x, self.rect.y)
                if self.path_pos < len(self.path):
                    self.is_rotating = self.path[self.path_pos][2]
                    if self.is_rotating:
                        self.rotating_direction = self.is_rotating


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption('Map test')

    running = True
    fps = 90
    clock = pygame.time.Clock()

    all_sprites = pygame.sprite.Group()

    build_map('test.csv', all_sprites)
    x = Enemy(all_sprites)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                all_sprites.update(event)

        screen.fill((255, 255, 255))

        x.update()
        all_sprites.draw(screen)

        clock.tick(fps)
        pygame.display.flip()

    pygame.quit()
