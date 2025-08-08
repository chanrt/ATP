from math import pi, sqrt
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
            pass

    def set_attributes(self):
        if self.type == "plankton":
            self.color = c.plankton_color
            self.health = c.plankton_health
            self.spawned_sugars = c.plankton_sugar

        self.radius = c.radii_multiplier * sqrt(self.health / pi)

    def render(self):
        self.radius = c.radii_multiplier * sqrt(self.health / pi)
        pg.draw.circle(c.screen, self.color, (c.s_width // 2 + self.x - c.player.x, c.s_height // 2 - self.y + c.player.y), self.radius)