import pygame
from Functions import load_image, black


class Play:
    def __init__(self, screen, screenSize, name):
        self.screen = screen  # Экран
        self.screenSize = screenSize  # Размер экрана
        self.font = pygame.font.Font(None, 100)  # Размер шрифта
        self.width, self.height = screenSize  # Ширина и высота экрана
        self.xRect = self.width  # Граница начала кнопки
        self.widthRect = 0  # Граница конца кнопки
        self.btns = []  # Список всех кнопок
        self.name = name  # Название картинки стрелочки

    def find(self, x, width):  # Функция определения границ кнопок
        if x < self.xRect:  # Если граница этой кнопки начинается раньше заданной, то новая и является нужной
            self.xRect = x
            self.widthRect = width

    def drawMode(self, text, n):  # Функция отрисовки кнокпи
        if text == 'Лёгкий':
            color = (0, 255, 0)
            change = -100
        elif text == 'Средний':
            color = (255, 255, 0)
            change = 0
        elif text == 'Сложный':
            color = (255, 0, 0)
            change = 100
        btn = self.font.render(text, True, color)  # Создаём кнопку
        x, y = (self.width // 2 - btn.get_width() // 2,
                self.height // 2 - btn.get_height() // 2 + change)  # Считаем координаты кнокпи
        self.screen.blit(btn, (x, y))  # Рисуем кнопку
        # Далее вокруг кнопки рисуется прямоугольник в случаях, когда границы уже определены и когда ещё нет
        if self.xRect == self.width and self.widthRect == 0:  # Границы не определены
            pygame.draw.rect(self.screen, color, (x - 10, y - 10,
                                                  btn.get_width() + 20, btn.get_height() + 20), 3)
        else:  # Границы определены
            pygame.draw.rect(self.screen, color, (self.xRect - 10, y - 10,
                                                  self.widthRect + 20, btn.get_height() + 20), 3)
        self.find(x, btn.get_width())  # Функция для определения границ
        self.btns.append(text)

    def drawBack(self):
        image = load_image(self.name)
        image = pygame.transform.scale(image, (32, 32))
        self.screen.blit(image, (10, 15))

    def btnClick(self, coords):
        x, y = coords
        if 10 <= x <= 42 and 10 <= y <= 42:
            return 'Назад'
        for i in range(len(self.btns)):
            # Создаём уже существующую кнопку для определения соответствующего ей прямоугольника
            btn = self.font.render(self.btns[i], True, (0, 0, 0))
            # Проверяем, попадают ли данные координаты в прямоугольник кнопки
            if self.xRect - 10 <= x <= self.xRect + 10 + self.widthRect \
                    and self.height // 2 - btn.get_height() // 2 + 100 * (i - 1)\
                    - 10 <= y <= self.height // 2 - btn.get_height() // 2 + 100 * \
                    (i - 1) + 10 + btn.get_height():
                return self.btns[i]  # Если да, то возвращаем кнопку

    def doPlay(self):
        self.drawMode("Лёгкий", 1)
        self.drawMode("Средний", 2)
        self.drawMode("Сложный", 3)
        self.drawBack()
