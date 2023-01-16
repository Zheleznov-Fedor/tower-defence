import pygame
from map import build_map
from Functions import load_image, getEquipment
from Enemy import Enemy, TILE_SIZE
from ShootingTower import ShootingTower, TOWERS_INFO
from FarmTower import FarmTower


class Game:
    def __init__(self, screen, level_filename):
        self.screen = screen
        self.land = pygame.sprite.Group()
        self.shooting_towers = pygame.sprite.Group()
        self.farm_towers = pygame.sprite.Group()
        self.missiles = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.map = build_map(level_filename, self.land)

        self.equipment = getEquipment()
        self.hp = 3
        self.coins = 500
        self.wave = 1
        self.is_sending_wave = False
        self.sending_enemy_index = 0
        self.game_start_state = 'waiting'

        self.is_tower_selected = False
        self.selected_tower = -1

    def draw_hp(self):
        for i in range(self.hp):
            image = load_image('./decor/other/heart.png')
            image = pygame.transform.scale(image, (32, 32))
            self.screen.blit(image, (1480 + i * 40, 5))

        for i in range(self.hp, 3):
            image = load_image('./decor/other/heart_empty.png')
            image = pygame.transform.scale(image, (32, 32))
            self.screen.blit(image, (1480 + i * 40, 5))

    def draw_coins(self):
        image = load_image('./decor/other/money.png')
        image = pygame.transform.scale(image, (32, 32))
        self.screen.blit(image, (1480, 50))

        text = pygame.font.Font(None, 45).render(str(self.coins), 1, (0, 0, 0))
        self.screen.blit(text, (1518, 53))

    def draw_header(self):
        pygame.draw.rect(self.screen, (0, 0, 0), (1470, -5, 135, 100), 5)
        self.draw_hp()
        self.draw_coins()

    def draw_waves(self):
        draw_text = f"Волна {self.wave}"

        if self.game_start_state == 'waiting':
            draw_text = 'Ждём'
        elif self.game_start_state == '3sec':
            draw_text = '3'
        elif self.game_start_state == '2sec':
            draw_text = '2'
        elif self.game_start_state == '1sec':
            draw_text = '1'
        elif self.game_start_state == 'starting':
            draw_text = 'Начали!'
        elif self.game_start_state == 'win':
            draw_text = 'Победа!'

        pygame.draw.rect(self.screen, (0, 0, 0), (725, -5, 150, 80), 5)
        text = pygame.font.Font(None, 45).render(draw_text, 1, (0, 0, 0))
        self.screen.blit(text, (1600 // 2 - text.get_width() // 2, 23))

    def draw_rect_alpha(self, surface, color, rect):
        shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
        pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
        surface.blit(shape_surf, rect)

    def draw_inventory(self):
        pygame.draw.rect(self.screen, (0, 0, 0), (-5, 740, 10 + len(self.equipment) * 100 + 15, 165), 5)

        if self.is_tower_selected:
            self.draw_rect_alpha(self.screen, (0, 0, 0, 90), (10 + (self.selected_tower - 1) * 100, 750, 100, 140))

        for i in range(len(self.equipment)):
            image = load_image('./defense/' + TOWERS_INFO[self.equipment[i]]['image_filename'])
            rect = image.get_rect()
            image = pygame.transform.scale(image, (rect.width / rect.height * 64, 64))
            text = pygame.font.Font(None, 30).render(self.equipment[i], 1, (0, 0, 0))

            self.screen.blit(image, (10 + i * 100 + 50 - rect.width / rect.height * 64 // 2, 760))
            self.screen.blit(text, (10 + i * 100 + 50 - text.get_width() // 2, 840))

            image = load_image('./decor/other/money.png')
            image = pygame.transform.scale(image, (16, 16))

            text = pygame.font.Font(None, 30).render(str(TOWERS_INFO[self.equipment[i]]['price']), 1, (0, 0, 0))
            self.screen.blit(image, (10 + i * 100 + 50 - (16 + 5 + text.get_width()) // 2, 865))
            self.screen.blit(text, (10 + i * 100 + 50 - text.get_width() // 2 + 10, 865))

    def add_money(self, value):
        self.coins += value

        # if step == 0:
        #     self.coins += value
        #
        # image = load_image('./decor/other/green_money.png')
        # print((step / 300) * 256)
        # image.set_alpha((step / 300) * 256)
        # self.screen.blit(image, (1500, 200))

    def lose_heart(self):
        self.hp -= 1

    def put_tower(self, tower_name, x, y):
        if tower_name == 'Farm':
            FarmTower(self.farm_towers, x, y, self.add_money)
        else:
            ShootingTower(self.shooting_towers, tower_name, x, y, self.enemies, self.missiles)

        self.coins -= TOWERS_INFO[tower_name]['price']

    def inventory_detect_mouse(self, pos):
        buttons = [[20, 95], [120, 195], [220, 295], [320, 395]]

        for i in range(len(self.equipment)):
            if buttons[i][0] <= pos[0] <= buttons[i][1] and 780 <= pos[1] <= 894:
                return i + 1

        return 0

    def tower_detect_mouse(self, pos):
        for shooting_tower in self.shooting_towers.sprites():
            if shooting_tower.rect.x <= pos[0] <= shooting_tower.rect.x + shooting_tower.rect.width and \
                    shooting_tower.rect.y <= pos[1] <= shooting_tower.rect.y + shooting_tower.rect.height:
                return shooting_tower

        return 0

    def tower_place_detect_mouse(self, pos):
        places = self.map['tower_places']

        for place in places:
            if place[0] * TILE_SIZE <= pos[0] <= (place[0] + 1) * TILE_SIZE and \
                    place[1] * TILE_SIZE <= pos[1] <= (place[1] + 1) * TILE_SIZE:
                if TOWERS_INFO[self.equipment[self.selected_tower - 1]]['place_type'] == place[2]:
                    return place

        return 0

    def draw(self):
        # ДЛЯ ТЕСТИРОВНИЯ
        ShootingTower(self.shooting_towers, 'Gun', 2, 4, self.enemies, self.missiles)
        ShootingTower(self.shooting_towers, 'Solider', 5, 3, self.enemies, self.missiles)
        ShootingTower(self.shooting_towers, 'Laser', 6, 5, self.enemies, self.missiles)
        ShootingTower(self.shooting_towers, 'Solider', 5, 6, self.enemies, self.missiles)
        ShootingTower(self.shooting_towers, 'Laser', 9, 3, self.enemies, self.missiles)

        FarmTower(self.farm_towers, 0, 0, self.add_money)

        running = True
        GAMESTART = pygame.USEREVENT + 1
        NEWWAVE = pygame.USEREVENT + 2
        ADDENEMY = pygame.USEREVENT + 3
        pygame.time.set_timer(GAMESTART, 1000)
        pygame.time.set_timer(ADDENEMY, 750)

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == GAMESTART:
                    if self.game_start_state == 'waiting':
                        pygame.time.set_timer(GAMESTART, 1000)
                        self.game_start_state = '3sec'
                    elif self.game_start_state == '3sec':
                        self.game_start_state = '2sec'
                    elif self.game_start_state == '2sec':
                        self.game_start_state = '1sec'
                    elif self.game_start_state == '1sec':
                        self.game_start_state = 'starting'
                        pygame.time.set_timer(GAMESTART, 500)
                    elif self.game_start_state == 'starting':
                        self.game_start_state = 'started'
                        pygame.time.set_timer(GAMESTART, 0)

                        self.is_sending_wave = True
                        pygame.time.set_timer(NEWWAVE, self.map['waves'][self.wave - 1]['timeout'])
                elif event.type == NEWWAVE and self.hp > 0:
                    self.is_sending_wave = True
                    self.sending_enemy_index = 0

                    if self.wave != len(self.map['waves']):
                        self.wave += 1
                        self.add_money(self.map['waves'][self.wave - 1]['bonus_coins'])
                        for farm in self.farm_towers:
                            farm.give_money()

                        pygame.time.set_timer(NEWWAVE, self.map['waves'][self.wave - 1]['timeout'])
                    else:
                        self.game_start_state = 'win'
                        print('WIN!!!')
                elif event.type == ADDENEMY and self.hp > 0:
                    self.enemies.update()
                    self.shooting_towers.update()

                    if self.game_start_state == 'started' and self.is_sending_wave:
                        if self.sending_enemy_index < len(self.map['waves'][self.wave - 1]['enemies']):
                            Enemy(self.enemies, self.map['waves'][self.wave - 1]['enemies'][self.sending_enemy_index],
                                  self.map['w'], self.map['h'],
                                  self.map['enemy_path'], self.lose_heart)
                            self.sending_enemy_index += 1
                        else:
                            self.is_sending_wave = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.is_tower_selected:
                            place = self.tower_place_detect_mouse(pygame.mouse.get_pos())
                            self.is_tower_selected = False
                            if place:
                                self.put_tower(self.equipment[self.selected_tower - 1],
                                               place[0], place[1])

                        tower = self.inventory_detect_mouse(event.pos)
                        if self.inventory_detect_mouse(event.pos) and self.selected_tower != tower:
                            if TOWERS_INFO[self.equipment[tower - 1]]['price'] <= self.coins:
                                self.is_tower_selected = True
                                self.selected_tower = tower
                        else:
                            self.is_tower_selected = False

                            hover_tower = self.tower_detect_mouse(pos)
                            if hover_tower:
                                self.draw_rect_alpha(self.screen, (0, 0, 0, 50), (hover_tower.rect.x,
                                                                                  hover_tower.rect.y,
                                                                                  hover_tower.rect.width,
                                                                                  hover_tower.rect.height))
                                hover_tower.kill()

            self.screen.fill((255, 255, 255))

            self.land.draw(self.screen)
            self.enemies.draw(self.screen)
            for enemy in self.enemies:
                enemy.draw(self.screen)
            self.missiles.draw(self.screen)
            self.shooting_towers.draw(self.screen)
            self.farm_towers.draw(self.screen)
            self.tanks.draw(self.screen)
            self.draw_header()
            self.draw_waves()

            pos = pygame.mouse.get_pos()
            hover_inventory_tower = self.inventory_detect_mouse(pos)
            if hover_inventory_tower:
                self.draw_rect_alpha(self.screen, (0, 0, 0, 50), (10 + (hover_inventory_tower - 1) * 100, 750, 100, 140))

            if self.is_tower_selected:
                place = self.tower_place_detect_mouse(pos)
                if place:
                    self.draw_rect_alpha(self.screen, (0, 0, 0, 50),
                                         (place[0] * TILE_SIZE, place[1] * TILE_SIZE,
                                          TILE_SIZE, TILE_SIZE))

            hover_tower = self.tower_detect_mouse(pos)
            if hover_tower:
                self.draw_rect_alpha(self.screen, (0, 0, 0, 50), (hover_tower.rect.x, hover_tower.rect.y,
                                                                  hover_tower.rect.width, hover_tower.rect.height))

            self.draw_inventory()

            if self.hp > 0:
                self.enemies.update()
                self.shooting_towers.update()
                self.missiles.update()
                self.tanks.update()
            else:
                print('GAME OVER!!!')

            pygame.display.flip()
        return


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1600, 900))
    pygame.display.set_caption('Map test')
    fps = 90
    clock = pygame.time.Clock()

    game = Game(screen, 'test.csv')
    game.draw()

    pygame.quit()
