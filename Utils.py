import os
import sys
import pygame

black = (30, 30, 30)
allEquipment = {'Solider': '0', 'Gun': '500', 'Farm': '1000',
                'RocketLauncher': '2000', 'Laser': '2500'}
ENEMIES_INFO = {
    '0':
        {
            'hp': 100,
            'image_filename': 'lvl0.png',
            'height': 50,
            'step': 1,
            'angle_step': 0.4,
            'needs_rotate': True
        },
    '1':
        {
            'hp': 250,
            'image_filename': 'lvl1.png',
            'height': 50,
            'step': 1,
            'angle_step': 0.4,
            'needs_rotate': True
        },
    '2':
        {
            'hp': 500,
            'image_filename': 'lvl2.png',
            'height': 50,
            'step': 1,
            'angle_step': 0.3,
            'needs_rotate': True
        },
    '3':
        {
            'hp': 1000,
            'image_filename': 'lvl3.png',
            'height': 50,
            'step': 1,
            'angle_step': 0.3,
            'needs_rotate': True
        },
}
TOWERS_INFO = {  # Настройки каждой башни
    'Solider':  # У Мити опечатка, правильно Soldier
        {
            'price': 200,  # Цена внутри матча
            'place_type': 'default',  # Тип места размещения
            'x_offset': 0,  # Сдвиг по горизонтали, для правильного размещения
            'y_offset': 0,  # Сдвиг по вертикали, для правильного размещения
            'max_size_in_match': 80,  # Максимальный размер картинки башни в матче
            'levels': [
                {
                    'image_filename': 'Solider2.png',  # Название файла картинки башни
                    'visible_radius': 250,  # Радиус на котором башня видит противников
                    'shoot_delay': 1000,  # Время перезарядки
                    'shoot_damage': 15,  # Урон выстрела
                    'missile_type': 'Bullet',  # Тип боеприпаса
                    'update_price': 200  # Цена обновления на новый уровень
                },
                {
                    'image_filename': 'Solider22.png',
                    'visible_radius': 250,
                    'shoot_delay': 400,
                    'shoot_damage': 15,
                    'missile_type': 'Bullet'
                }
            ]
        },
    'Gun':
        {
            'price': 300,
            'place_type': 'default',
            'x_offset': 18,
            'y_offset': -5,
            'max_size_in_match': 80,
            'levels': [
                {
                    'image_filename': 'Gun2.png',  # Название файла картинки башни
                    'visible_radius': 250,  # Радиус на котором башня видит противников
                    'shoot_delay': 400,  # Время перезарядки
                    'shoot_damage': 15,  # Урон выстрела
                    'missile_type': 'Rocket1',  # Тип боеприпаса
                    'update_price': 200  # Цена обновления на новый уровень
                },
                {
                    'image_filename': 'Gun22.png',
                    'visible_radius': 250,
                    'shoot_delay': 400,
                    'shoot_damage': 15,
                    'missile_type': 'Rocket2'
                }
            ]
        },
    'Laser':
        {
            'price': 500,
            'place_type': 'default',
            'x_offset': 0,
            'y_offset': 0,
            'max_size_in_match': 80,
            'levels': [
                {
                    'image_filename': 'Laser2.png',  # Название файла картинки башни
                    'visible_radius': 250,  # Радиус на котором башня видит противников
                    'shoot_delay': 400,  # Время перезарядки
                    'shoot_damage': 15,  # Урон выстрела
                    'missile_type': 'Bullet',  # Тип боеприпаса
                    'update_price': 200  # Цена обновления на новый уровень
                },
                {
                    'image_filename': 'Laser22.png',
                    'visible_radius': 250,
                    'shoot_delay': 400,
                    'shoot_damage': 15,
                    'missile_type': 'Bullet'
                }
            ]
        },
    'Farm':
        {
            'price': 750,
            'place_type': 'farm',
            'x_offset': 37,
            'y_offset': 10,
            'max_size_in_match': 25,
            'levels': [
                {
                    'image_filename': 'Farm2.png',  # Название файла картинки башни
                    'income': 100,  # Доход приносимый фермой в начале каждой волны
                    'update_price': 200
                },
                {
                    'image_filename': 'Farm22.png',
                    'income': 300,  # Доход приносимый фермой в начале каждой волны
                }
            ]
        },
    'RocketLauncher':
        {
            'price': 400,
            'place_type': 'default',
            'x_offset': 0,
            'y_offset': 0,
            'max_size_in_match': 80,
            'x_center_offset': 0,
            'y_center_offset': 0,
            'levels': [
                {
                    'image_filename': 'RocketLauncher2.png',  # Название файла картинки башни
                    'visible_radius': 250,  # Радиус на котором башня видит противников
                    'shoot_delay': 400,  # Время перезарядки
                    'shoot_damage': 100,  # Урон выстрела
                    'missile_type': 'Rocket2',  # Тип боеприпаса
                    'update_price': 200  # Цена обновления на новый уровень
                },
                {
                    'image_filename': 'RocketLauncher22.png',
                    'visible_radius': 250,
                    'shoot_delay': 1500,
                    'shoot_damage': 150,
                    'missile_type': 'Rocket2'
                }
            ]
        }
}
MISSILES_INFO = {
    'Rocket1': {
        'image_filename': 'Rocket1.png',  # Название файла картинки боеприпаса
        'width_in_match': 20,  # Ширина картинки боеприпаса в матче
        'is_need_rotate': True,  # Нужен ли поворот при перемещении к цели
        'step': 3  # Скорость боеприпаса
    },
    'Rocket2': {
        'image_filename': 'Rocket2.png',
        'width_in_match': 20,
        'is_need_rotate': True,
        'step': 7
    },
    'Bullet': {
        'image_filename': 'Bullet.png',
        'width_in_match': 40,
        'is_need_rotate': False,
        'step': 15
    }
}
TILE_SIZE = 100


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def getEquipment():
    f = open("txt/Equipment.txt", 'r')
    equipment = ''.join((f.readlines())).split('\n')[1].split(', ')
    f.close()
    return equipment


def getInventory():
    f = open("txt/Equipment.txt", 'r')
    inventory = ''.join((f.readlines())).split('\n')[2].split(', ')
    f.close()
    return inventory


def addInventory(defender):
    f = open("txt/Equipment.txt", 'r')
    # Достаём остальные настройки для записи их обратно без изменений
    lines = ''.join(f.readlines()).split('\n')
    crediti = lines[0]
    equipment = lines[1]
    inventory = lines[2].split(', ')
    inventory.append(defender)
    f.close()
    f = open("txt/Equipment.txt", 'w')
    print(crediti, file=f)
    print(equipment, file=f)
    print(', '.join(inventory), file=f, end='')
    f.close()


def delInventory(defender):
    f = open("txt/Equipment.txt", 'r')
    # Достаём остальные настройки для записи их обратно без изменений
    lines = ''.join(f.readlines()).split('\n')
    crediti = lines[0]
    equipment = lines[1]
    inventory = lines[2].split(', ')
    inventory.remove(defender)
    f.close()
    f = open("txt/Equipment.txt", 'w')
    print(crediti, file=f)
    print(equipment, file=f)
    print(', '.join(inventory), file=f, end='')
    f.close()


def addEquipment(defender):
    f = open("txt/Equipment.txt", 'r')
    # Достаём остальные настройки для записи их обратно без изменений
    lines = ''.join(f.readlines()).split('\n')
    crediti = lines[0]
    equipment = lines[1].split(', ')
    inventory = lines[2]
    equipment.append(defender)
    f.close()
    f = open("txt/Equipment.txt", 'w')
    print(crediti, file=f)
    print(', '.join(equipment), file=f)
    print(inventory, file=f, end='')
    f.close()


def getCrediti():
    f = open("txt/Equipment.txt", 'r')
    crediti = ''.join((f.readlines())).split('\n')[0]
    f.close()
    return crediti


def addCrediti(howMany):
    f = open("txt/Equipment.txt", 'r')
    # Достаём остальные настройки для записи их обратно без изменений
    lines = ''.join(f.readlines()).split('\n')
    crediti = lines[0]
    equipment = lines[1]
    inventory = lines[2]
    f.close()
    f = open("txt/Equipment.txt", 'w')
    print(str(int(crediti) + howMany), file=f)
    print(equipment, file=f)
    print(inventory, file=f, end='')
    f.close()
