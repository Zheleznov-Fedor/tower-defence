import pygame
from Functions import load_image


class Equipment:
    def __init__(self, screen, screenSize, name):
        self.screen = screen  # Экран
        self.screenSize = screenSize  # Размер экрана
        self.font = pygame.font.Font(None, 100)  # Размер шрифта
        self.width, self.height = screenSize  # Ширина и высота экрана
        self.xRect = self.width  # Граница начала кнопки
        self.widthRect = 0  # Граница конца кнопки
        self.btns = []  # Список всех кнопок
        self.name = name  # Название картинки стрелочки
        self.side = (self.width // 2 - 50) // 4

    def drawSeparator(self):
        pygame.draw.line(self.screen, (0, 0, 0), (self.width // 2, 65), (self.width // 2, self.height), width=2)

    def drawBack(self):
        image = load_image(self.name)
        image = pygame.transform.scale(image, (32, 32))
        self.screen.blit(image, (10, 15))

    def drawCells(self):
        image = load_image('./decor/other/lock.png')
        image = pygame.transform.scale(image, (32, 32))
        for i in range(4):
            pygame.draw.rect(self.screen, (192, 198, 200),
                             ((self.side + 10) * i + 10, 75, self.side, self.side), 0)
            self.screen.blit(image, ((self.side + 10) * i + 10 + self.side - 40,
                                     75 + self.side - 40))
            pygame.draw.rect(self.screen, (192, 198, 200),
                             ((self.side + 10) * i + 10 + self.width // 2, 75, self.side, self.side), 0)
