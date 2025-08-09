import pygame as pg


class Constants:
    def __init__(self):
        self.fps = 30
        self.dt = 1.0 / self.fps

        self.init_colors()

        self.level_atps = [100, 200, 300, 400, 500]
        self.max_upgrades = 3

        # movement parameters
        self.cycle_speed = 3
        self.player_accn = 25
        
        self.player_drag = 0.05
        self.move_atp_cost = 0.01

        # parameters subject to upgrades
        self.player_max_health = 100
        self.player_max_v = 100
        self.sugar_to_atp = 5
        self.sugar_synthesis_rate = 0
        self.atp_req_multiplier = 1.0
        self.sugar_multiplier = 1.0
        self.respawn = 0

        self.plankton_health = 20
        self.plankton_sugar = 5
        self.plankton_spikes = 20

    def init_colors(self):
        self.black = pg.Color("#000000")
        self.player_color = pg.Color("#1f51ff")
        self.bg_color = pg.Color("#222222")
        self.plankton_color = pg.Color("#4cd038")
        self.sugar_color = pg.Color("#eeeeee")

    def set_screen(self, screen):
        self.screen = screen
        self.s_width, self.s_height = pg.display.get_surface().get_size()
        print("Screen dimensions:", self.s_width, self.s_height)

        self.radii_multiplier = self.s_height // 100
        self.ellipse_wiggle = self.s_height // 100
        
        self.sugar_radius = self.s_height // 200
        self.splash_radius = self.s_height // 50

        self.title_font_size = self.s_height // 15
        self.stats_font_size = self.title_font_size // 2

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