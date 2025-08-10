from os import path
import pygame as pg


class Sounds:
    def __init__(self):
        pg.mixer.init()
        self.bg_music = pg.mixer.music.load(path.join(path.dirname(__file__), "assets", "bg_music.mp3"))

        self.devour = self.load_sound("devour.mp3")
        self.evolve = self.load_sound("evolve.wav")
        self.shoot = self.load_sound("shoot.wav")
        self.hit = self.load_sound("hit.wav")
        self.game_over = self.load_sound("game_over.wav")
        self.respawn = self.load_sound("respawn.wav")

    def load_sound(self, name):
        return pg.mixer.Sound(path.join(path.dirname(__file__), "assets", "sounds", name))

    def play_bg_music(self):
        pg.mixer.music.play(-1)

    def stop_bg_music(self):
        pg.mixer.music.pause()

sounds = Sounds()