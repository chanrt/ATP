import pygame as pg

from constants import consts as c
from player import Player


def game_loop():
    player = Player()

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

        c.screen.fill(c.bg_color)

        player.render()

        pg.display.flip()

        c.update_dt()


if __name__ == '__main__':
    pg.init()
    screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
    clock = pg.time.Clock()
    c.set_screen(screen)
    c.set_clock(clock)
    game_loop()