import pygame as pg
import sys
import random

from pygame.locals import *

from objects.tower import Tower
from objects.zombie import create_zombie, get_zombie_cost
from objects.bullet import create_bullet
from objects.player import Player
from structure import PyGameConfig
from servises import draw_text


class Game:
    """Main game class."""
    def __init__(self):
        self.config = PyGameConfig()

        self.menu = False
        self.time_bullet_creation = 20
        

        self.zombies = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.towers = pg.sprite.Group()
        
        tower = Tower(550, 550)
        self.towers.add(tower)
        
        self.player = Player(tower)
        

        self.ROUND = 1

    def check_zombie_Tower_collision(self) -> None:
        """Checks collision between zombies and Tower. The third parameter means 
        that the object will be killed automaticly."""
        for zombie in self.zombies:
            hits = pg.sprite.spritecollide(zombie, self.towers, False)
            if hits:
                [Tower.take_dmg(zombie.dmg) for Tower in hits]
                zombie.kill()

    def check_zombies_bullets_collision(self) -> None:
        for bullet in self.bullets:
            hits = pg.sprite.spritecollide(bullet, self.zombies, False)
            if hits:
                bullet.kill()
                [zombie.take_dmg(bullet.dmg) for zombie in hits]
                for zombie in self.zombies:
                    if zombie.hp <= 0:
                        money_for_kill = get_zombie_cost(zombie.classification)
                        zombie.kill()
                        self.player.get_money(money_for_kill)
    
    def check_mouse_click_towers_collision(self):
        pos = pg.mouse.get_pos()
        clicked_tower = [s for s in self.towers if s.rect.collidepoint(pos)]
        if clicked_tower:
            self.player.set_tower(clicked_tower[-1])
            return True
        return False

    def update_screen(self) -> None:
        self.config.screen.blit(self.config.bg_surface,(0,0))

        self.towers.update()
        self.towers.draw(self.config.screen)
        for p in self.towers:
            p.draw_hp_bar(self.config.screen)
        
        self.bullets.update()
        self.bullets.draw(self.config.screen)
        
        self.zombies.update()
        self.zombies.draw(self.config.screen)
        for z in self.zombies:
            z.draw_hp_bar(self.config.screen)

    def display_game_text(self):

        # Display ROUND
        draw_text(f'ROUND {self.ROUND}', 100, 100, self.config.screen, self.config.font)
        draw_text(f'Switch weapon: Z', 100, 150, self.config.screen, self.config.font)
        draw_text(f'Buy bullets: 1', 100, 200, self.config.screen, self.config.font)
        draw_text(f'Buy big bullets: 2', 100, 250, self.config.screen, self.config.font)
        draw_text(f'Buy kernels: 3', 100, 300, self.config.screen, self.config.font)
        
        for i, line in enumerate(self.player.show_info()):
            draw_text(line, 900, 100 + i * 20, self.config.screen, self.config.font)


    def create_game_monster(self):
        if random.random() < 0.01:
            to_wich_tower = random.choice([t for t in self.towers])
            zombie = create_zombie(to_wich_tower)
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
                        if self.check_mouse_click_towers_collision():
                            pass
                        elif self.time_bullet_creation < 0 and self.player.tower.check_bullet_available():
                            bullet = create_bullet(self.player.tower, event, 30, self.player.tower.current_bullet)
                            self.player.tower.shoot()
                            self.bullets.add(bullet)
                            self.time_bullet_creation = 20
                    if pg.key.get_pressed()[K_r]:
                        self.menu = True

                    if pg.key.get_pressed()[K_z]:
                        self.player.tower.change_bullet()

                    if pg.key.get_pressed()[K_1]:
                        if self.player.money - 25 >= 0:
                            self.player.tower.get_base_bullet()
                            self.player.take_money(25)
                    if pg.key.get_pressed()[K_2]:
                        if self.player.money - 50 >= 0:
                            self.player.tower.get_big_bullets()
                            self.player.take_money(50)
                    if pg.key.get_pressed()[K_3]:
                        if self.player.money - 200 >= 0:
                            self.player.tower.get_kernels()
                            self.player.take_money(200)
                    if pg.key.get_pressed()[K_x]:
                        new_tower = Tower(600, 550)
                        self.towers.add(new_tower)

                self.time_bullet_creation -= 1

                self.update_screen()

                self.display_game_text()

                self.create_game_monster()

                self.check_zombies_bullets_collision()

                self.check_zombie_Tower_collision()
                
            pg.display.update()
            self.config.clock.tick(30)