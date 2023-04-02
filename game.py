import pygame as pg
import sys
from pygame.locals import *
import random

from objects.player import Player
from objects.zombie import create_zombie
from objects.bullet import Bullet, create_bullet
from structure import Coordinate, PyGameConfig
from servises import draw_text


class Game:
    """Main game class."""
    def __init__(self):
        self.config = PyGameConfig()

        self.menu = False
        self.time_bullet_creation = 20

        self.zombies = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.players = pg.sprite.Group()
        
        self.player = Player()
        self.players.add(self.player)

        self.HEALTH = self.update_player_hp()
        self.ROUND = 1
        self.SCORES = 0

    def update_player_hp(self):
        return sum([x.hp for x in self.players])

    def check_zombie_player_collision(self):
        for zombie in self.zombies:
            hits = pg.sprite.spritecollide(zombie, self.players, False)
            if hits:
                self.player.take_dmg(zombie.dmg)
                print("ALO")
                zombie.kill()

    def check_zombies_bullets_collision(self):
        for bullet in self.bullets:
            hits = pg.sprite.spritecollide(bullet, self.zombies, False)
            if hits:
                bullet.kill()
                [zombie.take_dmg(bullet.dmg) for zombie in hits]
                self.SCORES += 1

    def update_screen(self):
        self.config.screen.blit(self.config.bg_surface,(0,0))

        self.players.update()
        self.players.draw(self.config.screen)
        for p in self.players:
            p.draw_hp_bar(self.config.screen)
        
        self.bullets.update()
        self.bullets.draw(self.config.screen)
        
        self.zombies.update()
        self.zombies.draw(self.config.screen)
        for z in self.zombies:
            z.draw_hp_bar(self.config.screen)

    def display_game_text(self):
        # Display SCORES
        draw_text(f'SCORES {self.SCORES}', 100, 200, self.config.screen, self.config.font)

        # Display PLAYER HEALTH
        draw_text(f'HEALTH {self.HEALTH}', 100, 300, self.config.screen, self.config.font)

        # Display ROUND
        draw_text(f'ROUND {self.ROUND}', 100, 400, self.config.screen, self.config.font)


    def create_game_monster(self):
        if random.random() < 0.01:
            to_wich_player = random.choice([player for player in self.players])
            zombie = create_zombie(to_wich_player)
            self.zombies.add(zombie)

    def run(self):
        while True:
            if self.menu:
                for event in pg.event.get():
                    if pg.key.get_pressed()[K_r]:
                        self.menu = False
                    if event.type == pg.QUIT:
                            pg.quit()
                            sys.exit()
                draw_text(f'PAUSE', 800, 200, self.config.screen, self.config.font)
            else:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                        sys.exit()
                    elif pg.mouse.get_pressed()[0] == True:
                        if self.time_bullet_creation < 0:
                            bullet = create_bullet(self.player, event)
                            self.bullets.add(bullet)
                            self.time_bullet_creation = 20
                    if pg.key.get_pressed()[K_r]:
                        self.menu = True

                    self.time_bullet_creation -= 1

                    self.update_screen()

                    self.display_game_text()

                    self.create_game_monster()

                    self.check_zombies_bullets_collision()

                    self.check_zombie_player_collision()
                    
                    self.HEALTH = self.update_player_hp()
                
            pg.display.update()
            self.config.clock.tick(30)


           
