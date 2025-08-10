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
        if self.type == "euglena":
            self.cycle += 3 * c.cycle_speed * c.dt

            self.dx = c.player.x - self.x
            self.dy = c.player.y - self.y
            norm = sqrt((self.dx * self.dx) + (self.dy * self.dy))
            self.dx /= norm
            self.dy /= norm

            self.x += self.dx * c.euglena_speed * c.dt
            self.y += self.dy * c.euglena_speed * c.dt

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