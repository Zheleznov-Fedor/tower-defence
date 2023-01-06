import pygame
import csv
from Functions import load_image, TILE_SIZE
from Enemy import Enemy


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
            'w': 0,
            'h': 0,
            'land': [],
            'decor': [],
            'enemy_path': [],
            'waves': []
        }
        r = list(reader)
        w, h = map(int, r[0])
        res['w'] = w
        res['h'] = h

        for i in range(1, h + 1):
            res['land'].append(r[i])

        decor_count = int(r[h + 1][0])

        for elem in r[h + 2:h + decor_count + 2]:
            res['decor'].append({
                'code': elem[0],
                'x': float(elem[1]),
                'y': float(elem[2]),
            })

        res['enemy_path'] = [list(map(int, point.split(','))) for point in r[h + decor_count + 2]]

        waves_count = r[h + decor_count + 3]
        for wave in r[h + decor_count + 4:]:
            res['waves'].append([tuple(map(int, elem.split(','))) for elem in wave])

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

    return map


class Tile(pygame.sprite.Sprite):
    def __init__(self, group, code, x, y):
        super().__init__(group)
        self.image = load_image('.' + parse_tile(code))
        size = TILE_SIZE
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect()
        self.rect.x = size * x
        self.rect.y = size * y


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1600, 900))
    pygame.display.set_caption('Map test')

    running = True
    fps = 90
    state = 'waiting'
    enemies = []
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    map = build_map('test.csv', all_sprites)
    last = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                all_sprites.update(event)

        screen.fill((255, 255, 255))

        if last + 1500 <= pygame.time.get_ticks():
            last = pygame.time.get_ticks()
            enemies.append(Enemy(all_sprites, '0.png', map['w'], map['h'], map['enemy_path']))

        all_sprites.update()
        all_sprites.draw(screen)

        for enemy in enemies:
            enemy.draw(screen)

        clock.tick(fps)
        pygame.display.flip()

    pygame.quit()
