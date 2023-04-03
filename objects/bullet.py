import pygame as pg
import math
from enum import Enum, auto


class BulletClassification(Enum):
    bullet = auto()
    big_bullet = auto()
    kernel =auto()


class BaseBullet:
    """Base represantation of the bullet."""
    def update(self):
        self.rect.x += int(self.speed * math.cos(self.angle))
        self.rect.y += int(self.speed * math.sin(self.angle))
        
        if self.rect.y <= 0:
            self.kill()


class Bullet(BaseBullet, pg.sprite.Sprite):
    def __init__(self, x, y, angle, damage=5, speed=10):
        super().__init__()
        pg.sprite.Sprite.__init__(self)

        self.image = pg.image.load('images/bullet.png').convert()
        self.image = pg.transform.scale(self.image, (2, 2))
        self.rect = self.image.get_rect(center = (x, y))
        self.angle = angle
        self.dmg = damage
        self.speed = speed + 25

class BigBullet(BaseBullet, pg.sprite.Sprite):
    def __init__(self, x, y, angle, damage=5, speed=10):
        super().__init__()
        pg.sprite.Sprite.__init__(self)

        self.image = pg.image.load('images/bullet.png').convert()
        self.image = pg.transform.scale(self.image, (4, 4))
        self.rect = self.image.get_rect(center = (x, y))
        self.angle = angle
        self.dmg = damage + 15
        self.speed = speed + 10

class Kernel(BaseBullet, pg.sprite.Sprite):
    def __init__(self, x, y, angle, damage=5, speed=10):
        super().__init__()
        pg.sprite.Sprite.__init__(self)

        self.image = pg.image.load('images/bullet.png').convert()
        self.image = pg.transform.scale(self.image, (10, 10))
        self.rect = self.image.get_rect(center = (x, y))
        self.angle = angle
        self.dmg = damage + 55
        self.speed = speed - 5


def create_bullet(start_point, mouse_click_event, damage, bullet_class) -> BaseBullet:
    """Method takes the start player coordinates and the mouse point 
    and calculates direction by two points on the game surface using the math module.
    """
    start_x, start_y = start_point.x, start_point.y
    mouse_x, mouse_y = mouse_click_event.pos
    
    angle = math.atan2((mouse_y - start_y), (mouse_x - start_x))
    
    bullet_classes = {
        BulletClassification.bullet: Bullet,
        BulletClassification.big_bullet: BigBullet,
        BulletClassification.kernel: Kernel,
    }

    return bullet_classes[bullet_class](start_x, start_y, angle, damage)


def get_all_bullet():
    return [x for x in BulletClassification]