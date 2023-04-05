import pygame as pg
import math
import random
from enum import Enum, auto


class ZombieClassification(Enum):
    zombie = auto()
    zombie_boss = auto()


class BaseZombie:
    def __init__(self, final_point, zombie_speed=2):
        self.final_point = final_point
        self.count = 0
        self.zombie_speed = zombie_speed

    def draw_hp_bar(self, screen):
        # Draw background rectangle
        pg.draw.rect(screen, (255, 255, 255), [self.rect.x, self.rect.y - 10, self.rect.width, 5])
        # Draw HP bar rectangle
        hp_width = int((self.hp / 100) * self.rect.width)
        pg.draw.rect(screen, (0, 255, 0), [self.rect.x, self.rect.y - 10, hp_width, 5])

    def update(self):
        # Update the Tower's position or state here
        self.count += 1
        if self.count >= self.zombie_speed:
            dx, dy = self.x -  self.final_point.x, self.y -  self.final_point.y
            dist = max(math.hypot(dx, dy), 0.01)
            dx_e = random.randint(-2, 2)
            dx, dy = dx/dist, dy/dist
            self.rect.x -= dx * 10
            self.rect.y -= dy * 10
            self.count = 0
        
    def take_dmg(self, dmg):
        self.hp -= dmg

    @property
    def x(self):
        return self.rect.centerx

    @property
    def y(self):
        return self.rect.centery

class Zombie(BaseZombie, pg.sprite.Sprite):
    def __init__(self, x, y, final_point):
        super().__init__(final_point, zombie_speed=10)
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load('images/zomb.jpg').convert_alpha()
        self.image = pg.transform.scale(self.image, (15, 15))
        self.rect = self.image.get_rect(center = (x, y))
        self.hp = 10
        self.dmg = 5
        self.classification = ZombieClassification.zombie


class ZombieBoss(BaseZombie, pg.sprite.Sprite):
    def __init__(self, x, y, final_point):
        super().__init__(final_point, zombie_speed=30)
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load('images/boss.jpeg').convert_alpha()
        self.image = pg.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect(center = (x, y))
        self.hp = 75
        self.dmg = 15
        self.classification = ZombieClassification.zombie_boss


def create_zombie(Tower):
    
    x = random.randint(400, 700)
    y = random.randint(0, 20)

    if random.random() < 0.3:
        return ZombieBoss(x, y, Tower)
    return Zombie(x, y, Tower)


def get_zombie_cost(z: ZombieClassification) -> int:
    zombie_cost = {
        ZombieClassification.zombie: 2,
        ZombieClassification.zombie_boss: 10,
    }
    return zombie_cost[z]
