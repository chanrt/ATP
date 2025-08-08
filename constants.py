import pygame as pg


class Constants:
    def __init__(self):
        self.fps = 30
        self.dt = 1.0 / self.fps

        self.init_colors()

        self.player_accn = 25
        self.player_max_v = 100
        self.player_drag = 0.05

        self.plankton_sugar = 5

    def init_colors(self):
        self.player_color = pg.Color("#1f51ff")
        self.bg_color = pg.Color("#111111")
        self.plankton_color = pg.Color("#4cd038")
        self.sugar_color = pg.Color("#eeeeee")

    def set_screen(self, screen):
        self.screen = screen
        self.s_width, self.s_height = pg.display.get_surface().get_size()
        print("Screen dimensions:", self.s_width, self.s_height)

        self.radii_multiplier = self.s_height // 100
        self.player_health = 100
        self.plankton_health = 20
        self.sugar_radius = self.s_height // 200
        self.splash_radius = self.s_height // 50

    def set_clock(self, clock):
        self.clock = clock

    def set_player(self, player):
        self.player = player

    def update_dt(self):
        actual_fps = self.clock.get_fps()
        if actual_fps == 0:
            self.dt = 1.0 / self.fps
        else:
            self.dt = 1.0 / actual_fps


consts = Constants()