from math import cos, pi, sin, sqrt
from random import random
import pygame as pg

from constants import consts as c


class Enemy:
    def __init__(self, x, y, enemy_type):
        self.is_alive = True
        self.x, self.y = x, y
        self.type = enemy_type
        self.set_attributes()

    def update(self):
        if self.type == "plankton":
            self.x += 2 * (random() - 0.5)
            self.y += 2 * (random() - 0.5)

    def set_attributes(self):
        if self.type == "plankton":
            self.color = c.plankton_color
            self.health = c.plankton_health
            self.spawned_sugars = c.plankton_sugar

            self.spike_angles = [2 * pi * random() for _ in range(c.plankton_spikes)]

        self.radius = c.radii_multiplier * sqrt(self.health / pi)

    def render(self):
        self.radius = c.radii_multiplier * sqrt(self.health / pi)
        x = c.s_width // 2 + self.x - c.player.x
        y = c.s_height // 2 - self.y + c.player.y
        pg.draw.circle(c.screen, self.color, (x, y), self.radius)

        if self.type == "plankton":
            for index, angle in enumerate(self.spike_angles):
                spike_x = x + self.radius * 1.3 * cos(angle)
                spike_y = y + self.radius * 1.3 * sin(angle)
                pg.draw.line(c.screen, self.color, (x, y), (spike_x, spike_y), 2)

                self.spike_angles[index] += 0.1 * (random() - 0.5)