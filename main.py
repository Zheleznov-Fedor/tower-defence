import pygame

from Menu import Menu

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Tower Defense')  # Название окна
    size = width, height = 1600, 900  # Размер окна
    screen = pygame.display.set_mode(size)  # Задаём экран для работы с ним
    running = True  # Работа программы
    screenColor = (255, 255, 255)  # Цвет экрана
    textColor = (0, 0, 0)  # Цвет текста
    menu = Menu(screen, size, textColor)  # Создаём меню
    while running:
        screen.fill(screenColor)  # Заполняем экран соответствующим цветом
        # Рисуем 3 кнопки:
        menu.draw("Играть", 1)
        menu.draw("Снаряжение", 2)
        menu.draw("Настройки", 3)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Если происходит выход из окна, заканчиваем программу
                running = False
            if event.type == pygame.MOUSEBUTTONUP:  # Если происходит нажатие мыши, проверяем, была ли нажата кнопка
                print(menu.btnClick(event.pos))
        pygame.display.flip()  # Обновляем экран
