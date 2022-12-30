import os
import sys
import pygame


def parse_tile(code):
    types = {
        'r': '/road',
        't': '/tower'
    }
    biomes = {
        'd': '/desert',
        's': '/spring',
        'w': '/winter'
    }
    return types[code[0]] + biomes[code[1]] + '/' + code[2:4] + '.png'


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


class Tile(pygame.sprite.Sprite):
    def init(self, group, code, x, y):
        super().init(group)
        self.image = load_image('.' + parse_tile(code))
        w = 100
        h = int(0.94 * w)
        self.image = pygame.transform.scale(self.image, (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = w * x
        self.rect.y = h * y

    def update(self, *args):
        pass


if name == 'main':
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    pygame.display.set_caption('Map test')

    running = True
    fps = 60
    clock = pygame.time.Clock()

    all_sprites = pygame.sprite.Group()

    Tile(all_sprites, 'rw07', 0, 0)
    Tile(all_sprites, 'rw07', 1, 0)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                all_sprites.update(event)

        screen.fill((255, 255, 255))

        all_sprites.update()
        all_sprites.draw(screen)

        clock.tick(fps)
        pygame.display.flip()

    pygame.quit()

