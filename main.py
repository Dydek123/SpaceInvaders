import random

import pygame

pygame.init()

window = pygame.display.set_mode((750, 860))

pygame.display.set_caption('Space Invaders')

programIcon = pygame.image.load('icons/green_alien.png')
pygame.display.set_icon(programIcon)

background_img = pygame.image.load('icons/backgroundv2.png')

white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
black = (0, 0, 0)

SHIP_SPEED = 10
SHIP_SIZE = [50, 22]
SHIP_X = 325
SHIP_Y = 800
SHIP_LIVES = 3

ENEMY_SIZE = [40, 40]
ENEMY_X_SPEED = 5
ENEMY_Y_SPEED = 5
GREEN_ENEMY_POINTS = 10
PINK_ENEMY_POINTS = 20

MISSILE_SIZE = [5, 10]
MISSILE_SPEED = 10
SHOT_DELAY = 800
shot_time = 0

SCORE = 0

class Ship(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(SHIP_SIZE)
        # self.image.fill(green)
        self.image = pygame.image.load('icons/ship.png')
        self.rect = self.image.get_rect()
        self.live = SHIP_LIVES

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class GreenEnemy(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(ENEMY_SIZE)
        # self.image.fill(white)
        self.image = pygame.image.load('icons/green_alien.png')
        self.rect = self.image.get_rect()
        self.group_rect = pygame.Rect(130, 75, 500, 250)
        self.direction = ENEMY_X_SPEED
        self.points = GREEN_ENEMY_POINTS

    def update(self):
        self.rect.x += self.direction
        self.group_rect.x += self.direction
        if self.group_rect.x + 500 >= 750 or self.group_rect.x < 25:
            self.direction = -self.direction
            self.rect.y += ENEMY_Y_SPEED


class PinkEnemy(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(ENEMY_SIZE)
        # self.image.fill(white)
        self.image = pygame.image.load('icons/pink_alien.png')
        self.rect = self.image.get_rect()
        self.group_rect = pygame.Rect(130, 75, 500, 250)
        self.direction = ENEMY_X_SPEED
        self.points = PINK_ENEMY_POINTS

    def update(self):
        self.rect.x += self.direction
        self.group_rect.x += self.direction
        if self.group_rect.x + 500 >= 750 or self.group_rect.x < 25:
            self.direction = -self.direction
            self.rect.y += ENEMY_Y_SPEED


class Missile(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(MISSILE_SIZE)
        self.image.fill(green)
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.y += -MISSILE_SPEED


class Bomb(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(MISSILE_SIZE)
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

for row in range(1, 3):

    for column in range(1, 11):
        enemy_green = GreenEnemy()
        enemy_green.rect.x = 80 + (50 * column)
        enemy_green.rect.y = 25 + (50 * row)
        enemy_list.add(enemy_green)

        enemy_pink = PinkEnemy()
        enemy_pink.rect.x = 80 + (50 * column)
        enemy_pink.rect.y = 125 + (50 * row)
        enemy_list.add(enemy_pink)


def redraw():
    # window.fill(black)
    window.blit(background_img, [0, 0])

    font = pygame.font.SysFont('Time New Roman', 30)
    text_score = font.render("SCORE: {}".format(str(SCORE)), False, white)
    textRect = text_score.get_rect()
    textRect.center = (750 // 4, 25)
    window.blit(text_score, textRect)

    text_lives = font.render("LIVES: {}".format(str(ship.live)), False, white)
    textRect = text_lives.get_rect()
    textRect.center = (750 // 4 * 3, 25)
    window.blit(text_lives, textRect)

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
        if ship.rect.x > 0:
            ship.rect.x += -SHIP_SPEED

    if key[pygame.K_RIGHT]:
        if ship.rect.x < 700:
            ship.rect.x += SHIP_SPEED

    if key[pygame.K_SPACE]:
        press_space_time = pygame.time.get_ticks()
        time_delta = press_space_time - shot_time
        if time_delta > SHOT_DELAY:
            missile = Missile()
            missile.rect.x = ship.rect.x + 25
            missile.rect.y = ship.rect.y
            missile_list.add(missile)

            shot_time = pygame.time.get_ticks()

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
                SCORE += enemy.points
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
