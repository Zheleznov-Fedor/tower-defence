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
        self.image = load_image('./enemy/0.png')
        size = 100
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect()
        self.start = (size * -0.5 - 24, size * 0.5)
        self.rect.x = size * -0.5 - 24
        self.rect.y = size * 0.5
        self.path = [(1, 0, 0), (2, 0, 0), (3, 0, 0), (4, 0, 0), (4, 1, 1), (4, 2, 0)]
        self.path_pos = 0
        self.grid_pos = (0, 0)
        print(self.grid_pos)

    def update(self, *args):
        if self.path_pos < len(self.path):
            if self.rect.x - self.start[0] != 100 and self.rect.y - self.start[1] != 100:
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
                if self.path[self.path_pos][2]:
                    self.image = pygame.transform.rotate(self.image, -90)
                print(self.grid_pos)

            # if self.rect.x - self.start[0] != 100:
            #     self.rect.x += 1
            # else:
            #     self.grid_pos[0] += 1
            #     self.path_pos += 1
            #     self.start = (self.rect.x, self.rect.y)
            #     print(self.grid_pos)


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption('Map test')

    running = True
    fps = 120
    clock = pygame.time.Clock()

    all_sprites = pygame.sprite.Group()

    build_map('test.csv', all_sprites)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                all_sprites.update(event)

        screen.fill((255, 255, 255))

        all_sprites.draw(screen)

        clock.tick(fps)
        pygame.display.flip()

    pygame.quit()
