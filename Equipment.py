import pygame
from Functions import load_image, getEquipment, black, allEquipment


class Equipment:
    def __init__(self, screen, screenSize, name):
        self.screen = screen  # Экран
        self.screenSize = screenSize  # Размер экрана
        self.width, self.height = screenSize  # Ширина и высота экрана
        self.xRect = self.width  # Граница начала кнопки
        self.widthRect = 0  # Граница конца кнопки
        self.btns = []  # Список всех кнопок
        self.name = name  # Название картинки стрелочки
        self.side = (self.width // 2 - 50) // 4
        self.equipment = allEquipment
        self.font75 = pygame.font.Font(None, 75)
        self.font30 = pygame.font.Font(None, 30)

    def drawSeparator(self):
        pygame.draw.line(self.screen, black, (self.width // 2, 65), (self.width // 2, self.height), width=2)

    def drawBack(self):
        image = load_image(self.name)
        image = pygame.transform.scale(image, (32, 32))
        self.screen.blit(image, (10, 15))

    def drawText(self):
        text1 = self.font75.render('Снаряжение:', True, black)
        text2 = self.font75.render('Ваш инвентарь:', True, black)
        self.screen.blit(text1, (self.width // 4 - text1.get_width() // 2, 75))
        self.screen.blit(text2, (self.width // 4 - text2.get_width() // 2 + self.width // 2, 75))
        pygame.draw.line(self.screen, black, (0, 130), (self.width, 130), width=2)

    def drawCells(self):
        image = load_image('./decor/other/lock.png')
        image = pygame.transform.scale(image, (32, 32))
        for i in range(len(self.equipment)):
            pygame.draw.rect(self.screen, (192, 198, 200),
                             ((self.side + 10) * (i % 4) + 10, 150 + (self.side + 10) * (i // 4), self.side, self.side),
                             0)
        for i in range(4):
            pygame.draw.rect(self.screen, (192, 198, 200),
                             ((self.side + 10) * i + 10 + self.width // 2, 150, self.side, self.side), 0)

    def drawMyEquipment(self):
        myEquipment = getEquipment()
        i = 0
        for defender in myEquipment:
            image = load_image(f'./defense/{defender}2.png')
            self.screen.blit(image, ((self.side + 10) * i + 10 + self.width // 2 + self.side // 2
                                     - image.get_width() // 2, self.side // 2 - image.get_height() // 2 + 150))
            i += 1
        text = self.font75.render('Пусто!', True, black)
        for i in range(5 - len(myEquipment)):
            self.screen.blit(text, ((self.side + 10) * (4 - i) + 10 + self.width // 2 + self.side // 2
                                    - text.get_width() // 2, self.side // 2 - text.get_height() // 2 + 150))

    def drawAllEquipment(self):
        myEquipment = getEquipment()
        i = 0
        imageLock = load_image('./decor/other/lock.png')
        imageLock = pygame.transform.scale(imageLock, (32, 32))
        imageCrediti = load_image('./decor/money/Crediti.png')
        imageCrediti = pygame.transform.scale(imageCrediti, (32, 32))
        for defender in self.equipment:
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
            i += 1

    def drawIfBuy(self):
        text1 = self.font75.render('Вы действительно хотите купить?', True, black)
        text2 = self.font30.render('Да', True, black)
        text3 = self.font30.render('Отмена', True, black)
        x, y = (self.width // 2 - text1.get_width() // 2, self.height // 2 - text1.get_height() // 2)
        self.screen.blit(text1, (x, y))
        self.screen.blit(text2, (x + 650, y + 75))
        self.screen.blit(text3, (x + 750, y + 75))

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

    def btnClick(self, coords):
        x, y = coords
        if 10 <= x <= 42 and 10 <= y <= 42:
            return 'Назад'
        for i in range(len(self.equipment)):
            if (self.side + 10) * (i % 4) + 10 <= x <= (self.side + 10) * (i % 4) + 10 + self.side and \
                    150 + (self.side + 10) * (i // 4) <= y <= 150 + (self.side + 10) * (i // 4) + self.side:
                return list(self.equipment.keys())[i]

    def doEquipment(self):
        self.drawSeparator()
        self.drawBack()
        self.drawCells()
        self.drawMyEquipment()
        self.drawAllEquipment()
        self.drawText()
