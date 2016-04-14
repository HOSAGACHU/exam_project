import pygame, random, sys, pygame.gfxdraw, os
from pygame.locals import *
from socket import *

''' ГЛОБАЛЬНЫЕ КОНСТАНТЫ '''
WHITE      = (255, 255, 255)
BLACK      = (  0,   0,   0)
PICS       = "pics"
SERVERHOST = ''              # сетевой интерфейс сервера
SERVERPORT = 12345           # TCP-порт
  
class Ship(pygame.Surface):
  ''' класс кораблей '''
  def __init__(self, rank):
    self.deck       = pygame.image.load(os.path.join(PICS, "deck.png"))
    self.rank       = rank # количество палуб корабля
    self.list_decks = []   # список координат палуб корабля
    self.genDecks()        # генерируем палубы корабля
    
  def Draw(self, SCREEN, field):
    ''' отрисовка корабля '''
    for coord in self.list_decks:
      (gx, gy) = field.fromLocalToGlobal(coord[0], coord[1])
      SCREEN.blit(self.deck, (gx, gy, 40, 40))
      
  def genDecks(self):
    ''' генерация палуб корабля '''
    while True:
      initx, inity = (random.randint(0, 9), random.randint(0, 9))       # координаты начальной палубы
      self.list_decks.append((initx, inity))                            # добавляем начальную палубу в корабль
      direct = random.randint(0, 1)                                     # направление корабля от начальной палубы
      if initx + (self.rank - 1) < 10 and inity + (self.rank - 1) < 10: # если корабль помещается на поле
        if direct == 0:                                                 # если корабль смотрит вниз относительно начальной палубы
          for i in range(1, self.rank): self.list_decks.append((initx, inity + i)) # генерируем корабль вниз
        if direct == 1:                                                 # если корабль смотрит вправо относительно начальной палубы
          for i in range(1, self.rank): self.list_decks.append((initx + i, inity)) # генерируем корабль вправо
        break
      else: self.list_decks = []                                        # если не получилось сгенерировать корабль, то начнем заново  
      
class Field(pygame.Surface):
  ''' базовый класс игрового поля '''
  def __init__(self, center, size_field):
    ''' конструктор класса '''
    pygame.Surface.__init__(self, (size_field, size_field))
    self.SIZE_CELL     = 40              # ширина и высота квадратной клетки (в пикселах)
    self.GAP_CELL      = 2               # зазор между соседними клетками (в пикселах)
    self.NUM_CELLS     = 10              # количество клеток по горизонтали или вертикали
    self.WIDTH_BORDER  = 5               # ширина рамки игрового поля
    self.HEIGHT_BORDER = 5               # высота рамки игрового поля
    self.rect          = self.get_rect() # прямоугольник поверхности игрового поля
    self.rect.center   = center          # центр поверхности игрового поля
    self.ships         = []              # список всех кораблей игрового поля
    self.genShips()                      # генерация кораблей

  def Draw(self, SCREEN):
    ''' отрисовка игрового поля '''
    pygame.gfxdraw.box(SCREEN, (self.rect.x, self.rect.y, self.rect.width, self.rect.height), BLACK)
    pygame.gfxdraw.box(SCREEN, (self.rect.x + self.WIDTH_BORDER, self.rect.y + self.HEIGHT_BORDER, self.rect.width - 2 * self.WIDTH_BORDER, self.rect.height - 2 * self.HEIGHT_BORDER), WHITE)
    
    for i in range(1, self.NUM_CELLS):
      x = self.rect.x + self.WIDTH_BORDER + i * self.SIZE_CELL + (i - 1) * self.GAP_CELL 
      pygame.gfxdraw.box(SCREEN, (x, self.rect.y + self.WIDTH_BORDER, self.GAP_CELL, self.rect.width - 2 * self.WIDTH_BORDER), BLACK)
      y = self.rect.y + self.WIDTH_BORDER + i * self.SIZE_CELL + (i - 1) * self.GAP_CELL 
      pygame.gfxdraw.box(SCREEN, (self.rect.x + self.WIDTH_BORDER, y, self.rect.width - 2 * self.WIDTH_BORDER, self.GAP_CELL), BLACK)
      
  def Distance(self, ship1, ship2):
    ''' расстояние между двумя кораблями '''
    dist = 18
    for i in range(0, len(ship1.list_decks)):
      for j in range(0, len(ship2.list_decks)):
        newdist = abs(ship2.list_decks[j][0] - ship1.list_decks[i][0]) + abs(ship2.list_decks[j][1] - ship1.list_decks[i][1])
        if newdist < dist: dist = newdist
    return dist
    
  def genShips(self):
    ''' генерация всех кораблей '''
    self.ships.append(Ship(4))
    for rank in range(3, 0, -1):
      counter = 5 - rank
      while counter != 0:
        newship = Ship(rank)
        iscorrect = True
        for ship in self.ships:
          if self.Distance(newship, ship) < 3:
            del(newship)
            iscorrect = False
            break
        if iscorrect:
          self.ships.append(newship)  
          counter -= 1

class MyField(Field):
  ''' класс нашего поля '''
  def __init__(self, center, size_field):
    super().__init__(center, size_field)
    
  def fromGlobalToLocal(self, gx, gy):
    ''' преобразование из глобальных координат в локальные '''
    lx = int((gx - 56)/42)
    ly = int((gy - 41)/42)
    return (lx, ly)
  
  def fromLocalToGlobal(self, lx, ly):
    ''' преобразование локальных координат в глобальные '''
    gx = lx * 42 + 56
    gy = ly * 42 + 41
    return (gx, gy)
  
class EnemyField(Field):
  ''' класс вражеского поля '''
  def __init__(self, center, size_field):
    super().__init__(center, size_field)
    
  def fromGlobalToLocal(self, gx, gy):
    ''' преобразование из глобальных координат в локальные '''
    lx = int((gx - 541)/42)
    ly = int((gy - 41)/42)
    return (lx, ly)
  
  def fromLocalToGlobal(self, lx, ly):
    ''' преобразование локальных координат в глобальные '''
    gx = lx * 42 + 541
    gy = ly * 42 + 41
    return (gx, gy)
    
class Connect():
  def __init__(self, server = SERVERHOST, port = SERVERPORT):
    self.sockobj = socket(AF_INET, SOCK_STREAM) # создаём сокет
    self.sockobj.bind((SERVERHOST, SERVERPORT)) # привязываем сокет к ip:port
    self.sockobj.listen(3)                      # задаем ограничение на количество входящих соединений
    self.connection = None                      # идентификатор соединения
    self.address    = None                      # адрес визави
    
  def WaitConnect(self):
    ''' функция ожидания соединения '''
    self.connection, self.address = self.sockobj.accept()
    print("Соединение установлено с машиной ", self.address[0])
