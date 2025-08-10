import pygame as pg


from constants import consts as c


class Storm:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.radius = 5
        self.over = False

    def update(self):
        self.radius += c.storm_speed * c.dt
        if self.radius > c.storm_limit:
            self.over = True

    def render(self):
        x = c.s_width // 2 + self.x - c.player.x
        y = c.s_height // 2 - self.y + c.player.y
        pg.draw.circle(c.screen, c.sugar_color, (x, y), self.radius, 2)