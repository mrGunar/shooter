import pygame as pg
import math


class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        self.image = pg.image.load('images/bullet.png').convert()
        self.image = pg.transform.scale(self.image, (2, 2))
        self.rect = self.image.get_rect(center = (x, y))
        self.angle = angle
        self.dmg = 5

    def update(self):
        self.rect.x += 10 * math.cos(self.angle)
        self.rect.y += 10 * math.sin(self.angle)
    
    @property
    def x(self):
        return self.rect.centerx

    @property
    def y(self):
        return self.rect.centery