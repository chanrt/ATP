import pygame as pg

from constants import consts as c
from utils import *


class Sugar:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.radius = c.sugar_radius
        self.picked_up = False

    def render(self):
        pg.draw.circle(c.screen, c.sugar_color, (c.s_width // 2 + self.x - c.player.x, c.s_height // 2 - self.y + c.player.y), c.sugar_radius)