import pygame as pg
from itertools import cycle

from .bullet import get_all_bullet


ALL_BULLETS = cycle(get_all_bullet())


class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load('images/player.jpg').convert()
        self.image = pg.transform.scale(self.image, (25, 25))
        self.rect = self.image.get_rect(center = (550,500))
        self.hp = 100
        self.money = 0

        self.current_bullet = next(ALL_BULLETS)

        self.available_current_bullet = False
        self.equipment = {x: 10 for x in get_all_bullet()}

    def check_bullet_available(self):
        print(self.equipment[self.current_bullet])
        return self.equipment[self.current_bullet] > 0
    
    def shoot(self):
        self.equipment[self.current_bullet] -= 1

    def update(self):
        # Update the player's position or state here
        pass

    def draw_hp_bar(self, screen):
        # Draw background rectangle
        pg.draw.rect(screen, (255, 255, 255), [self.rect.x, self.rect.y - 10, self.rect.width, 5])
        # Draw HP bar rectangle
        hp_width = int((self.hp / 100) * self.rect.width)
        pg.draw.rect(screen, (0, 255, 0), [self.rect.x, self.rect.y - 10, hp_width, 5])

    def take_dmg(self, dmg):
        self.hp -= dmg

    def get_hp(self, hp):
        self.hp += hp

    def take_money(self, m):
        if self.money - m >= 0:
            self.money -= m
            return True
        return False

    def get_money(self, m):
        self.money += m

    def change_bullet(self):
        self.current_bullet = next(ALL_BULLETS)

    @property
    def x(self):
        return self.rect.centerx

    @property
    def y(self):
        return self.rect.centery

    def text_info(self):
        return  [f"Money: {self.money}", f"Health: {self.hp}", f"Bullet: {self.current_bullet.value}",
                 f"Left: {self.equipment[self.current_bullet]}"
                 ]