#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Authors: dasdas97d, 
# Consultant: grishnan
# Emails: khozyainov.maksim@yandex.ru grishnan@gmail.com
# License: CC BY-SA 3.0
# Description(ru): Сетевая игра «Морской бой». Предназначена для запуска в локальной сети для двух игроков

import pygame, random, time
from classes import *
from threading import Thread
pygame.init()
clock = pygame.time.Clock()

''' глобальные константы '''
WIDTH_SCREEN, HEIGHT_SCREEN = 1014, 768 # размеры окна
POS_FIELD1  = (265, 250) # координаты центра первого игрового поля
POS_FIELD2  = (750, 250) # координаты центра второго игрового поля
SIZE_FIELD  = 428        # ширина и высота игрового поля
FPS         = 2          # кадров в секунду
FLAGRECV    = False

SCREEN = pygame.display.set_mode((WIDTH_SCREEN, HEIGHT_SCREEN - 100))
pygame.display.set_caption("Sea Fight")

''' игровые объекты '''
field1 = MyField(POS_FIELD1, SIZE_FIELD)
field2 = EnemyField(POS_FIELD2, SIZE_FIELD)

''' создание потока '''

sockobj = socket(AF_INET, SOCK_STREAM)

while True:
  ''' обработчик событий '''
  for event in pygame.event.get():
    if event.type == QUIT:
      sockobj.close()
      pygame.quit()
      sys.exit()
    elif event.type == MOUSEBUTTONDOWN:
      mousex, mousey = event.pos
      
  if not FLAGRECV:
    FLAGRECV = True
    t = Thread(target=sockobj.connect((SERVERHOST, SERVERPORT)), args=((SERVERHOST, SERVERPORT),))
    t.start()
    data = sockobj.recv(1024)
    print(data)
    if data != None:
      del(t)
  else:
    FLAGRECV = False
  ''' отрисовка игрового поля '''
  SCREEN.fill(WHITE)
  field1.Draw(SCREEN)
  field2.Draw(SCREEN)
  for ship in field1.ships: ship.Draw(SCREEN, field1)
  pygame.display.update()
  clock.tick(FPS)
