import pygame

from Menu import Menu
from Play import Play
from Equipment import Equipment
from Functions import drawMenu, drawPlay, drawEquipment

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Tower Defense')  # Название окна
    size = width, height = 1600, 900  # Размер окна
    screen = pygame.display.set_mode(size)  # Задаём экран для работы с ним
    running = True  # Работа программы
    screenColor = (255, 245, 238)  # Цвет экрана
    menu = Menu(screen, size)  # Создаём меню
    play = Play(screen, size, './decor/buttons/BtnBack.png')
    equipment = Equipment(screen, size, './decor/buttons/BtnBack.png')
    while running:
        screen.fill(screenColor)  # Заполняем экран соответствующим цветом
        # Рисуем 3 кнопки:
        drawMenu(menu)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Если происходит выход из окна, заканчиваем программу
                running = False
            if event.type == pygame.MOUSEBUTTONUP:  # Если происходит нажатие мыши, проверяем, была ли нажата кнопка
                if menu.btnClick(event.pos) == 'Играть':
                    print(drawPlay(play, screenColor))
                if menu.btnClick(event.pos) == 'Снаряжение':
                    print(drawEquipment(equipment, screenColor))
        pygame.display.flip()  # Обновляем экран
