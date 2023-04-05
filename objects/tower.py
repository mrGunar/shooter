import pygame as pg
from itertools import cycle

from .bullet import get_all_bullet, BulletClassification


ALL_BULLETS = cycle(get_all_bullet())


class Tower(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pg.image.load('images/player.jpg').convert_alpha()
        self.image = pg.transform.scale(self.image, (25, 25))
        self.rect = self.image.get_rect(center = (x, y))
        self.hp = 100

        self.current_bullet = next(ALL_BULLETS)

        self.available_current_bullet = False
        self.equipment = {x: 10 for x in get_all_bullet()}

    def check_bullet_available(self):
        return self.equipment[self.current_bullet] > 0
    
    def shoot(self):
        self.equipment[self.current_bullet] -= 1

    def update(self):
        # Update the Tower's position or state here
        pass

    def draw_hp_bar(self, screen):
        # Draw background rectangle
        pg.draw.rect(screen, (255, 255, 255), [self.rect.x, self.rect.y - 10, self.rect.width, 5])
        # Draw HP bar rectangle
        hp_width = int((self.hp / 100) * self.rect.width)
        pg.draw.rect(screen, (0, 255, 0), [self.rect.x, self.rect.y - 10, hp_width, 5])

    def take_dmg(self, dmg):
        self.hp -= dmg

        if self.hp <= 0:
            self.kill()

    def get_hp(self, hp):
        self.hp += hp


    def change_bullet(self):
        self.current_bullet = next(ALL_BULLETS)

    @property
    def x(self):
        return self.rect.centerx

    @property
    def y(self):
        return self.rect.centery

    def show_info(self):
        return  [f"Health: {self.hp}", f"Bullet: {self.current_bullet.value}",
                 f"Left: {self.equipment[self.current_bullet]}"]

    def get_base_bullet(self):
        self.equipment[BulletClassification.bullet] += 20

    def get_big_bullets(self):
        self.equipment[BulletClassification.big_bullet] += 10

    def get_kernel(self):
        self.equipment[BulletClassification.kernel] += 20