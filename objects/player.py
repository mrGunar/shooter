import pygame as pg


class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load('images/player.jpg').convert()
        self.image = pg.transform.scale(self.image, (25, 25))
        self.rect = self.image.get_rect(center = (550,500))
        self.hp = 100

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


    @property
    def x(self):
        return self.rect.centerx

    @property
    def y(self):
        return self.rect.centery

