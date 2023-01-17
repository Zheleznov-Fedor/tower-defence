import pygame
from Functions import black


class Menu:
    def __init__(self, screen, screenSize):
        self.screen = screen  # Экран
        self.screenSize = screenSize  # Размер экрана
        self.textColor = black  # Цвет текста
        self.font = pygame.font.Font(None, 100)  # Размер шрифта
        self.width, self.height = screenSize  # Ширина и высота экрана
        self.xRect = self.width  # Граница начала кнопки
        self.widthRect = 0  # Граница конца кнопки
        self.btns = {}  # Словарь всех кнопок
        self.colors = {}  # Словарь цветов кнопок

    def find(self, x, width):  # Функция определения границ кнопок
        if x < self.xRect:  # Если граница этой кнопки начинается раньше заданной, то новая и является нужной
            self.xRect = x
            self.widthRect = width

    def draw(self, text, n):  # Функция отрисовки кнокпи
        if text in self.colors.keys():
            color = self.colors[text]
        else:
            color = self.textColor
            self.colors[text] = self.textColor
        btn = self.font.render(text, True, color)  # Создаём кнопку
        x, y = (self.width // 2 - btn.get_width() // 2,
                self.height // 2 - btn.get_height() // 2 + 100 * (n - 1))  # Считаем координаты кнокпи
        self.screen.blit(btn, (x, y))  # Рисуем кнопку
        # Далее вокруг кнопки рисуется прямоугольник в случаях, когда границы уже определены и когда ещё нет
        if self.xRect == self.width and self.widthRect == 0:  # Границы не определены
            pygame.draw.rect(self.screen, color, (x - 10, y - 10,
                                                  btn.get_width() + 20, btn.get_height() + 20), 3)
            self.btns[text] = (x - 10, y - 10,
                               btn.get_width() + 20, btn.get_height() + 20)
        else:  # Границы определены
            pygame.draw.rect(self.screen, color, (self.xRect - 10, y - 10,
                                                  self.widthRect + 20, btn.get_height() + 20), 3)
            self.btns[text] = (self.xRect - 10, y - 10,
                               self.widthRect + 20, btn.get_height() + 20)
        self.find(x, btn.get_width())  # Функция для определения границ

    # Функция для определения места нажатия
    def btnClick(self, coords):
        x, y = coords
        # Это очень легко проверить, потому что есть словарь с координатами кнопок
        for btn in self.btns.keys():
            x1, y1, x2, y2 = self.btns[btn]
            if x1 <= x <= x1 + x2 and y1 <= y <= y1 + y2:
                return btn  # Если да, то возвращаем кнопку

    # Функция подсветки кнопок
    def backlight(self, btn):
        for elem in self.colors.keys():
            self.colors[elem] = self.textColor
        if btn in self.colors.keys():
            self.colors[btn] = (135, 206, 235)
