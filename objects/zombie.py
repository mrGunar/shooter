import pygame as pg
import math
import random


class Zombie(pg.sprite.Sprite):
    def __init__(self, x, y, final_point):
        super().__init__()
        self.image = pg.image.load('images/zomb.jpg').convert()
        self.image = pg.transform.scale(self.image, (15, 15))
        self.rect = self.image.get_rect(center = (x, y))
        self.final_point = final_point
        self.hp = 5
        self.dmg = 1

    def draw_hp_bar(self, screen):
        # Draw background rectangle
        pg.draw.rect(screen, (255, 255, 255), [self.rect.x, self.rect.y - 10, self.rect.width, 5])
        # Draw HP bar rectangle
        hp_width = int((self.hp / 100) * self.rect.width)
        pg.draw.rect(screen, (0, 255, 0), [self.rect.x, self.rect.y - 10, hp_width, 5])

    def update(self):
        # Update the player's position or state here
        dx, dy = self.x -  self.final_point.x, self.y -  self.final_point.y
        dist = max(math.hypot(dx, dy), 0.01)
        dx, dy = dx/dist, dy/dist
        self.rect.x -= dx * 2
        self.rect.y -= dy * 2
        
        if self.hp <= 0:
            self.kill()
        
    def take_dmg(self, dmg):
        self.hp -= dmg

    @property
    def x(self):
        return self.rect.centerx

    @property
    def y(self):
        return self.rect.centery


class ZombieBoss(pg.sprite.Sprite):
    def __init__(self, x, y, final_point):
        super().__init__()
        self.image = pg.image.load('images/boss.jpeg').convert()
        self.image = pg.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect(center = (x, y))
        self.final_point = final_point
        self.hp = 50
        self.dmg = 10

    def draw_hp_bar(self, screen):
        # Draw background rectangle
        pg.draw.rect(screen, (255, 255, 255), [self.rect.x, self.rect.y - 10, self.rect.width, 5])
        # Draw HP bar rectangle
        hp_width = int((self.hp / 100) * self.rect.width)
        pg.draw.rect(screen, (0, 255, 0), [self.rect.x, self.rect.y - 10, hp_width, 5])

    def update(self):
        # Update the player's position or state here
        dx, dy = self.x -  self.final_point.x, self.y -  self.final_point.y
        dist = max(math.hypot(dx, dy), 0.01)
        dx, dy = dx/dist, dy/dist
        self.rect.x -= dx * 2
        self.rect.y -= dy * 2
        
        if self.hp <= 0:
            self.kill()
        
    def take_dmg(self, dmg):
        self.hp -= dmg

    @property
    def x(self):
        return self.rect.centerx

    @property
    def y(self):
        return self.rect.centery



def create_zombie(player):
    
    x = random.randint(400, 700)
    y = random.randint(0, 20)
    
    if random.random() < 0.01:
        return ZombieBoss(x, y, player)
    return Zombie(x, y, player)