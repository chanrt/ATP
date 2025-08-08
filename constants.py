import pygame as pg


class Constants:
    def __init__(self):
        self.fps = 30
        self.dt = 1.0 / self.fps

        self.player_color = (0, 255, 0)
        self.bg_color = (0, 0, 255)

        self.player_accn = 10
        self.player_max_v = 100
        self.player_drag = 0.05

    def set_screen(self, screen):
        self.screen = screen
        self.s_width, self.s_height = pg.display.get_surface().get_size()
        print("Screen dimensions:", self.s_width, self.s_height)

        self.player_radius = self.s_height // 50

    def set_clock(self, clock):
        self.clock = clock

    def update_dt(self):
        actual_fps = self.clock.get_fps()
        if actual_fps == 0:
            self.dt = 1.0 / self.fps
        else:
            self.dt = 1.0 / actual_fps


consts = Constants()