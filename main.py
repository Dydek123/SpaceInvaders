import random

import pygame

pygame.init()

window = pygame.display.set_mode((750, 860))

pygame.display.set_caption('Space Invaders')

white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
black = (0, 0, 0)

SHIP_SPEED = 10
SHIP_X = 325
SHIP_Y = 800
SHIP_LIVES = 3

MISSILE_SPEED = 10


class Ship(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([50, 22])
        self.image.fill(green)  # self.image = pygame.image.load('icons/ship.png')
        self.rect = self.image.get_rect()
        self.live = SHIP_LIVES

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Enemy(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([40, 40])
        self.image.fill(white)
        self.rect = self.image.get_rect()
        self.group_rect = pygame.Rect(130,75,500,250)
        self.direction = 5

    def update(self):
        self.rect.x += self.direction
        self.group_rect.x += self.direction
        if self.group_rect.x + 500 >= 750 or self.group_rect.x < 25:
            self.direction = -self.direction
            self.rect.y += 5


class Missile(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([5, 10])
        self.image.fill(green)
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.y += -MISSILE_SPEED


class Bomb(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([5, 10])
        self.image.fill(red)
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.y += MISSILE_SPEED


ship = Ship()

ship.rect.x = SHIP_X
ship.rect.y = SHIP_Y

enemy_list = pygame.sprite.Group()
missile_list = pygame.sprite.Group()
bomb_list = pygame.sprite.Group()

for row in range(1, 6):

    for column in range(1, 11):
        enemy = Enemy()

        enemy.rect.x = 80 + (50 * column)

        enemy.rect.y = 25 + (50 * row)

        enemy_list.add(enemy)


def redraw():
    window.fill(black)

    font = pygame.font.SysFont('Time New Roman', 30)
    text = font.render('Space Invaders', False, white)
    textRect= text.get_rect()
    textRect.center = (750//2, 25)
    window.blit(text, textRect)

    ship.draw()

    enemy_list.update()
    enemy_list.draw(window)

    missile_list.update()
    missile_list.draw(window)

    bomb_list.update()
    bomb_list.draw(window)

    pygame.display.update()


run = True

while run:

    pygame.time.delay(100)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False

    key = pygame.key.get_pressed()

    if key[pygame.K_LEFT]:
        ship.rect.x += -SHIP_SPEED

    if key[pygame.K_RIGHT]:
        ship.rect.x += SHIP_SPEED

    if key[pygame.K_SPACE]:
        if len(missile_list) < 10:
            missile = Missile()
            missile.rect.x = ship.rect.x + 25
            missile.rect.y = ship.rect.y
            missile_list.add(missile)

    shoot_chance = random.randint(1, 100)
    if shoot_chance < 10:
        if len(enemy_list) > 0:
            random_enemy = random.choice(enemy_list.sprites())
            bomb = Bomb()
            bomb.rect.x = random_enemy.rect.x + 20
            bomb.rect.y = random_enemy.rect.y + 40
            bomb_list.add(bomb)

    for missile in missile_list:
        if missile.rect.y < -10:
            missile_list.remove(missile)

        for enemy in enemy_list:
            if missile.rect.colliderect(enemy.rect):
                missile_list.remove(missile)
                enemy_list.remove(enemy)

    for bomb in bomb_list:
        if bomb.rect.y > 880:
            bomb_list.remove(bomb)

        if bomb.rect.colliderect(ship.rect):
            bomb_list.remove(bomb)
            ship.live -= 1
            # print(ship.live)

    if ship.live <= 0 or len(enemy_list) == 0:
        run = False

    redraw()

pygame.quit()
