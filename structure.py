from dataclasses import dataclass
import pygame as pg

pg.mixer.pre_init(frequency = 44100, size = 16, channels = 1, buffer = 512)
pg.init()


@dataclass
class Coordinate:
    x : int
    y: int


@dataclass
class PyGameConfig:
        font = pg.font.Font('freesansbold.ttf', 32)
        screen = pg.display.set_mode((1000,600))
        clock = pg.time.Clock()
        bg_surface = pg.image.load('images/field.jpg').convert()

        def __post_init__(self):
            self.bg_surface = pg.transform.smoothscale(self.bg_surface, (1000, 600))