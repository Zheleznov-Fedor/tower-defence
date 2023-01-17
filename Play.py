# Всё, что нам нужно:
import pygame
from Utils import load_image, black


class Play:
    def __init__(self, screen, screenSize, name):
        self.screen = screen  # Экран
        self.screenSize = screenSize  # Размер экрана
        self.font = pygame.font.Font(None, 100)  # Размер шрифта
        self.width, self.height = screenSize  # Ширина и высота экрана
        self.xRect = self.width  # Граница начала кнопки
        self.widthRect = 0  # Граница конца кнопки
        self.btns = {}  # Словарь всех кнопок
        self.name = name  # Название картинки стрелочки
        # Словарь цветов кнопок
        self.colors = {'Лёгкий': (152, 255, 152), 'Средний': (255, 255, 0), 'Сложный': (255, 36, 0)}

    def find(self, x, width):  # Функция определения границ кнопок
        if x < self.xRect:  # Если граница этой кнопки начинается раньше заданной, то новая и является нужной
            self.xRect = x
            self.widthRect = width

    def drawMode(self, text, n):  # Функция отрисовки кнокпи
        # В зависимости от кнопки, добавляем ей изменения координат
        if text == 'Лёгкий':
            change = -100
        elif text == 'Средний':
            change = 0
        elif text == 'Сложный':
            change = 100
        color = self.colors[text]  # Берём её цвет из словаря цветов кнопок
        btn = self.font.render(text, True, color)  # Создаём кнопку
        x, y = (self.width // 2 - btn.get_width() // 2,
                self.height // 2 - btn.get_height() // 2 + change)  # Считаем координаты кнокпи
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

    # Функция, рисующая кнопку назад
    def drawBack(self):
        image = load_image(self.name)
        image = pygame.transform.scale(image, (32, 32))
        self.screen.blit(image, (10, 15))

    # Функция для определения места нажатия
    def btnClick(self, coords):
        x, y = coords
        if 10 <= x <= 42 and 10 <= y <= 42:
            return 'Назад'
        # Это очень легко проверить, потому что есть словарь с координатами кнопок
        for btn in self.btns.keys():
            x1, y1, x2, y2 = self.btns[btn]
            if x1 <= x <= x1 + x2 and y1 <= y <= y1 + y2:
                return btn

    # Функция подсветки кнопок
    def backlight(self, btn):
        self.colors['Лёгкий'] = (152, 255, 152)
        self.colors['Средний'] = (255, 255, 0)
        self.colors['Сложный'] = (255, 36, 0)
        if btn in self.colors.keys():
            self.colors[btn] = (135, 206, 235)

    # Функция отрисовки окна
    def doPlay(self):
        self.drawMode("Лёгкий", 1)
        self.drawMode("Средний", 2)
        self.drawMode("Сложный", 3)
        self.drawBack()
