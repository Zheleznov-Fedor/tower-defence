import pygame
from Utils import load_image, TILE_SIZE, ENEMIES_INFO


class Enemy(pygame.sprite.Sprite):
    def __init__(self, group, lvl, map_w, map_h, path, game_lose_heart, add_money):
        super().__init__(group)
        self.game_lose_heart = game_lose_heart
        self.add_money = add_money

        self.orig_image = load_image('./enemy/' + ENEMIES_INFO[lvl]['image_filename'])
        self.image = load_image('./enemy/' + ENEMIES_INFO[lvl]['image_filename'])
        height = ENEMIES_INFO[lvl]['height']
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (height * self.rect.width / self.rect.height, height))
        self.orig_image = pygame.transform.scale(self.orig_image, (height * self.rect.width / self.rect.height, height))

        self.start = (path[0][0] * 100, (1 + path[0][1]) * 100 - 50 * 0.5)
        self.map_w = map_w
        self.map_h = map_h
        if path[0][0] == map_w - 1:
            self.rect.x = map_w * TILE_SIZE
        else:
            self.rect.x = -60
        self.rect.y = self.start[1]

        self.step = ENEMIES_INFO[lvl]['step']
        self.rot_speed = ENEMIES_INFO[lvl]['angle_step']

        self.path = path
        self.path_pos = 1
        self.grid_pos = self.path[0]
        self.is_came_out = False
        self.is_rotating = False
        self.rotating_direction = 0
        self.rotating_pos = 0

        self.hp = ENEMIES_INFO[lvl]['hp']
        self.max_hp = ENEMIES_INFO[lvl]['hp']

        if self.path[self.path_pos][0] < self.grid_pos[0]:
            self.image = pygame.transform.rotate(self.orig_image, -180)
        elif self.path[self.path_pos][1] > self.grid_pos[1]:
            self.image = pygame.transform.rotate(self.orig_image, 90)
        elif self.path[self.path_pos][1] != self.grid_pos[1]:
            self.image = pygame.transform.rotate(self.orig_image, -90)

    def bezier(self, p0, p1, p2, t):
        p0 = [p0[0] * 100, (1 + p0[1]) * 100 - 50 * 0.5]
        p1 = [p1[0] * 100, (1 + p1[1]) * 100 - 50 * 0.5]
        p2 = [p2[0] * 100, (1 + p2[1]) * 100 - 50 * 0.5]
        px = p0[0] * (1 - t) ** 2 + 2 * (1 - t) * t * p1[0] + p2[0] * t ** 2
        py = p0[1] * (1 - t) ** 2 + 2 * (1 - t) * t * p1[1] + p2[1] * t ** 2
        return px, py

    def rot_center(self, angle):
        self.image = pygame.transform.rotate(self.orig_image, angle)

    def rotation_direction(self, args):
        x1, y1, x2, y2, x3, y3 = args
        if y2 > y1:
            if x3 > x1:
                return -1
            return 1
        elif y1 > y2:
            if x3 > x1:
                return 1
            return -1
        elif y1 == y2:
            if y3 > y1:
                return 1
            return -1

    def update(self, *args):
        if not self.is_came_out:
            if self.path[self.path_pos][0] > self.grid_pos[0]:
                self.rect.x += self.step
                if self.rect.x == 0:
                    self.is_came_out = True
            elif self.path[self.path_pos][0] != self.grid_pos[0]:
                self.rect.x -= self.step

                if self.rect.x == self.map_w * TILE_SIZE:
                    self.is_came_out = True
            elif self.path[self.path_pos][1] > self.grid_pos[1]:
                self.rect.y += self.step

                if self.rect.y == 0:
                    self.is_came_out = True
            elif self.path[self.path_pos][1] != self.grid_pos[1]:
                self.rect.y -= self.step

                if self.rect.h == self.map_h * TILE_SIZE:
                    self.is_came_out = True
        elif self.path_pos < len(self.path):
            if self.is_rotating:
                self.rect.x, self.rect.y = self.bezier(*self.path[self.path_pos:self.path_pos + 3],
                                                       round(self.rotating_pos / 90, 3))
                self.rotating_pos = round(self.rotating_pos + self.rot_speed, 3)
                self.rot_center(-self.rotating_pos * self.rotating_direction)
                if self.rotating_pos == 90:
                    self.orig_image = pygame.transform.rotate(self.orig_image, -90 * self.rotating_direction)
                    self.rotating_pos = 0
                    self.is_rotating = False
                    self.path_pos += 2
            elif abs(self.rect.x - self.start[0]) != 100 and abs(self.rect.y - self.start[1]) != 100:
                if self.path[self.path_pos][0] > self.grid_pos[0]:
                    self.rect.x += self.step
                elif self.path[self.path_pos][0] != self.grid_pos[0]:
                    self.rect.x -= self.step
                if self.path[self.path_pos][1] > self.grid_pos[1]:
                    self.rect.y += self.step
                elif self.path[self.path_pos][1] != self.grid_pos[1]:
                    self.rect.y -= self.step
            else:
                self.grid_pos = self.path[self.path_pos]
                self.path_pos += 1
                self.start = (self.rect.x, self.rect.y)

                if self.path_pos < len(self.path):
                    self.is_rotating = self.path[self.path_pos][2]
                    if self.is_rotating:
                        res = []
                        for elem in [elem[0:2] for elem in self.path[self.path_pos: self.path_pos + 3]]:
                            res.extend(elem)
                        self.rotating_direction = self.rotation_direction(res)
        else:
            if self.path[-1][0] > self.path[-2][0]:
                self.rect.x += self.step

                if self.rect.x == self.map_w * TILE_SIZE + 15:
                    self.game_lose_heart()
                    self.kill()
            elif self.path[-1][0] != self.path[-2][0]:
                self.rect.x -= self.step

                if self.rect.x == -15:
                    self.game_lose_heart()
                    self.kill()
            if self.path[-1][1] > self.path[-2][1]:
                self.rect.y += self.step

                if self.rect.y == self.map_h * TILE_SIZE + 15:
                    self.game_lose_heart()
                    self.kill()
            elif self.path[-1][1] != self.path[-2][1]:
                self.rect.y -= self.step

                if self.rect.y == -15:
                    self.game_lose_heart()
                    self.kill()

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (self.rect.x - 5, self.rect.y - 20, 60, 10))
        pygame.draw.rect(screen, (0, 255, 0), (self.rect.x - 5, self.rect.y - 20, 60 / self.max_hp * self.hp, 10))
        pygame.draw.rect(screen, (0, 0, 0), (self.rect.x - 5, self.rect.y - 20, 60, 10), 2)

    def damage(self, value):
        self.hp -= value

        if self.hp <= 0:
            self.add_money(20)
            self.kill()
            return -1
