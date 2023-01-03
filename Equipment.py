import pygame
from Functions import load_image, getEquipment, black


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
        self.equipment = {'Solider': '0', 'Gun': '500', 'Plane': '1500', 'RocketLauncher': '2000', 'Laser': '2500'}

    def drawSeparator(self):
        pygame.draw.line(self.screen, black, (self.width // 2, 65), (self.width // 2, self.height), width=2)

    def drawBack(self):
        image = load_image(self.name)
        image = pygame.transform.scale(image, (32, 32))
        self.screen.blit(image, (10, 15))

    def drawText(self):
        font = pygame.font.Font(None, 75)
        text1 = font.render('Снаряжение:', True, black)
        text2 = font.render('Ваш инвентарь:', True, black)
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
        font = pygame.font.Font(None, 50)
        text = font.render('Пусто!', True, black)
        for i in range(5 - len(myEquipment)):
            self.screen.blit(text, ((self.side + 10) * (4 - i) + 10 + self.width // 2 + self.side // 2
                                    - text.get_width() // 2, self.side // 2 - text.get_height() // 2 + 150))

    def drawAllEquipment(self):
        myEquipment = getEquipment()
        i = 0
        font = pygame.font.Font(None, 30)
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
                text = font.render(price, True, black)
                self.screen.blit(text, ((self.side + 10) * (i % 4) + 20, 160 + (self.side + 10) * (i // 4)))
                self.screen.blit(imageCrediti, (
                    (self.side + 10) * (i % 4) + 25 + text.get_width(), 150 + (self.side + 10) * (i // 4)))
                self.screen.blit(imageLock, ((self.side + 10) * (i % 4) + 10 + self.side - 40,
                                             150 + self.side - 40 + (self.side + 10) * (i // 4)))
            i += 1

    def btnClick(self, coords):
        x, y = coords
        if 10 <= x <= 42 and 10 <= y <= 42:
            return 'Назад'

    def doEquipment(self):
        self.drawSeparator()
        self.drawBack()
        self.drawCells()
        self.drawMyEquipment()
        self.drawAllEquipment()
        self.drawText()
