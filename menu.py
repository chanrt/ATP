from os import path
from random import shuffle
import pygame as pg

from button import Button
from constants import consts as c
from gameloop import game_loop
from text import Text


def menu():
    tips = [
        "Use plasma membrane upgrades to increase health",
        "Keep an eye on your membrane health, sugar and ATP",
        "Antibodies allow you to kill enemies without taking damage",
        "Cytokine storms are effective if there are many enemies around",
        "Use anabolism upgrades to increase your healing",
        "Photosynthesis allows you to play passively"
    ] 
    shuffle(tips)
    tips = ["Mitochondria is the powerhouse of the cell"] + tips
    current_tip = 0

    title_text = Text(c.s_width // 2, c.s_height // 5, "ATP", c.screen)
    title_text.set_font(pg.font.Font(path.join(path.dirname(__file__), "assets", "orbitron.ttf"), c.title_font_size))

    play_button = Button(3 * c.s_width // 4, c.s_height // 2, c.s_width // 5, 40, c.screen, "Play")
    play_button.set_font(pg.font.Font(path.join(path.dirname(__file__), "assets", "orbitron.ttf"), c.stats_font_size))

    tip_text = Text(c.s_width // 2, 4 * c.s_height // 5, f"Tip: {tips[current_tip]}", c.screen)
    tip_text.set_font(pg.font.Font(path.join(path.dirname(__file__), "assets", "orbitron.ttf"), c.stats_font_size))

    controls = Text(c.s_width // 4, c.s_height // 2, "Controls \n \
        WASD: movement \n \
        Esc: quit \n \
        Q: sugar -> ATP \n \
        E: sugar -> membrance \n \
        SPACE: all sugar -> ATP until upgrade \n \
        Left click: shoot antibody \n \
        Right click: release cytokine storm", c.screen)
    controls.set_font(pg.font.Font(path.join(path.dirname(__file__), "assets", "orbitron.ttf"), c.stats_font_size))

    next_tip = pg.USEREVENT + 1
    pg.time.set_timer(next_tip, 3000)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return 0

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    return 0
                
            if event.type == next_tip:
                current_tip += 1
                if current_tip == len(tips):
                    current_tip = 0
                tip_text.set_text(f"Tip: {tips[current_tip]}")
                
            if event.type == pg.MOUSEBUTTONDOWN:
                play_button.check_clicked(pg.mouse.get_pos(), event.button)
                if play_button.left_clicked:
                    return 1

        c.screen.fill(c.black)

        play_button.update(pg.mouse.get_pos())

        title_text.render()
        controls.render()
        play_button.render()
        tip_text.render()

        pg.display.flip()


if __name__ == '__main__':
    pg.init()
    screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
    clock = pg.time.Clock()
    c.set_screen(screen)
    c.set_clock(clock)

    status = menu()
    if status:
        game_loop()