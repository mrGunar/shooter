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
        self.rect.x += 30 * math.cos(self.angle)
        self.rect.y += 30 * math.sin(self.angle)
    
    @property
    def x(self):
        return self.rect.centerx

    @property
    def y(self):
        return self.rect.centery

def create_bullet(start_point, mouse_click_event):
    """Method takes the start player coordinates and the mouse point 
    and calculates direction by two points on the game surface using the math module.
    """
    start_x, start_y = start_point.x, start_point.y
    mouse_x, mouse_y = mouse_click_event.pos
    
    angle = math.atan2((mouse_y - start_y), (mouse_x - start_x))
    
    bullet = Bullet(start_x, start_y, angle)
    return bullet