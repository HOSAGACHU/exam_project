#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Authors: dasdas97d, 
# Consultant: grishnan
# Emails: khozyainov.maksim@yandex.ru grishnan@gmail.com
# License: CC BY-SA 3.0
# Description(ru): Сетевая игра «Морской бой». Предназначена для запуска в локальной сети для двух игроков

import pygame, random
from classes import *
import time
from threading import Thread

pygame.init()

''' глобальные константы '''
WIDTH_SCREEN, HEIGHT_SCREEN = 1014, 768 # размеры окна
POS_FIELD1  = (265, 250) # координаты центра первого игрового поля
POS_FIELD2  = (750, 250) # координаты центра второго игрового поля
SIZE_FIELD  = 428        # ширина и высота игрового поля

SCREEN = pygame.display.set_mode((WIDTH_SCREEN, HEIGHT_SCREEN - 100))
pygame.display.set_caption("Sea Fight")

''' игровые объекты '''
field1 = MyField(POS_FIELD1, SIZE_FIELD)
field2 = EnemyField(POS_FIELD2, SIZE_FIELD)

''' объект соединения '''
connect = Connect()
t = Thread(target=connect.WaitConnect)
t.start()

while True:
  ''' обработчик событий '''
  for event in pygame.event.get():
    if event.type == QUIT:
      del(t)
      connect.connection.close() # закрываем сетевое соединение
      pygame.quit()              # деактивируем pygame
      sys.exit()                 # системный выход
    elif event.type == MOUSEBUTTONDOWN:
      mousex, mousey = event.pos
      print(field2.fromGlobalToLocal(mousex, mousey))
      connect.connection.send(str.encode(str(mousex)) + b'.' + str.encode(str(mousey)))
                  
  ''' отрисовка игрового поля '''
  SCREEN.fill(WHITE)
  field1.Draw(SCREEN)
  field2.Draw(SCREEN)
  for ship in field1.ships: ship.Draw(SCREEN, field1)
  pygame.display.update()
