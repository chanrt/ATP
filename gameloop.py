from math import sqrt
import pygame as pg

from constants import consts as c
from enemy import Enemy
from player import Player
from utils import *


def game_loop():
    player = Player()
    enemies = [Enemy(200, 200, "plankton")]
    sugar_molecules = []
    c.set_player(player)

    running = True

    while running:
        clock.tick(c.fps)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False

        keys_pressed = pg.key.get_pressed()
        cursor_states = {
            "up": keys_pressed[pg.K_UP] or keys_pressed[pg.K_w],
            "right": keys_pressed[pg.K_RIGHT] or keys_pressed[pg.K_d],
            "down": keys_pressed[pg.K_DOWN] or keys_pressed[pg.K_s],
            "left": keys_pressed[pg.K_LEFT] or keys_pressed[pg.K_a],
        }
        player.move(cursor_states)

        player.update()
        for enemy in enemies:
            enemy.update()

        enemy_collisions = check_collisions(player, enemies)
        for index, collision in enumerate(enemy_collisions):
            if collision:
                if enemies[index].health < player.health:
                    sugar_molecules += sugar_spawner(enemies[index])
                    enemies[index].is_alive = False

        sugar_collisions = check_collisions(player, sugar_molecules)
        for index, collision in enumerate(sugar_collisions):
            if collision:
                player.sugar += 1
                sugar_molecules[index].picked_up = True

        enemies = [enemy for enemy in enemies if enemy.is_alive]
        sugar_molecules = [sugar for sugar in sugar_molecules if not sugar.picked_up]

        c.screen.fill(c.bg_color)

        player.render()
        for sugar in sugar_molecules:
            sugar.render()
        for enemy in enemies:
            enemy.render()

        pg.display.flip()

        c.update_dt()


if __name__ == '__main__':
    pg.init()
    screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
    clock = pg.time.Clock()
    c.set_screen(screen)
    c.set_clock(clock)
    game_loop()