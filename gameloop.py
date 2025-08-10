from math import sqrt
from os import path
import pygame as pg

from antibody import Antibody
from constants import consts as c
from enemy import Enemy
from player import Player
from progress_bar import ProgressBar
from sounds import sounds
from storm import Storm
from text import Text
from utils import *


def game_loop():
    player = Player()
    c.set_player(player)
    
    antibodies = []
    enemies = []
    sugar_molecules = []
    storms = []

    for _ in range(50):
        enemy_x = 2 * c.s_width * (random() - 0.5)
        enemy_y = 2 * c.s_height * (random() - 0.5)

        if random() < 0:
            enemy_type = "euglena"
        else:
            enemy_type = "plankton"
        enemies.append(Enemy(enemy_x, enemy_y, enemy_type))

    health_text = Text(c.s_width // 4, c.stats_font_size // 2, f"Membrane", c.screen)
    health_text.set_font(pg.font.Font(path.join(path.dirname(__file__), "assets", "orbitron.ttf"), c.stats_font_size))

    atp_text = Text(3 * c.s_width // 4, c.stats_font_size // 2, f"ATP", c.screen)
    atp_text.set_font(pg.font.Font(path.join(path.dirname(__file__), "assets", "orbitron.ttf"), c.stats_font_size))

    sugar_text = Text(c.s_width // 2, c.s_height - c.stats_font_size, f"Sugar: {player.sugar}", c.screen)
    sugar_text.set_font(pg.font.Font(path.join(path.dirname(__file__), "assets", "orbitron.ttf"), c.stats_font_size))

    health_progress_bar = ProgressBar(c.s_width // 4, 2 * c.stats_font_size, c.s_width // 6, c.stats_font_size // 2, c.screen)
    atp_progress_bar = ProgressBar(3 * c.s_width // 4, 2 * c.stats_font_size, c.s_width // 6, c.stats_font_size // 2, c.screen)

    lightning_image = pg.image.load(path.join(path.dirname(__file__), "assets", "icons", "lightning_bolt.png"))
    lightning_image = pg.transform.scale(lightning_image, (100, 100))

    sounds.play_bg_music()
    running = True

    while running:
        clock.tick(c.fps)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
                if event.key == pg.K_q:
                    player.respire()
                if event.key == pg.K_e:
                    player.heal()
                if event.key == pg.K_SPACE:
                    player.exhaust_sugar()
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1 and c.antibody:
                    if player.atp < 1 and player.sugar > 0:
                        player.respire()

                    dx = event.pos[0] - c.s_width // 2
                    dy = c.s_height // 2 - event.pos[1]
                    distance = sqrt(dx * dx + dy * dy)
                    antibody = Antibody(player.x, player.y, dx / distance, dy / distance, "player")
                    antibodies.append(antibody)
                    player.atp -= 1
                    sounds.shoot.play()
                if event.button == 3 and c.storm:
                    if player.atp >= c.storm_cost:
                        player.atp -= c.storm_cost
                        new_storm = Storm(player.x, player.y)
                        storms.append(new_storm)
                        sounds.storm.play()

        keys_pressed = pg.key.get_pressed()
        cursor_states = {
            "up": keys_pressed[pg.K_UP] or keys_pressed[pg.K_w],
            "right": keys_pressed[pg.K_RIGHT] or keys_pressed[pg.K_d],
            "down": keys_pressed[pg.K_DOWN] or keys_pressed[pg.K_s],
            "left": keys_pressed[pg.K_LEFT] or keys_pressed[pg.K_a],
        }
        player.move(cursor_states)

        # update entities
        player.update(enemies)
        for antibody in antibodies:
            antibody.update()
        for sugar in sugar_molecules:
            sugar.update()
        for enemy in enemies:
            enemy.update()
        for storm in storms:
            storm.update()

        # check for player - enemy collisions
        enemy_collisions = check_collisions(player, enemies)
        for index, collision in enumerate(enemy_collisions):
            if collision:
                if enemies[index].health < player.health:
                    player.health -= enemies[index].health * c.contact_damage_multiplier
                    sugar_molecules += sugar_spawner(enemies[index])
                    sounds.devour.play()
                    enemies[index].is_alive = False
                else:
                    enemies[index].health -= player.health
                    player.kill()

        # check for player - sugar collisions
        sugar_collisions = check_collisions(player, sugar_molecules)
        for index, collision in enumerate(sugar_collisions):
            if collision:
                player.sugar += 1
                sugar_molecules[index].picked_up = True

        # check for antibody - enemy collisions
        for antibody in antibodies:
            antibody_collisions = check_collisions(antibody, enemies)
            for index, collision in enumerate(antibody_collisions):
                if collision:
                    enemies[index].health -= c.antibody_damage
                    antibody.outside_screen = True
                    sounds.hit.play()
                    if enemies[index].health <= 0:
                        sugar_molecules += sugar_spawner(enemies[index])
                        enemies[index].is_alive = False

        # check for enemy - storm collisions
        for storm in storms:
            for index, enemy in enumerate(enemies):
                if sqrt((enemy.x - storm.x) ** 2 + (enemy.y - storm.y) ** 2) < storm.radius:
                    enemies[index].health -= c.storm_damage * c.dt
                    if enemies[index].health <= 0:
                        sugar_molecules += sugar_spawner(enemies[index])
                        enemies[index].is_alive = False

        # remove dead enemies and picked up sugars and out of screen antibodies
        enemies = [enemy for enemy in enemies if enemy.is_alive]
        sugar_molecules = [sugar for sugar in sugar_molecules if not sugar.picked_up]
        antibodies = [antibody for antibody in antibodies if not antibody.outside_screen]
        storms = [storm for storm in storms if not storm.over]

        # update UI elements
        health_text.set_text(f"Membrane: {player.health}/{int(player.max_health)}")
        atp_text.set_text(f"ATP: {round(player.atp, 1)}/{int(player.max_atp)}")
        sugar_text.set_text(f"Sugar: {round(player.sugar, 1)} (1 sugar -> {c.sugar_to_atp} ATP or {c.sugar_to_health} health)")
        health_progress_bar.set_progress(player.health / player.max_health)
        atp_progress_bar.set_progress(player.atp / player.max_atp)

        c.screen.fill(c.bg_color)

        # render entities
        for antibody in antibodies:
            antibody.render()
        for storm in storms:
            storm.render()
        player.render()
        for sugar in sugar_molecules:
            sugar.render()
        for enemy in enemies:
            enemy.render()
        
        # render UI elements
        health_text.render()
        atp_text.render()
        sugar_text.render()
        health_progress_bar.render()
        atp_progress_bar.render()

        # render status effects
        if player.respired:
            c.screen.blit(lightning_image, (c.s_width // 2 - 50, c.s_height // 2 - 50))
            player.respired = False

        pg.display.flip()
        c.update_dt()


if __name__ == '__main__':
    pg.init()
    screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
    clock = pg.time.Clock()
    c.set_screen(screen)
    c.set_clock(clock)
    game_loop()