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
        self.btns = []  # Список всех кнопок

    def find(self, x, width):  # Функция определения границ кнопок
        if x < self.xRect:  # Если граница этой кнопки начинается раньше заданной, то новая и является нужной
            self.xRect = x
            self.widthRect = width

    def draw(self, text, n):  # Функция отрисовки кнокпи
        btn = self.font.render(text, True, self.textColor)  # Создаём кнопку
        x, y = (self.width // 2 - btn.get_width() // 2,
                self.height // 2 - btn.get_height() // 2 + 100 * (n - 1))  # Считаем координаты кнокпи
        self.screen.blit(btn, (x, y))  # Рисуем кнопку
        # Далее вокруг кнопки рисуется прямоугольник в случаях, когда границы уже определены и когда ещё нет
        if self.xRect == self.width and self.widthRect == 0:  # Границы не определены
            pygame.draw.rect(self.screen, self.textColor, (x - 10, y - 10,
                                                           btn.get_width() + 20, btn.get_height() + 20), 3)
        else:  # Границы определены
            pygame.draw.rect(self.screen, self.textColor, (self.xRect - 10, y - 10,
                                                           self.widthRect + 20, btn.get_height() + 20), 3)
        self.find(x, btn.get_width())  # Функция для определения границ
        self.btns.append(text)

    def btnClick(self, coords):
        x, y = coords
        for i in range(len(self.btns)):
            # Создаём уже существующую кнопку для определения соответствующего ей прямоугольника
            btn = self.font.render(self.btns[i], True, self.textColor)
            # Проверяем, попадают ли данные координаты в прямоугольник кнопки
            if self.xRect - 10 <= x <= self.xRect + 10 + self.widthRect \
                    and self.height // 2 - btn.get_height() // 2 + 100 * i \
                    - 10 <= y <= self.height // 2 - btn.get_height() // 2 + 100 * \
                    i + 10 + btn.get_height():
                return self.btns[i]  # Если да, то возвращаем кнопку
