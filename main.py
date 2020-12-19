import random

import pygame

WIDTH, HEIGHT = 750, 860
SHOT_DELAY = 800
SHOT_TIME = 0
SCORE = 0


class Colors:
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    BLACK = (0, 0, 0)
    FONT_COLOR = (164, 239, 255)


class Ship(pygame.sprite.Sprite):
    SHIP_SPEED = 10
    SHIP_SIZE = [50, 22]
    SHIP_X = 325
    SHIP_Y = 800
    SHIP_LIVES = 3

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(self.SHIP_SIZE)
        self.image = pygame.image.load('icons/ship.png')
        self.rect = self.image.get_rect()
        self.live = self.SHIP_LIVES
        self.rect.x = self.SHIP_X
        self.rect.y = self.SHIP_Y

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Enemy(pygame.sprite.Sprite):
    ENEMY_SIZE = [40, 40]
    ENEMY_X_SPEED = 5
    ENEMY_Y_SPEED = 10

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(self.ENEMY_SIZE)
        self.rect = self.image.get_rect()
        self.group_rect = pygame.Rect(130, 75, 500, 250)
        self.direction = self.ENEMY_X_SPEED

    def update(self):
        self.rect.x += self.direction
        self.group_rect.x += self.direction
        if self.group_rect.x + 500 >= WIDTH or self.group_rect.x < 25:
            self.direction = -self.direction
            self.rect.y += self.ENEMY_Y_SPEED


class GreenEnemy(Enemy):
    GREEN_ENEMY_POINTS = 20

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('icons/green_alien.png')
        self.points = self.GREEN_ENEMY_POINTS


class PinkEnemy(Enemy):
    PINK_ENEMY_POINTS = 10

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('icons/pink_alien.png')
        self.points = self.PINK_ENEMY_POINTS


class Missile(pygame.sprite.Sprite):
    MISSILE_SIZE = [5, 10]
    MISSILE_SPEED = 10

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(self.MISSILE_SIZE)
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.y += -self.MISSILE_SPEED


class ShipMissile(Missile):
    def __init__(self):
        super().__init__()
        self.image.fill(Colors.GREEN)


class EnemyMissile(Missile):
    def __init__(self):
        super().__init__()
        self.MISSILE_SPEED = -self.MISSILE_SPEED
        self.image.fill(Colors.RED)

def redraw():
    # window.fill(black)
    window.blit(background_img, [0, 0])

    font = pygame.font.Font('Fonts/Caudex-Bold.ttf', 30)
    text_score = font.render("SCORE: {}".format(str(SCORE)), False, Colors.FONT_COLOR)
    text_rect = text_score.get_rect()
    text_rect.center = (WIDTH // 4, 25)
    window.blit(text_score, text_rect)

    text_lives = font.render("LIVES: {}".format(str(ship.live)), False, Colors.FONT_COLOR)
    text_rect = text_lives.get_rect()
    text_rect.center = (WIDTH // 4 * 3, 25)
    window.blit(text_lives, text_rect)

    ship.draw()

    enemy_list.update()
    enemy_list.draw(window)

    missile_list.update()
    missile_list.draw(window)

    bomb_list.update()
    bomb_list.draw(window)

    pygame.display.update()

ship = Ship()

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
        print(enemy_list)

pygame.init()

window = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('Space Invaders')

programIcon = pygame.image.load('icons/green_alien.png')
pygame.display.set_icon(programIcon)

background_img = pygame.image.load('icons/backgroundv2.png')

run = True

while run:

    pygame.time.delay(50)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False

    key = pygame.key.get_pressed()

    if key[pygame.K_LEFT]:
        if ship.rect.x > 0:
            ship.rect.x += -ship.SHIP_SPEED

    if key[pygame.K_RIGHT]:
        if ship.rect.x < 700:
            ship.rect.x += ship.SHIP_SPEED

    if key[pygame.K_SPACE]:
        press_space_time = pygame.time.get_ticks()
        time_delta = press_space_time - SHOT_TIME
        if time_delta > SHOT_DELAY:
            missile = ShipMissile()
            missile.rect.x = ship.rect.x + 25
            missile.rect.y = ship.rect.y
            missile_list.add(missile)

            SHOT_TIME = pygame.time.get_ticks()

    shoot_chance = random.randint(1, 100)
    if shoot_chance < 10:
        if len(enemy_list) > 0:
            random_enemy = random.choice(enemy_list.sprites())
            bomb = EnemyMissile()
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
        from tkinter import *
        from tkinter import messagebox

        root = Tk()
        root.title("Message Box")


        def popup():
            response = messagebox.showinfo("Game over", "You won!\nYour score:{}".format(SCORE), )
            Label(root, text=response).pack()
            # if response == 1:
            #     Label(root,text='You clicked yes').pack()
            # else:
            #     Label(root, text='You clicked no').pack()


        popup()

        root.mainloop()
        run = False

    redraw()

pygame.quit()
