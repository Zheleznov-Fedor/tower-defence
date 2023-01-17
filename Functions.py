import pygame
from Game import Game
from Utils import getEquipment, black, getCrediti, load_image, addEquipment,\
    addCrediti, allEquipment, getInventory, addInventory, delInventory


def drawHeader(name, screen, size):
    font = pygame.font.Font(None, 75)
    text = font.render(name, True, black)
    width, height = size  # Ширина и высота экрана
    x, y = width // 2 - text.get_width() // 2, 10
    pygame.draw.line(screen, black, (0, 65), (width, 65), width=2)
    screen.blit(text, (x, y))


def drawCrediti(screen, size):
    font = pygame.font.Font(None, 40)
    crediti = getCrediti()
    text = font.render(': ' + crediti, True, black)
    image = load_image('./decor/money/Crediti.png')
    image = pygame.transform.scale(image, (64, 64))
    width, height = size  # Ширина и высота экрана
    x, y = width - text.get_width() - 104, 0
    screen.blit(image, (x, y))
    screen.blit(text, (x + 64, y + 30))


def drawMenu(menu):
    menu.draw("Играть", 1)
    menu.draw("Снаряжение", 2)
    menu.draw("Настройки", 3)


def drawPlay(play, screenColor):
    running = True
    while running:
        play.screen.fill(screenColor)
        play.doPlay()
        drawCrediti(play.screen, play.screenSize)
        drawHeader('Играть', play.screen, play.screenSize)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Если происходит выход из окна, заканчиваем программу
                running = False
            if event.type == pygame.MOUSEBUTTONUP:  # Если происходит нажатие мыши, проверяем, была ли нажата кнопка
                click = play.btnClick(event.pos)
                print(click)
                if click is not None:
                    if click == 'Назад':
                        return
                    elif click == 'Лёгкий':
                        game = Game(play.screen, 'test.csv', 15)
                        game.draw()
                    elif click == 'Средний':
                        game = Game(play.screen, 'test.csv', 20)
                        game.draw()
                    elif click == 'Сложный':
                        game = Game(play.screen, 'test.csv', 25)
                        game.draw()
            if event.type == pygame.MOUSEMOTION:
                click = play.btnClick(event.pos)
                play.backlight(click)
        pygame.display.flip()
    return


def drawEquipment(equipment, screenColor):
    running, wantBuy, noplace, nomoney, lastplace = (True, False, False, False, False)
    wantBuy = False
    whatBuy = ''
    fps = 120
    time = 0
    clock = pygame.time.Clock()
    while running:
        equipment.screen.fill(screenColor)
        equipment.screen.set_alpha(200)
        equipment.doEquipment()
        drawCrediti(equipment.screen, equipment.screenSize)
        drawHeader('Снаряжение', equipment.screen, equipment.screenSize)
        if wantBuy:
            equipment.drawIfBuy()
        if noplace:
            equipment.noPlace()
            time += 1
            if time > 20:
                noplace = False
                time = 0
        if nomoney:
            equipment.noMoney()
            time += 1
            if time > 20:
                nomoney = False
                time = 0
        if lastplace:
            equipment.lastPlace()
            time += 1
            if time > 20:
                lastplace = False
                time = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Если происходит выход из окна, заканчиваем программу
                running = False
            if event.type == pygame.MOUSEBUTTONUP:  # Если происходит нажатие мыши, проверяем, была ли нажата кнопка
                if wantBuy:
                    buy = equipment.ifBuyClick(event.pos)
                    if buy == 'Yes':
                        addEquipment(whatBuy)
                        addCrediti(-int(allEquipment[whatBuy]))
                        wantBuy = False
                    elif buy == 'No':
                        wantBuy = False
                click = equipment.btnClick(event.pos)
                print(click)
                if click is not None:
                    if click == 'Назад':
                        return
                    else:
                        whatBuy = click
                        myEquipment = getEquipment()
                        myInventory = getInventory()
                        if click not in myEquipment:
                            needCrediti = int(allEquipment[whatBuy])
                            myCrediti = int(getCrediti())
                            if myCrediti >= needCrediti:
                                wantBuy = True
                            else:
                                nomoney = True
                        elif click in myEquipment and click not in myInventory:
                            if len(myInventory) < 4:
                                addInventory(click)
                            else:
                                noplace = True
                        elif click in myInventory:
                            if len(myInventory) > 1:
                                delInventory(click)
                            else:
                                lastplace = True
            if event.type == pygame.MOUSEMOTION:
                click = equipment.btnClick(event.pos)
                equipment.backlight(click)
        clock.tick(fps)
        pygame.display.flip()
    return

"""
def drawEnd(result, wave, screen, screenSize):
    width, height = screenSize
    if wave <= 15:
        income = wave * 5
    elif 15 < wave <= 20:
        income = 75 + (wave - 15) * 10
    elif wave > 20:
        income = 125 + (wave - 20) * 15
    if result == 'win':
        text = 'Вы выиграли!'
        income += 100
        color = (40, 114, 51)
    elif result == 'lose':
        text = 'Вы проиграли!'
        color = (255, 36, 0)
    font150 = pygame.font.Font(None, 150)
    font100 = pygame.font.Font(None, 100)
    inscription = font150.render(text, True, color)
    total = font100.render(f"Итого волн: {str(wave)}", True, color)
    incomeText = font100.render(f"Получено: +{str(income)}", True, color)
    x, y = (width // 2 - inscription.get_width() // 2, height // 2 - inscription.get_height() // 2)
    pygame.draw.rect(screen, (255, 245, 238), (x - 20, y - 20, inscription.get_width() + 40,
                                               inscription.get_height() + incomeText.get_height() + total.get_height()
                                               + 40), 0)
    pygame.draw.rect(screen, color, (x - 20, y - 20, inscription.get_width() + 40,
                                     inscription.get_height() + incomeText.get_height() + total.get_height() + 40), 2)
    pygame.draw.rect(screen, color, (x - 20, y - 20, inscription.get_width() + 40, inscription.get_height() + 30), 2)
    screen.blit(inscription, (x, y))
    screen.blit(total, (x, height // 2 - incomeText.get_height() // 2 + inscription.get_height()))
    screen.blit(incomeText,
                (x, height // 2 - incomeText.get_height() // 2 + inscription.get_height() + total.get_height()))
    addCrediti(income)
"""
