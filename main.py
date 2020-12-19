import random

import pygame

WIDTH, HEIGHT = 750, 860
ROW, COLUMN = 4, 10
SHOT_DELAY = 800


class Colors:
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    BLACK = (0, 0, 0)
    FONT_COLOR = (164, 239, 255)


class Ship(pygame.sprite.Sprite):
    SHIP_SPEED = 10
    SHIP_SIZE = [50, 22]
    SHIP_X = WIDTH / 2
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


class Game:
    score = 0
    shot_time = 0

    def __init__(self):
        self.ship = Ship()
        self.enemy_list = pygame.sprite.Group()
        self.missile_list = pygame.sprite.Group()
        self.bomb_list = pygame.sprite.Group()
        self.create_enemies()
        self.play()

    def create_enemies(self):
        for row in range(1, ROW // 2 + 1):
            for column in range(1, COLUMN + 1):
                enemy_green = GreenEnemy()
                enemy_green.rect.x = 80 + (50 * column)
                enemy_green.rect.y = 25 + (50 * row)
                self.enemy_list.add(enemy_green)

                enemy_pink = PinkEnemy()
                enemy_pink.rect.x = 80 + (50 * column)
                enemy_pink.rect.y = 125 + (50 * row)
                self.enemy_list.add(enemy_pink)

    def redraw(self):
        background_img = pygame.image.load('icons/backgroundv2.png')
        window.blit(background_img, [0, 0])

        font = pygame.font.Font('Fonts/Caudex-Bold.ttf', 30)
        text_score = font.render("SCORE: {}".format(str(self.score)), False, Colors.FONT_COLOR)
        text_rect = text_score.get_rect()
        text_rect.center = (WIDTH // 4, 25)
        window.blit(text_score, text_rect)

        text_lives = font.render("LIVES: {}".format(str(self.ship.live)), False, Colors.FONT_COLOR)
        text_rect = text_lives.get_rect()
        text_rect.center = (WIDTH // 4 * 3, 25)
        window.blit(text_lives, text_rect)

        self.ship.draw()

        self.enemy_list.update()
        self.enemy_list.draw(window)

        self.missile_list.update()
        self.missile_list.draw(window)

        self.bomb_list.update()
        self.bomb_list.draw(window)

        pygame.display.update()

    def play(self):
        run = True
        while run:
            pygame.time.delay(50)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            self.move()
            self.enemy_shot()

            for missile in self.missile_list:
                self.check_out_of_bounds(missile)
                self.check_hit_enemy(missile)

            for bomb in self.bomb_list:
                if bomb.rect.y > HEIGHT+Missile.MISSILE_SIZE[1]:
                    self.bomb_list.remove(bomb)

                self.check_hit_ship(bomb)

            run = self.check_end_condition()

            self.redraw()

    def move(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            if self.ship.rect.x > 0:
                self.ship.rect.x += -self.ship.SHIP_SPEED

        if key[pygame.K_RIGHT]:
            if self.ship.rect.x < 700:
                self.ship.rect.x += self.ship.SHIP_SPEED

        if key[pygame.K_SPACE]:
            press_space_time = pygame.time.get_ticks()
            time_delta = press_space_time - self.shot_time
            if time_delta > SHOT_DELAY:
                missile = ShipMissile()
                missile.rect.x = self.ship.rect.x + 25
                missile.rect.y = self.ship.rect.y
                self.missile_list.add(missile)

                self.shot_time = pygame.time.get_ticks()

    def enemy_shot(self):
        shoot_chance = random.randint(1, 100)
        if shoot_chance < 10:
            if len(self.enemy_list) > 0:
                random_enemy = random.choice(self.enemy_list.sprites())
                bomb = EnemyMissile()
                bomb.rect.x = random_enemy.rect.x + 20
                bomb.rect.y = random_enemy.rect.y + 40
                self.bomb_list.add(bomb)

    def check_hit_enemy(self, missile):
        for enemy in self.enemy_list:
            if missile.rect.colliderect(enemy.rect):
                self.score += enemy.points
                self.missile_list.remove(missile)
                self.enemy_list.remove(enemy)

    def check_out_of_bounds(self, missile):
        if missile.rect.y < -10:
            self.missile_list.remove(missile)

    def check_hit_ship(self, bomb):
        if bomb.rect.colliderect(self.ship.rect):
            self.bomb_list.remove(bomb)
            self.ship.live -= 1

    def check_end_condition(self):
        if self.ship.live <= 0 or len(self.enemy_list) == 0:
            import tkinter
            from tkinter import messagebox

            root = tkinter.Tk()
            root.title("Message Box")

            response = messagebox.showinfo("Game over", "You won!\nYour score:{}".format(self.score), )
            tkinter.Label(root, text=response).pack()
            # if response == 1:
            #     Label(root,text='You clicked yes').pack()
            # else:

            root.mainloop()
            # run = False
            return False
        return True


if __name__ == '__main__':
    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Space Invaders')
    programIcon = pygame.image.load('icons/green_alien.png')
    pygame.display.set_icon(programIcon)
    Game()
    pygame.quit()
