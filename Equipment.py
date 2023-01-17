# Всё, что нам нужно:
import pygame
from Functions import load_image, getEquipment, black, allEquipment, getInventory


class Equipment:
    def __init__(self, screen, screenSize, name):
        self.screen = screen  # Экран
        self.screenSize = screenSize  # Размер экрана
        self.width, self.height = screenSize  # Ширина и высота экрана
        self.xRect = self.width  # Граница начала кнопки
        self.widthRect = 0  # Граница конца кнопки
        self.btns = []  # Список всех кнопок
        self.name = name  # Название картинки стрелочки
        self.side = (self.width // 2 - 50) // 4  # Размер клетки снаряжения
        self.equipment = allEquipment  # Записываем весь существующий инвентарь
        # Далее создаём 2 использующихся шрифта
        self.font75 = pygame.font.Font(None, 75)
        self.font30 = pygame.font.Font(None, 30)
        self.cellColor = (192, 198, 200)  # Начальный цвет клетки
        self.lighting = None  # Включить ли подсветку

    # Риcуем разделитель
    def drawSeparator(self):
        pygame.draw.line(self.screen, black, (self.width // 2, 65), (self.width // 2, self.height), width=2)

    # Рисуем кнопку назад
    def drawBack(self):
        image = load_image(self.name)
        image = pygame.transform.scale(image, (32, 32))
        self.screen.blit(image, (10, 15))

    # Рисуем текст
    def drawText(self):
        text1 = self.font75.render('Снаряжение:', True, black)
        text2 = self.font75.render('Ваш инвентарь:', True, black)
        self.screen.blit(text1, (self.width // 4 - text1.get_width() // 2, 75))
        self.screen.blit(text2, (self.width // 4 - text2.get_width() // 2 + self.width // 2, 75))
        pygame.draw.line(self.screen, black, (0, 130), (self.width, 130), width=2)

    # Рисуем клетки снаряжения
    def drawCells(self):
        n = 0
        myInventory = getInventory()
        for defender in self.equipment:
            if defender not in myInventory:
                n += 1  # Для этого считаем количество закрытых/неиспользуемых единиц
        for i in range(n):  # Рисуем их
            pygame.draw.rect(self.screen, self.cellColor,
                             ((self.side + 10) * (i % 4) + 10, 150 + (self.side + 10) * (i // 4), self.side, self.side),
                             0)
        for i in range(4):  # Рисуем 4 клетки инвентаря
            pygame.draw.rect(self.screen, self.cellColor,
                             ((self.side + 10) * i + 10 + self.width // 2, 150, self.side, self.side), 0)

    # Рисуем моой инвентарь
    def drawMyEquipment(self):
        imageRemove = load_image('./decor/other/remove.png')
        imageRemove = pygame.transform.scale(imageRemove, (16, 16))
        myInventory = getInventory()
        i = 0
        # Для каждого защитника рисуем его картинку и картинку удаления
        for defender in myInventory:
            imageDefender = load_image(f'./defense/{defender}2.png')
            if defender == self.lighting:  # Если на него навёден курсор, то включаем подсветку
                pygame.draw.rect(self.screen, (135, 206, 235),
                                 ((self.side + 10) * i + 10 + self.width // 2, 150, self.side, self.side))
            self.screen.blit(imageDefender, ((self.side + 10) * i + 10 + self.width // 2 + self.side // 2
                                             - imageDefender.get_width() // 2,
                                             self.side // 2 - imageDefender.get_height() // 2 + 150))
            self.screen.blit(imageRemove, ((self.side + 10) * i + self.width // 2 + self.side
                                           - imageRemove.get_width(), 160))
            i += 1
        # Незаполненные клетки заполняем текстом: "Пусто!"
        text = self.font75.render('Пусто!', True, black)
        for i in range(5 - len(myInventory)):
            self.screen.blit(text, ((self.side + 10) * (4 - i) + 10 + self.width // 2 + self.side // 2
                                    - text.get_width() // 2, self.side // 2 - text.get_height() // 2 + 150))

    # Риисуем остальную часть снаряжения
    def drawAllEquipment(self):
        myEquipment = getEquipment()
        myInventory = getInventory()
        i = 0
        imageLock = load_image('./decor/other/lock.png')
        imageLock = pygame.transform.scale(imageLock, (32, 32))
        imageCrediti = load_image('./decor/money/Crediti.png')
        imageCrediti = pygame.transform.scale(imageCrediti, (32, 32))
        imagePlus = load_image('./decor/other/plus.png')
        imagePlus = pygame.transform.scale(imagePlus, (16, 16))
        # Далее мы просто смотрим, какие куплены, но не в инвентаре и не куплены
        # В зависимости от этого рисуем замочек и цену
        for defender in self.equipment:
            if defender not in myInventory:
                if defender == self.lighting:
                    pygame.draw.rect(self.screen, (135, 206, 235),
                                     ((self.side + 10) * (i % 4) + 10, 150 + (self.side + 10) * (i // 4), self.side,
                                      self.side))
                imageDefender = load_image(f'./defense/{defender}2.png')
                self.screen.blit(imageDefender,
                                 ((self.side + 10) * (i % 4) + 10 + self.side // 2 - imageDefender.get_width() // 2,
                                  self.side // 2 - imageDefender.get_height() // 2 + 150 + (self.side + 10) * (i // 4)))
            if defender not in myEquipment:
                price = self.equipment[defender]
                text = self.font30.render(price, True, black)
                self.screen.blit(text, ((self.side + 10) * (i % 4) + 20, 160 + (self.side + 10) * (i // 4)))
                self.screen.blit(imageCrediti, (
                    (self.side + 10) * (i % 4) + 25 + text.get_width(), 150 + (self.side + 10) * (i // 4)))
                self.screen.blit(imageLock, ((self.side + 10) * (i % 4) + 10 + self.side - 40,
                                             150 + self.side - 40 + (self.side + 10) * (i // 4)))
            if defender in myEquipment and defender not in myInventory:
                self.screen.blit(imagePlus, (
                    (self.side + 10) * (i % 4) + self.side - imagePlus.get_width(), 160 + (self.side + 10) * (i // 4)))
            if defender not in myInventory:
                i += 1

    # Рисуем опрос о том, хочет ли человек купить это
    def drawIfBuy(self):
        text1 = self.font75.render('Вы действительно хотите купить?', True, black)
        text2 = self.font30.render('Да', True, black)
        text3 = self.font30.render('Отмена', True, black)
        x, y = (self.width // 2 - text1.get_width() // 2, self.height // 2 - text1.get_height() // 2)
        pygame.draw.rect(self.screen, (255, 245, 238), (x - 20, y - 20, text1.get_width() + 40,
                                                        text1.get_height() + text2.get_height() + text3.get_height()
                                                        + 40), 0)
        pygame.draw.rect(self.screen, black, (x - 20, y - 20, text1.get_width() + 40,
                                              text1.get_height() + text2.get_height() + text3.get_height() + 40), 2)
        self.screen.blit(text1, (x, y))
        self.screen.blit(text2, (x + 650, y + 75))
        self.screen.blit(text3, (x + 750, y + 75))

    # Проверяем, нажал ли на кнопку чпользователь. Если да, то на какую
    def ifBuyClick(self, coords):
        mx, my = coords
        text1 = self.font75.render('Вы действительно хотите купить?', True, black)
        text2 = self.font30.render('Да', True, black)
        text3 = self.font30.render('Отмена', True, black)
        x, y = (self.width // 2 - text1.get_width() // 2, self.height // 2 - text1.get_height() // 2)
        if x + 650 <= mx <= x + 650 + text2.get_width() and y + 75 <= my <= y + 75 + text2.get_height():
            return 'Yes'
        if x + 750 <= mx <= x + 750 + text3.get_width() and y + 75 <= my <= y + 75 + text3.get_height():
            return 'No'

    # Функция для определения места нажатия
    def btnClick(self, coords):
        myInventory = getInventory()
        x, y = coords
        i = 0
        # Для этого просто проверяем, произошло ли место нажатия в какой-либо клетке
        if 10 <= x <= 42 and 10 <= y <= 42:
            return 'Назад'
        for defender in self.equipment:
            if defender not in myInventory:
                if (self.side + 10) * (i % 4) + 10 <= x <= (self.side + 10) * (i % 4) + 10 + self.side and \
                        150 + (self.side + 10) * (i // 4) <= y <= 150 + (self.side + 10) * (i // 4) + self.side:
                    return defender
                i += 1
        i = 0
        for defender in myInventory:
            if (self.side + 10) * i + 10 + self.width // 2 <= x <= (self.side + 10) * i + 10 + \
                    self.width // 2 + self.side and 150 <= y <= 150 + self.side:
                return defender
            i += 1

    # Функция, дающая подсветку
    def backlight(self, defender):
        if defender in self.equipment:
            self.lighting = defender
        else:
            self.lighting = None

    # Выводит текст о нехватке средств
    def noMoney(self):
        text = self.font75.render('Недостаточно средств!', True, (255, 36, 0))
        self.screen.blit(text, (self.width // 2 - text.get_width() // 2, self.height // 2 - text.get_height() // 2))

    # Выводит текст о нехватке места
    def noPlace(self):
        text = self.font75.render('Инвентарь заполнен!', True, (255, 36, 0))
        self.screen.blit(text, (self.width // 2 - text.get_width() // 2, self.height // 2 - text.get_height() // 2))

    # Выводит текст о мимнимальном количестве защитников в инвентаре
    def lastPlace(self):
        text = self.font75.render('Нельзя оставлять пустой инвентарь!', True, (255, 36, 0))
        self.screen.blit(text, (self.width // 2 - text.get_width() // 2, self.height // 2 - text.get_height() // 2))

    # Рисует окно
    def doEquipment(self):
        self.drawSeparator()
        self.drawBack()
        self.drawCells()
        self.drawMyEquipment()
        self.drawAllEquipment()
        self.drawText()
