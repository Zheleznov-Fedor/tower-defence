import pygame
import csv
from Utils import load_image, TILE_SIZE


def parse_tile(code):
    """Преобразует код тайла в путь к картинке"""
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
    """Загружает файл карты и строит словарь карты"""
    with open(filname, encoding="utf8") as file:
        reader = csv.reader(file, delimiter=';', quotechar='"')
        tower_places_types = {
            0: 'default',
            3: 'farm'
        }
        res = {
            'w': 0,
            'h': 0,
            'land': [],
            'decor': [],
            'enemy_path': [],
            'tower_places': []
        }
        r = list(reader)
        w, h = map(int, r[0])
        res['w'] = w
        res['h'] = h

        for i in range(1, h + 1):
            for x in range(w):
                if r[i][x][0] == 'P':
                    res['tower_places'].append((x, i - 1, tower_places_types[int(r[i][x][3:5])]))
            res['land'].append(r[i])

        decor_count = int(r[h + 1][0])

        for elem in r[h + 2:h + decor_count + 2]:
            res['decor'].append({
                'code': elem[0],
                'x': float(elem[1]),
                'y': float(elem[2]),
            })

        res['enemy_path'] = [list(map(int, point.split(','))) for point in r[h + decor_count + 2]]

        return res


def build_map(filename, sprite_group):
    """Рисует карту"""
    map = load_map(filename)
    land = map['land']
    decor = map['decor']

    for y in range(len(land)):
        for x in range(len(land[0])):
            Tile(sprite_group, land[y][x], x, y)

    for elem in decor:
        Tile(sprite_group, elem['code'], elem['x'], elem['y'], 'decor')

    return map


def get_waves(waves):
    """Берёт волны из файла и возвращает первые waves штук"""
    f = open('txt/waves.txt')
    lines = f.readlines()
    f.close()
    return list(map(str.strip, lines))[:waves]


class Tile(pygame.sprite.Sprite):
    """Класс тайла карты"""
    def __init__(self, group, code, x, y, type='land'):
        super().__init__(group)
        self.image = load_image('.' + parse_tile(code))

        self.rect = self.image.get_rect()
        if type == 'land':
            size = TILE_SIZE
            self.image = pygame.transform.scale(self.image, (size, size))
            self.rect.x = size * x
            self.rect.y = size * y
        elif type == 'decor':
            size = (self.rect.width * 100 / 128, self.rect.height * 100 / 128)
            self.image = pygame.transform.scale(self.image, (self.rect.width * 100 / 128, self.rect.height * 100 / 128))
            self.rect.x = size[0] * x
            self.rect.y = size[1] * y
