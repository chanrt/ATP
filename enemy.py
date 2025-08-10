from math import cos, pi, sin, sqrt
from random import random
import pygame as pg

from antibody import Antibody
from constants import consts as c
from sounds import sounds
from utils import *


class Enemy:
    def __init__(self, x, y, enemy_type):
        self.is_alive = True
        self.x, self.y = x, y
        self.type = enemy_type
        self.set_attributes()

    def update(self, antibodies):
        if self.type == "plankton":
            self.x += 2 * (random() - 0.5)
            self.y += 2 * (random() - 0.5)
        if self.type == "euglena":
            self.cycle += 3 * c.cycle_speed * c.dt

            self.dx = c.player.x - self.x
            self.dy = c.player.y - self.y
            norm = sqrt((self.dx * self.dx) + (self.dy * self.dy))
            self.dx /= norm
            self.dy /= norm

            self.x += self.dx * c.euglena_speed * c.dt
            self.y += self.dy * c.euglena_speed * c.dt
        if self.type == "virus":
            self.shoot_cycle += c.virus_shoot_speed * c.dt
            if self.shoot_cycle >= 1 and in_screen(self):
                dx = c.player.x - self.x
                dy = c.player.y - self.y
                norm = sqrt(dx * dx + dy * dy)
                dx /= norm
                dy /= norm
                new_antibody = Antibody(self.x, self.y, dx, dy, "enemy")
                antibodies.append(new_antibody)

                sounds.shoot.play()
                self.shoot_cycle = 0

    def set_attributes(self):
        if self.type == "plankton":
            self.color = c.plankton_color
            self.health = c.plankton_health
            self.spawned_sugars = c.plankton_sugar
            self.spike_angles = [2 * pi * random() for _ in range(c.plankton_spikes)]
        elif self.type == "euglena":
            self.color = c.euglena_color
            self.health = c.euglena_health
            self.spawned_sugars = c.euglena_sugar
            self.cycle = 0
            self.dx, self.dy = 0, 0
        elif self.type == "virus":
            self.color = c.virus_color
            self.health = c.virus_health
            self.spawned_sugars = c.virus_sugar
            self.shoot_cycle = random()

        self.radius = c.radii_multiplier * sqrt(self.health / pi)

    def render(self):
        self.radius = c.radii_multiplier * sqrt(self.health / pi)
        x = c.s_width // 2 + self.x - c.player.x
        y = c.s_height // 2 - self.y + c.player.y

        if self.type == "plankton":
            pg.draw.circle(c.screen, self.color, (x, y), self.radius)
            for index, angle in enumerate(self.spike_angles):
                spike_x = x + self.radius * 1.3 * cos(angle)
                spike_y = y + self.radius * 1.3 * sin(angle)
                pg.draw.line(c.screen, self.color, (x, y), (spike_x, spike_y), 2)

                self.spike_angles[index] += 0.1 * (random() - 0.5)
        elif self.type == "euglena":
            self.major_axis = 2 * self.radius + c.ellipse_wiggle * sin(self.cycle)
            self.minor_axis = 2 * self.radius + c.ellipse_wiggle * sin(self.cycle + pi / 2)
            rect = pg.Rect(
                x - self.major_axis / 2,
                y - self.minor_axis / 2,
                self.major_axis,
                self.minor_axis,)
            
            pg.draw.ellipse(c.screen, self.color, rect)
        elif self.type == "virus":
            radius = self.radius + 0.3 * self.radius * cos(pi / 2 + self.shoot_cycle * pi)
            rect = pg.Rect((x - radius // 2, y - radius // 2, 2 * radius, 2 * radius))
            pg.draw.rect(c.screen, self.color, rect)


class EnemySpawner:
    def __init__(self):
        pass

    def spawn(self, enemies, number=1):
        virus_prob = c.player.level * 0.02
        euglena_prob = c.player.level * 0.03
        plankton_prob = 1 - euglena_prob - virus_prob

        probs = {
            "plankton": plankton_prob,
            "euglena": euglena_prob,
            "virus": virus_prob,
        }

        if number > 1:
            # spawn that many enemies around the player as long as they're not too close
            for _ in range(number):
                enemy_type = random_enemy_type(probs)
                while True:
                    x = 2 * c.s_width * (random() - 0.5)
                    y = 2 * c.s_height * (random() - 0.5)

                    if sqrt((x - c.player.x) ** 2 + (y - c.player.y) ** 2) < c.exclusion_radius:
                        continue
                    else:
                        new_enemy = Enemy(x, y, enemy_type)
                        enemies.append(new_enemy)
                        break
        else:
            enemy_type = random_enemy_type(probs)
            # spawn an enemy around the player but not immediately visible on the screen
            while True:
                x = c.player.x + 2 * c.s_width * (random() - 0.5)
                y = c.player.y + 2 * c.s_height * (random() - 0.5)

                if c.player.x - c.s_width // 2 < x < c.player.x + c.s_width // 2:
                    if c.player.y - c.s_height // 2 < y < c.player.y + c.s_height // 2:
                        continue
                else:
                    new_enemy = Enemy(x, y, enemy_type)
                    enemies.append(new_enemy)
                    break