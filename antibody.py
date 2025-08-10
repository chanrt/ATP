import pygame as pg

from constants import consts as c
from utils import distance_between


class Antibody:
    def __init__(self, x, y, dx, dy, source):
        self.x, self.y = x, y
        self.dx, self.dy = dx, dy
        self.source = source

        self.outside_screen = False
        self.radius = 1

    def update(self):
        self.x += c.antibody_speed * self.dx * c.dt
        self.y += c.antibody_speed * self.dy * c.dt

        if distance_between(self, c.player) > c.s_width:
            self.outside_screen = True

    def render(self):
        x = c.s_width // 2 + self.x - c.player.x
        y = c.s_height // 2 - self.y + c.player.y

        pg.draw.circle(c.screen, c.antibody_color, (x, y), 2)