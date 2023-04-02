import pygame as pg
import sys
import math
from pygame.locals import *
import random

from objects.player import Player
from objects.zombie import create_zombie
from objects.bullet import Bullet

def draw_text(text, color1, color2, x, y, screen, font):
    t = font.render(text, True, color1, color2)
    t_text = t.get_rect()
    t_text.center = (x, y)
    screen.blit(t, t_text)

pg.mixer.pre_init(frequency = 44100, size = 16, channels = 1, buffer = 512)
pg.init()
 
def create_bullet(player_rect, event):
    start_x, start_y = player_rect.x, player_rect.y
    mouse_x, mouse_y = event.pos
    
    angle = math.atan2((mouse_y - start_y), (mouse_x - start_x))
    
    bullet = Bullet(start_x, start_y, angle)
    return bullet







class Game:
    
    def __init__(self):
        self.font = pg.font.Font('freesansbold.ttf', 32)

        self.screen = pg.display.set_mode((1000,600))
        self.clock = pg.time.Clock()


        self.bg_surface = pg.image.load('images/field.jpg').convert()
        self.bg_surface = pg.transform.smoothscale(self.bg_surface, (1000, 600))

        self.menu = False
        self.time_bullet_creation = 20
        self.SCORES = 0

        self.player = Player()

        self.zombies = pg.sprite.Group()

        self.bullets = pg.sprite.Group()

        self.players = pg.sprite.Group()
        self.players.add(self.player)

        self.HEALTH = sum([x.hp for x in self.players])

        self.ROUND = 1
    
    def run(self):
        while True:
            
            if self.menu:
                for event in pg.event.get():
                    if pg.key.get_pressed()[K_r]:
                        self.menu = False
                    if event.type == pg.QUIT:
                            pg.quit()
                            sys.exit()
                draw_text(f'PAUSE',  (255,255,255), (0,0,0), 800, 200, self.screen, self.font)

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

                # Update screen
                self.screen.blit(self.bg_surface,(0,0))

                self.players.update()
                self.players.draw(self.screen)
                for p in self.players:
                    p.draw_hp_bar(self.screen)
                
                self.bullets.update()
                self.bullets.draw(self.screen)
                
                self.zombies.update()
                self.zombies.draw(self.screen)
                for z in self.zombies:
                    z.draw_hp_bar(self.screen)

                # Display SCORES
                draw_text(f'SCORES {self.SCORES}', (255,255,255), (0,0,0), 100, 200, self.screen, self.font)


                # Display PLAYER HEALTH
                draw_text(f'HEALTH {self.HEALTH}', (255,255,255), (0,0,0), 100, 300, self.screen, self.font)

                # Display ROUND
                draw_text(f'ROUND {self.ROUND}', (255,255,255), (0,0,0), 100, 400, self.screen, self.font)
                
                
                if random.random() < 0.01:
                    to_wich_player = random.choice([x for x in self.players])
                    zombie = create_zombie(to_wich_player)
                    self.zombies.add(zombie)


                # Check collision zombie with bullets        
                for bullet in self.bullets:
                    hits = pg.sprite.spritecollide(bullet, self.zombies, False)
                    if hits:
                        bullet.kill()
                        [z.take_dmg(bullet.dmg) for z in hits]
                        self.SCORES += 1
                            
                # Check collision zombies with player
                for zombie in self.zombies:
                    hits = pg.sprite.spritecollide(zombie, self.players, False)
                    if hits:
                        self.HEALTH -= zombie.dmg
                        zombie.kill()

            pg.display.update()
            self.clock.tick(30)


if __name__ == "__main__":
    Game().run()