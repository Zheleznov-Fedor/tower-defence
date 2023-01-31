import pygame
from map import build_map, get_waves
from Utils import load_image, TILE_SIZE, getInventory, addCrediti
from Enemy import Enemy
from ShootingTower import ShootingTower, TOWERS_INFO
from FarmTower import FarmTower


class Game:
    """Класс игры"""

    def __init__(self, screen, level_filename, waves):
        self.screen = screen
        self.waves = get_waves(waves)
        self.land = pygame.sprite.Group()
        self.shooting_towers = pygame.sprite.Group()
        self.farm_towers = pygame.sprite.Group()
        self.missiles = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.map = build_map(level_filename, self.land)

        self.inventory = getInventory()  # Инвентарь игрока на матч
        self.hp = 3  # Количество жизней (сердечек)
        self.coins = 1000  # Количество денег
        self.wave = 1  # Номер волны, начиная с нуля
        self.is_sending_wave = False  # Отправляется ли сейчас волна
        self.sending_enemy_index = 0  # Отправляемый пришелец
        self.game_start_state = 'waiting'  # Состояние игры
        self.wave_state = 0  # Статус отправляемый волны
        self.is_tower_selected = False  # Выбрана ли башню
        self.selected_tower = -1  # Выбранная башня

        self.btn_end = 0
        self.get_money = False
        self.is_end = False

    def draw_hp(self):
        '''Функция рисующая сердечки'''
        for i in range(self.hp):
            image = load_image('./decor/other/heart.png')
            image = pygame.transform.scale(image, (32, 32))
            self.screen.blit(image, (1480 + i * 40, 5))

        for i in range(self.hp, 3):
            image = load_image('./decor/other/heart_empty.png')
            image = pygame.transform.scale(image, (32, 32))
            self.screen.blit(image, (1480 + i * 40, 5))

    def draw_coins(self):
        '''Функция рисующая деньги'''
        image = load_image('./decor/other/money.png')
        image = pygame.transform.scale(image, (32, 32))
        self.screen.blit(image, (1480, 50))

        text = pygame.font.Font(None, 45).render(str(self.coins), 1, (0, 0, 0))
        self.screen.blit(text, (1518, 53))

    def draw_header(self):
        '''Функция рисующая заголовок'''
        pygame.draw.rect(self.screen, (0, 0, 0), (1470, -5, 135, 100), 5)
        self.draw_hp()
        self.draw_coins()

    def draw_waves(self):
        '''Функция рисующая состояние игры и волны'''
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
        '''Функция рисующая полупрозрачный прямоугольник'''
        shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
        pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
        surface.blit(shape_surf, rect)

    def draw_inventory(self):
        '''Функция рисующая инвентарь'''
        pygame.draw.rect(self.screen, (0, 0, 0), (-5, 740, 10 + len(self.inventory) * 100 + 15, 165), 5)

        if self.is_tower_selected:
            self.draw_rect_alpha(self.screen, (0, 0, 0, 90), (10 + (self.selected_tower - 1) * 100, 750, 100, 140))

        for i in range(len(self.inventory)):
            image = load_image('./defense/' + TOWERS_INFO[self.inventory[i]]['levels'][0]['image_filename'])
            rect = image.get_rect()
            image = pygame.transform.scale(image, (rect.width / rect.height * 64, 64))
            text = pygame.font.Font(None, 30).render(self.inventory[i], 1, (0, 0, 0))

            self.screen.blit(image, (10 + i * 100 + 50 - rect.width / rect.height * 64 // 2, 760))
            self.screen.blit(text, (10 + i * 100 + 50 - text.get_width() // 2, 840))

            image = load_image('./decor/other/money.png')
            image = pygame.transform.scale(image, (16, 16))

            text = pygame.font.Font(None, 30).render(str(TOWERS_INFO[self.inventory[i]]['price']), 1, (0, 0, 0))
            self.screen.blit(image, (10 + i * 100 + 50 - (16 + 5 + text.get_width()) // 2, 865))
            self.screen.blit(text, (10 + i * 100 + 50 - text.get_width() // 2 + 10, 865))

    def add_money(self, value):
        '''Добавляет деньги'''
        self.coins += value

    def lose_heart(self):
        '''Убрает одно сердечко'''
        self.hp -= 1

    def put_tower(self, tower_name, x, y):
        '''Ставит башню и снимает деньги'''
        if tower_name == 'Farm':
            FarmTower(self.farm_towers, x, y, self.add_money)
        else:
            ShootingTower(self.shooting_towers, tower_name, x, y, self.enemies, self.missiles)

        self.coins -= TOWERS_INFO[tower_name]['price']

    def inventory_detect_mouse(self, pos):
        '''Проверяет не наведена ли мышка на башню в инвентаре'''
        buttons = [[20, 95], [120, 195], [220, 295], [320, 395]]

        for i in range(len(self.inventory)):
            if buttons[i][0] <= pos[0] <= buttons[i][1] and 780 <= pos[1] <= 894:
                return i + 1

        return 0

    def detect_mouse(self, pos, tower):
        '''Проверяет не наведена ли мышка на башню'''
        return tower.rect.x <= pos[0] <= tower.rect.x + tower.rect.width + 26 and \
            tower.rect.y - 32 <= pos[1] <= tower.rect.y + tower.rect.height + 26

    def tower_detect_mouse(self, pos):
        '''Проверяет не наведена ли мышка на башню на карте'''
        for shooting_tower in self.shooting_towers.sprites():
            if self.detect_mouse(pos, shooting_tower):
                return shooting_tower

        for farm_tower in self.farm_towers.sprites():
            if self.detect_mouse(pos, farm_tower):
                return farm_tower

        return 0

    def tower_place_detect_mouse(self, pos):
        '''Проверяет не наведена ли мышка на место для установки башни'''
        places = self.map['tower_places']

        for place in places:
            if place[0] * TILE_SIZE <= pos[0] <= (place[0] + 1) * TILE_SIZE and \
                    place[1] * TILE_SIZE <= pos[1] <= (place[1] + 1) * TILE_SIZE:
                if TOWERS_INFO[self.inventory[self.selected_tower - 1]]['place_type'] == place[2]:
                    return place

        return 0

    def buttons_detect_mouse(self, towers, pos):
        '''Проверяет не нажата ли кнопка удаления или обновления переданный башни'''
        for tower in towers:
            coords = tower.coords()

            if tower.coords()[1] >= TILE_SIZE:
                if coords[0] <= pos[0] <= coords[0] + 0.77 * 26 and \
                        coords[1] - 26 <= pos[1] <= coords[1]:
                    tower.delete()
                    self.coins += tower.price()
                elif coords[0] + 30 <= pos[0] <= coords[0] + 0.77 * 26 + 30 and \
                        coords[1] - 26 <= pos[1] <= coords[1]:
                    if tower.is_updateable() and self.coins >= tower.update_price():
                        tower.update_level()
                        print(tower.update_price())
                        self.coins -= tower.update_price()
            else:
                if coords[0] <= pos[0] <= coords[0] + 0.77 * 26 and \
                        coords[1] + tower.size()[1] <= pos[1] <= coords[1] + tower.size()[1] + 26:
                    tower.delete()
                    self.coins += tower.price()
                elif coords[0] + 30 <= pos[0] <= coords[0] + 0.77 * 26 + 30 and \
                        coords[1] + tower.size()[1] <= pos[1] <= coords[1] + tower.size()[1] + 26:
                    if tower.is_updateable() and self.coins >= tower.update_price():
                        tower.update_level()
                        print(tower.update_price())
                        self.coins -= tower.update_price()

    def tower_buttons_detect_mouse(self, pos):
        '''Проверяет не нажата ли кнопка удаления или обновления всех башни'''
        self.buttons_detect_mouse(self.shooting_towers.sprites(), pos)
        self.buttons_detect_mouse(self.farm_towers.sprites(), pos)

    def draw_tower_buttons(self, tower):
        '''Рисует кнопки удаления и обновления башни'''
        if tower.coords()[1] >= TILE_SIZE:
            image = load_image('./decor/buttons/Delete.png')
            image = pygame.transform.scale(image, (0.77 * 26, 26))

            self.screen.blit(image, (tower.coords()[0], tower.coords()[1] - 30))

            image = load_image('./decor/other/money.png')
            image = pygame.transform.scale(image, (16, 16))
            text = pygame.font.Font(None, 30).render(str(tower.price()), 1, (0, 0, 0))

            self.screen.blit(image, (tower.coords()[0] - 15 - text.get_width() - 5, tower.coords()[1] - 25))
            self.screen.blit(text, (tower.coords()[0] - text.get_width() - 5, tower.coords()[1] - 25))

            image = load_image('./decor/buttons/Update.png')
            image = pygame.transform.scale(image, (26, 26))

            self.screen.blit(image, (tower.coords()[0] + 30, tower.coords()[1] - 30))

            if tower.is_updateable():
                image = load_image('./decor/other/money.png')
                image = pygame.transform.scale(image, (16, 16))
                self.screen.blit(image, (tower.coords()[0] + 60, tower.coords()[1] - 25))

                text = pygame.font.Font(None, 30).render(str(tower.update_price()), 1, (0, 0, 0))
                self.screen.blit(text, (tower.coords()[0] + 75, tower.coords()[1] - 25))
            else:
                text = pygame.font.Font(None, 30).render('No update', 1, (0, 0, 0))
                self.screen.blit(text, (tower.coords()[0] + 60, tower.coords()[1] - 25))
        else:
            image = load_image('./decor/buttons/Delete.png')
            image = pygame.transform.scale(image, (0.77 * 26, 26))

            self.screen.blit(image, (tower.coords()[0], tower.coords()[1] + tower.size()[1]))

            image = load_image('./decor/other/money.png')
            image = pygame.transform.scale(image, (16, 16))
            text = pygame.font.Font(None, 30).render(str(tower.price()), 1, (0, 0, 0))

            self.screen.blit(image, (tower.coords()[0] - 15 - text.get_width() - 5,
                                     tower.coords()[1] + tower.size()[1] + 5))
            self.screen.blit(text, (tower.coords()[0] - text.get_width() - 5, tower.coords()[1] + tower.size()[1] + 5))

            image = load_image('./decor/buttons/Update.png')
            image = pygame.transform.scale(image, (26, 26))

            self.screen.blit(image, (tower.coords()[0] + 30, tower.coords()[1] + tower.size()[1]))

            if tower.is_updateable():
                image = load_image('./decor/other/money.png')
                image = pygame.transform.scale(image, (16, 16))
                self.screen.blit(image, (tower.coords()[0] + 60, tower.coords()[1] + tower.size()[1] + 5))

                text = pygame.font.Font(None, 30).render(str(tower.update_price()), 1, (0, 0, 0))
                self.screen.blit(text, (tower.coords()[0] + 75, tower.coords()[1] + tower.size()[1] + 5))
            else:
                text = pygame.font.Font(None, 30).render('No update', 1, (0, 0, 0))
                self.screen.blit(text, (tower.coords()[0] + 60, tower.coords()[1] + tower.size()[1] + 5))

    def end(self, result, screenSize):
        width, height = screenSize
        if self.wave <= 15:
            income = self.wave * 5
        elif 15 < self.wave <= 20:
            income = 75 + (self.wave - 15) * 10
        elif self.wave > 20:
            income = 125 + (self.wave - 20) * 15
        if result == 'win':
            text = 'Вы выиграли!'
            income += 100
            color = (40, 114, 51)
        elif result == 'lose':
            text = 'Вы проиграли!'
            color = (255, 36, 0)
        font150 = pygame.font.Font(None, 150)
        font100 = pygame.font.Font(None, 100)
        inscription = font150.render(text, True, color)
        total = font100.render(f"Итого волн: {str(self.wave)}", True, color)
        incomeText = font100.render(f"Получено: +{str(income)}", True, color)
        endText = font100.render('Ок', True, color)
        x, y = (width // 2 - inscription.get_width() // 2, height // 2 - inscription.get_height() // 2)
        pygame.draw.rect(self.screen, (255, 245, 238), (x - 20, y - 20, inscription.get_width() + 40,
                                                        inscription.get_height() + incomeText.get_height() + total.get_height()
                                                        + 40), 0)
        pygame.draw.rect(self.screen, color, (x - 20, y - 20, inscription.get_width() + 40,
                                              inscription.get_height() + incomeText.get_height() + total.get_height() + 40),
                         2)
        pygame.draw.rect(self.screen, color,
                         (x - 20, y - 20, inscription.get_width() + 40, inscription.get_height() + 30),
                         2)
        self.screen.blit(inscription, (x, y))
        self.screen.blit(total, (x, height // 2 - incomeText.get_height() // 2 + inscription.get_height()))
        self.screen.blit(incomeText,
                         (
                             x,
                             height // 2 - incomeText.get_height() // 2 + inscription.get_height() + total.get_height()))
        self.screen.blit(endText, (x + inscription.get_width() - endText.get_width(),
                                   y + inscription.get_height() + incomeText.get_height() + total.get_height() - endText.get_height() + 10))
        self.btn_end = (x + inscription.get_width() - endText.get_width(),
                        y + inscription.get_height() + incomeText.get_height() + total.get_height() - endText.get_height() + 10,
                        endText.get_width(), endText.get_width())
        if not self.get_money:
            addCrediti(income)
            self.get_money = True
        self.is_end = True

    def end_click(self, coords):
        x, y = coords
        x1, y1, x2, y2 = self.btn_end
        if x1 <= x <= x1 + x2 and y1 <= y <= y1 + y2:
            return 'ok'

    def draw(self):
        running = True
        GAMESTART = pygame.USEREVENT + 130
        NEWWAVE = pygame.USEREVENT + 2
        ADDENEMY = pygame.USEREVENT + 3
        pygame.time.set_timer(GAMESTART, 1000)
        pygame.time.set_timer(ADDENEMY, 750)
        self.game_start_state = 'starting'

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

                elif event.type == NEWWAVE and self.hp > 0:
                    pygame.time.set_timer(NEWWAVE, 0)
                    self.wave_state = 0
                    self.is_sending_wave = True
                    self.sending_enemy_index = 0

                    if self.wave != len(self.waves):
                        self.wave += 1
                        self.add_money(500)
                        for farm in self.farm_towers:
                            farm.give_money()
                    else:
                        self.game_start_state = 'win'
                elif event.type == ADDENEMY and self.hp > 0:
                    self.enemies.update()
                    self.shooting_towers.update()

                    if self.game_start_state == 'started' and self.is_sending_wave:
                        if self.sending_enemy_index < len(self.waves[self.wave - 1]):
                            Enemy(self.enemies, self.waves[self.wave - 1][self.sending_enemy_index],
                                  self.map['w'], self.map['h'],
                                  self.map['enemy_path'], self.lose_heart, self.add_money)
                            self.sending_enemy_index += 1
                        else:
                            self.is_sending_wave = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.is_end:
                            if self.end_click(event.pos) == 'ok':
                                return
                        if self.is_tower_selected:
                            place = self.tower_place_detect_mouse(pygame.mouse.get_pos())
                            self.is_tower_selected = False
                            if place:
                                self.put_tower(self.inventory[self.selected_tower - 1],
                                               place[0], place[1])
                                self.selected_tower = None

                        tower = self.inventory_detect_mouse(event.pos)
                        if self.inventory_detect_mouse(event.pos) and self.selected_tower != tower:
                            if TOWERS_INFO[self.inventory[tower - 1]]['price'] <= self.coins:
                                self.is_tower_selected = True
                                self.selected_tower = tower
                        else:
                            self.selected_tower = None
                            self.is_tower_selected = False
                            self.tower_buttons_detect_mouse(pos)

            self.screen.fill((255, 255, 255))

            self.land.draw(self.screen)
            self.enemies.draw(self.screen)
            for enemy in self.enemies:
                enemy.draw(self.screen)
            self.missiles.draw(self.screen)
            self.shooting_towers.draw(self.screen)
            self.farm_towers.draw(self.screen)
            self.draw_header()
            self.draw_waves()

            pos = pygame.mouse.get_pos()
            hover_inventory_tower = self.inventory_detect_mouse(pos)
            if hover_inventory_tower:
                self.draw_rect_alpha(self.screen, (0, 0, 0, 50),
                                     (10 + (hover_inventory_tower - 1) * 100, 750, 100, 140))

            if self.is_tower_selected:
                place = self.tower_place_detect_mouse(pos)
                if place:
                    self.draw_rect_alpha(self.screen, (0, 0, 0, 50),
                                         (place[0] * TILE_SIZE, place[1] * TILE_SIZE,
                                          TILE_SIZE, TILE_SIZE))

            hover_tower = self.tower_detect_mouse(pos)
            if hover_tower:
                self.draw_tower_buttons(hover_tower)

            self.draw_inventory()
            if self.wave == len(self.waves) and len(self.enemies) == 0 and not self.is_sending_wave and \
                    self.game_start_state == 'started' and self.wave_state != 'waiting':
                self.game_start_state = 'win'
            elif not self.is_sending_wave and len(self.enemies) == 0 and \
                    self.game_start_state == 'started' and self.wave_state != 'waiting':
                pygame.time.set_timer(NEWWAVE, 5000)
                self.wave_state = 'waiting'

            if self.game_start_state == 'win':
                self.end('win', (1600, 900))

            if self.hp > 0:
                self.enemies.update()
                self.shooting_towers.update()
                self.missiles.update()
            else:
                self.end('lose', (1600, 900))
            pygame.display.flip()
        return


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1600, 900))
    pygame.display.set_caption('Map test')
    fps = 90
    clock = pygame.time.Clock()

    game = Game(screen, 'txt/test1.csv', 15)
    game.draw()

    pygame.quit()
