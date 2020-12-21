import random
from abc import abstractmethod

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


class SpaceObject(pygame.sprite.Sprite):

    @abstractmethod
    def shot(self):
        pass


class Ship(SpaceObject):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.size = [50, 22]
        self.image = pygame.Surface(self.size)
        self.image = pygame.image.load('icons/ship.png')
        self.rect = self.image.get_rect()
        self.speed = 10
        self.live = 3
        self.rect.x = WIDTH/2
        self.rect.y = HEIGHT - 60
        self.shot_time = 0

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def move(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            if self.rect.x > 0:
                self.rect.x += -self.speed

        if key[pygame.K_RIGHT]:
            if self.rect.x < WIDTH - self.size[0]:
                self.rect.x += self.speed

    def shot(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            press_space_time = pygame.time.get_ticks()
            time_delta = press_space_time - self.shot_time
            if time_delta > SHOT_DELAY:
                missile = ShipMissile()
                missile.rect.x = self.rect.x + self.size[0]/2
                missile.rect.y = self.rect.y
                # self.missile_list.add(missile)
                self.shot_time = pygame.time.get_ticks()
                return missile
        return None


class Enemy(SpaceObject):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.size = [40,40]
        self.image = pygame.Surface(self.size)
        self.rect = self.image.get_rect()
        self.group_rect = pygame.Rect(130, 75, 500, 250)
        self.x_speed = 5
        self.y_speed = 10

    def update(self):
        self.rect.x += self.x_speed
        self.group_rect.x += self.x_speed
        if self.group_rect.x + 500 >= WIDTH or self.group_rect.x < 25:
            self.x_speed = -self.x_speed
            self.rect.y += self.y_speed

    def shot(self):
        shoot_chance = random.randint(1, 100)
        if shoot_chance < 10:
            bomb = EnemyMissile()
            bomb.rect.x = self.rect.x + self.size[0]/2
            bomb.rect.y = self.rect.y + self.size[1]/2
            # self.bomb_list.add(bomb)
            return bomb
        return None

    # def collide(self, missile):
    #     return missile.rect.colliderect(self.rect)


class GreenEnemy(Enemy):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('icons/green_alien.png')
        self.points = 20


class PinkEnemy(Enemy):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('icons/pink_alien.png')
        self.points = 10


class Missile(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.size = [5, 10]
        self.image = pygame.Surface(self.size)
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.y += -self.speed

    @abstractmethod
    def out_of_bounds(self):
        pass

    def collide(self, space_object):
        return self.rect.colliderect(space_object.rect)


class ShipMissile(Missile):
    def __init__(self):
        super().__init__()
        self.image.fill(Colors.GREEN)

    def out_of_bounds(self):
        return self.rect.y < -self.size[1]


class EnemyMissile(Missile):
    def __init__(self):
        super().__init__()
        self.speed = -self.speed
        self.image.fill(Colors.RED)

    def out_of_bounds(self):
        return self.rect.y > HEIGHT + self.size[1]


class Game:
    def __init__(self):
        self.score = 0
        self.ship = Ship()
        self.enemy_list = pygame.sprite.Group()
        self.missile_list = pygame.sprite.Group()
        self.bomb_list = pygame.sprite.Group()
        self.create_enemies()

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
            pygame.time.delay(10)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        return

            self.ship.move()

            random_enemy = random.choice(self.enemy_list.sprites())
            bomb = random_enemy.shot()
            if bomb:
                self.bomb_list.add(bomb)

            missile = self.ship.shot()
            if missile:
                self.missile_list.add(missile)

            for missile in self.missile_list:
                if missile.out_of_bounds():
                    self.missile_list.remove(missile)

                for enemy in self.enemy_list:
                    if missile.collide(enemy):
                        self.score += enemy.points
                        self.missile_list.remove(missile)
                        self.enemy_list.remove(enemy)
                # self.check_hit_enemy(missile)

            for bombs in self.bomb_list:
                if bombs.out_of_bounds():
                    self.bomb_list.remove(bombs)

                # if self.ship.collide(bombs):
                if bombs.collide(self.ship):
                    self.ship.live -= 1
                    self.bomb_list.remove(bombs)

            run = self.check_end_condition()

            self.redraw()

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
    game = Game()
    game.play()
    pygame.quit()
