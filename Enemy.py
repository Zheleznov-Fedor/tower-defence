import pygame
from Functions import load_image, TILE_SIZE


class Enemy(pygame.sprite.Sprite):
    def __init__(self, group, type,  map_w, map_h, path):
        super().__init__(group)
        self.orig_image = load_image('./enemy/' + type)
        self.image = load_image('./enemy/' + type)
        height = 50
        self.image = pygame.transform.scale(self.image, (48 * height / 56, height))
        self.orig_image = pygame.transform.scale(self.orig_image, (48 * height / 56, height))
        self.rect = self.image.get_rect()

        if path[0][0] == map_w - 1:
            self.start = (map_w * TILE_SIZE, (0 + path[0][1]) * 100 - 50 * 0.5)
        else:
            self.start = (-36, (1 + path[0][1]) * 100 - 50 * 0.5)
        self.map_w = map_w
        self.map_h = map_h
        self.rect.x = self.start[0]
        self.rect.y = self.start[1]
        self.rect.w = 30
        self.rect.width = 30

        self.path = path
        self.path_pos = 1
        self.grid_pos = self.path[0]
        self.is_came_out = False
        self.is_rotating = False
        self.rotating_direction = 0
        self.rotating_pos = 0

        if self.path[self.path_pos][0] < self.grid_pos[0]:
            self.image = pygame.transform.rotate(self.orig_image, -180)
        elif self.path[self.path_pos][1] > self.grid_pos[1]:
            self.image = pygame.transform.rotate(self.orig_image, 90)
        elif self.path[self.path_pos][1] != self.grid_pos[1]:
            self.image = pygame.transform.rotate(self.orig_image, -90)

    def bezier(self, p0, p1, p2, t):
        p0 = [64 + (p0[0] - 1) * 100, 75 + (p0[1]) * 100]
        p1 = [64 + (p1[0] - 1) * 100, 75 + (p1[1]) * 100]
        p2 = [64 + (p2[0] - 1) * 100, 75 + (p2[1]) * 100]
        px = p0[0] * (1 - t) ** 2 + 2 * (1 - t) * t * p1[0] + p2[0] * t ** 2
        py = p0[1] * (1 - t) ** 2 + 2 * (1 - t) * t * p1[1] + p2[1] * t ** 2
        return px, py

    def rot_center(self, angle):
        self.image = pygame.transform.rotate(self.orig_image, angle)

    def update(self, *args):
        if not self.is_came_out:
            if self.path[self.path_pos][0] > self.grid_pos[0]:
                self.rect.x += 1

                if self.rect.x == 0:
                    self.is_came_out = True
            elif self.path[self.path_pos][0] != self.grid_pos[0]:
                self.rect.x -= 1
            elif self.path[self.path_pos][1] > self.grid_pos[1]:
                self.rect.y += 1

                if self.rect.y == 0:
                    self.is_came_out = True
            elif self.path[self.path_pos][1] != self.grid_pos[1]:
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

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), (self.rect.x - 5, self.rect.y - 20, 60, 10))
        pygame.draw.rect(screen, (0, 0, 0), (self.rect.x - 5, self.rect.y - 20, 60, 10), 2)