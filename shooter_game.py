#Создай собственный Шутер!
# from pygame import *

# class GameSprite(sprite.Sprite):
#     def __init__(self, player_image, player_x, player_y, player_speed):
#         sprite.Sprite.__init__(self)
#         self.image = transform.scale(image.load(player_image), (65, 65))
#         self.speed = player_speed
#         self.rect = self.image.get_rect()
#         self.rect.x = player_x
#         self.rect.y = player_y
# def reset(self):
#     window.blit(self.image, (self.rect.x, self.rect.y))

# class Asteroid(GameSprite):
#     def update(self):
#         if self.rect.x <= 470:
#             self.direction = 'right'
#         if self.rect.x >= win_width - 85:
#             self.direction = 'left'
#         if self.direction == 'left':
#             self.rect.x -= self.speed
#         else:
#             self.rect.x += self.speed

# class Rocket(GameSprite):
#     def update(self):
#         keys = key.get_pressed()
#         if keys[K_LEFT] and self.rect.x > 5:
#             self.rect.x -= self.speed
#         if keys[K_RIGHT] and self.rect.x < win_width - 80:
#             self.rect.x += self.speed
#         if keys[K_UP] and self.rect.y > 5:
#             self.rect.y -= self.speed
#         if keys[K_DOWN] and self.rect.y < win_height - 80:
#             self.rect.y += self.speed    
    
# win_width = 700
# win_height = 500
# rocket = Rocket('rocket.png', 5, win_height - 80, 4)
# asteroid = Asteroid('asteroid.png', win_width - 80, 280, 2)
# window = display.set_mode((win_width, win_height))
# display.set_caption('Самый лучший шутер!')
# background = transform.scale(image.load('galaxy.jpg'), ((700, 500)))

# mixer.init()
# mixer.music.load('space.ogg')
# mixer.music.play()
# fire_sound = mixer.Sound('fire.ogg')
# img_back = 'galaxy.jpg'
# img_hero = 'rocket.png'

# #ship = Rocket(img_hero, 5, win_height - 100, 80, 100, 10)
# finish = False
# run = True
# while run:
#     for e in event.get():
#         if e.type == QUIT:
#             run = False
#     if not finish:
#         window.blit(background, (0,0))
#         rocket.update()
#         rocket.reset()
#         display.update()
#     time.delay(50)


from pygame import *
from random import randint

#фоновая музыка

#шрифты и надписи
font.init()
font2 = font.Font(None, 36)

# нам нужны такие картинки:
img_back = "galaxy.jpg" # фон игры
img_hero = "rocket.png" # герой
img_enemy = "ufo.png" # враг

score = 0 # сбито кораблей
lost = 0 # пропущено кораблей

# класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
  # конструктор класса
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # Вызываем конструктор класса (Sprite):
        sprite.Sprite.__init__(self)

        # каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 
  # метод, отрисовывающий героя на окне
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# класс главного игрока
class Player(GameSprite):
    # метод для управления спрайтом стрелками клавиатуры
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
  # метод "выстрел" (используем место игрока, чтобы создать там пулю)
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)
        

# класс спрайта-врага   
class Enemy(GameSprite):
    # движение врага
    def update(self):
        self.rect.y += self.speed
        global lost
        # исчезает, если дойдет до края экрана
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

win_font = pygame.font.SysFont('Times New Roman', 80)
# Создаем окошко
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

# создаем спрайты
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

bullets = sprite.Group()
# переменная "игра закончилась": как только там True, в основном цикле перестают работать спрайты
finish = False
# Основной цикл игры:
run = True # флаг сбрасывается кнопкой закрытия окна
while run:
    # событие нажатия на кнопку Закрыть
    for e in event.get():
        if e.type == QUIT:
            run = False

    if not finish:
        # обновляем фон
        window.blit(background,(0,0))

        # пишем текст на экране
        text = font2.render("Счет: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        # производим движения спрайтов
        ship.update()
        monsters.update()

        # обновляем их в новом местоположении при каждой итерации цикла
        ship.reset()
        monsters.draw(window)

        display.update()
    # цикл срабатывает каждую 0.05 секунд
    time.delay(50)