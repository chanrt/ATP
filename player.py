from math import pi, sqrt

import pygame as pg

from constants import consts as c


class Player:
    def __init__(self):
        self.x, self.y = 0, 0
        self.vx, self.vy = 0, 0
        self.ax, self.ay = 0, 0

        self.health = c.player_health
        self.sugar = 0
        self.atp = 0

        self.radius = c.radii_multiplier * sqrt(self.health / pi)

    def update(self):
        self.v = sqrt(self.vx * self.vx + self.vy * self.vy)
        if self.v < c.player_max_v:
            self.vx += self.ax * c.dt
            self.vy += self.ay * c.dt

        if self.ax == 0:
            self.vx -= c.player_drag * self.vx
        if self.ay == 0:
            self.vy -= c.player_drag * self.vy
        
        self.x += self.vx * c.dt
        self.y += self.vy * c.dt

    def move(self, keys_pressed):
        num_pressed = sum([keys_pressed[key] for key in keys_pressed])

        # ignore illegal combinations
        if (keys_pressed["up"] and keys_pressed["down"]) or (keys_pressed["left"] and keys_pressed["right"]) or num_pressed == 0:
            self.ax = 0
            self.ay = 0
            return
        
        if not (keys_pressed["up"] or keys_pressed["down"]):
            self.ay = 0
        if not (keys_pressed["left"] or keys_pressed["right"]):
            self.ax = 0
        
        if keys_pressed["up"]:
            self.ay = c.player_accn / sqrt(num_pressed)
        elif keys_pressed["right"]:
            self.ax = c.player_accn / sqrt(num_pressed)
        elif keys_pressed["down"]:
            self.ay = -c.player_accn / sqrt(num_pressed)
        elif keys_pressed["left"]:
            self.ax = -c.player_accn / sqrt(num_pressed)

    def render(self):
        self.radius = c.radii_multiplier * sqrt(self.health / pi)
        pg.draw.circle(c.screen, c.player_color, (c.s_width // 2, c.s_height // 2), self.radius)