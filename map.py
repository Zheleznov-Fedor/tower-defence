import pygame
import csv
from Functions import load_image, TILE_SIZE
from Enemy import Enemy
from ShootingTower import ShootingTower


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
            'waves': [],
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

        for wave in r[h + decor_count + 4:]:
            res['waves'].append({
                'enemies': wave[0].split(','),
                'timeout': int(wave[1]),
                'bonus_coins': int(wave[2])
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
    clock = pygame.time.Clock()
    land = pygame.sprite.Group()
    towers = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    map = build_map('test.csv', land)
    last = 0
    # Board(all_sprites, 1, 2)
    x = ShootingTower(towers, 'Gun.png', 1, 2, enemies)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))

        if last + 1500 <= pygame.time.get_ticks():
            last = pygame.time.get_ticks()
            Enemy(enemies, '0.png', map['w'], map['h'], map['enemy_path'])

        enemies.update()
        towers.update()
        land.draw(screen)
        enemies.draw(screen)
        towers.draw(screen)

        x.update()

        last += 1
        for enemy in enemies:
            enemy.draw(screen)

        clock.tick(fps)
        pygame.display.flip()

    pygame.quit()
