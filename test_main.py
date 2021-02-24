import unittest
import pyautogui

import main
import pygame


class TestShip(unittest.TestCase):
    def setUp(self):
        self.ship = main.Ship()

    def test_move(self):
        tmp_pos = self.ship.rect.x
        pygame.init()
        key_list = [0 for val in range (0, 323)]

        #Move in left direction
        pygame.key.set_mods(pygame.K_LEFT)

        self.assertEqual(pygame.key.get_mods(), pygame.K_LEFT)
        key_list[pygame.key.get_mods()] = 1
        self.ship.move(key_list)
        self.assertEqual(self.ship.rect.x, tmp_pos-self.ship.speed)

        #Reset key
        key_list[pygame.key.get_mods()] = 0

        #Move in right direction
        pygame.key.set_mods(pygame.K_RIGHT)
        key_list[pygame.key.get_mods()] = 1
        self.ship.move(key_list)
        #Move in sequence: move left, move right means no displacement
        self.assertEqual(self.ship.rect.x, tmp_pos)

        pygame.quit()


class TestEnemy(unittest.TestCase):
    def setUp(self):
        self.enemy_green = main.GreenEnemy()
        self.enemy_green.rect.x = 100
        self.enemy_green.rect.y = 100

    def test_update(self):
        self.enemy_green.update()
        self.assertEqual(self.enemy_green.rect.x, 100+self.enemy_green.x_speed)

    def test_shot(self):
        bomb = main.EnemyMissile()
        bomb.rect.x = self.enemy_green.rect.x + self.enemy_green.size[0] / 2
        bomb.rect.y = self.enemy_green.rect.y + self.enemy_green.size[1]

        while True:
            generated_bomb = self.enemy_green.shot()
            if generated_bomb:
                self.assertEqual(generated_bomb.rect.x, bomb.rect.x)
                self.assertEqual(generated_bomb.rect.y, bomb.rect.y)
                break

class TestShipMissile(unittest.TestCase):
    def setUp(self):
        self.missile = main.ShipMissile()

    def test_out_of_bounds(self):
        self.missile.rect.y = 0
        self.assertEqual(self.missile.out_of_bounds(), False)
        self.missile.update()
        self.assertEqual(self.missile.out_of_bounds(), True)

    def test_update(self):
        tmp_pos = 100
        self.missile.rect.y = tmp_pos
        self.missile.update()
        self.assertEqual(self.missile.rect.y, tmp_pos-self.missile.speed)

    def test_collide(self):
        enemy_green = main.GreenEnemy()
        enemy_green.rect.x = 10
        enemy_green.rect.y = 10
        x_pos = 20
        y_pos = 30

        self.missile.rect.x = x_pos
        self.missile.rect.y = y_pos
        self.assertEqual(self.missile.collide(enemy_green), True)

        self.missile.rect.x = 100
        self.missile.rect.y = 100
        self.assertEqual(self.missile.collide(enemy_green), False)


class TestEnemyMissile(unittest.TestCase):
    def setUp(self):
        self.missile = main.EnemyMissile()

    def test_out_of_bounds(self):
        self.missile.rect.y = main.HEIGHT
        self.assertEqual(self.missile.out_of_bounds(), False)
        self.missile.update()
        self.assertEqual(self.missile.out_of_bounds(), True)

    def test_update(self):
        tmp_pos = 100
        self.missile.rect.y = tmp_pos
        self.missile.update()
        self.assertEqual(self.missile.rect.y, tmp_pos-self.missile.speed)

    def test_collide(self):
        ship = main.Ship()

        self.missile.rect.x = ship.rect.x
        self.missile.rect.y = ship.rect.y - self.missile.size[1]
        self.assertEqual(self.missile.collide(ship), False)

        self.missile.rect.y += 1
        self.assertEqual(self.missile.collide(ship), True)

        self.missile.rect.x = ship.rect.x - self.missile.size[0]
        self.missile.rect.y = ship.rect.y
        self.assertEqual(self.missile.collide(ship), False)

        self.missile.rect.x += 1
        self.assertEqual(self.missile.collide(ship), True)

class TesstGame(unittest.TestCase):
    def setUp(self):
        self.game = main.Game()

    def test_create_enemies(self):
        #Method create_enemies called in constructor
        self.assertEqual(len(self.game.enemy_list), 40)