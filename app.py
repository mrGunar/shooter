import pygame as pg
import sys
import math
from pygame.locals import *
import random

from objects.player import Player
from objects.zombie import create_zombie
from objects.bullet import Bullet


pg.mixer.pre_init(frequency = 44100, size = 16, channels = 1, buffer = 512)
pg.init()
 
def create_bullet(player_rect, event):
    start_x, start_y = player_rect.x, player_rect.y
    mouse_x, mouse_y = event.pos
    
    angle = math.atan2((mouse_y - start_y), (mouse_x - start_x))
    
    bullet = Bullet(start_x, start_y, angle)
    return bullet



    



font = pg.font.Font('freesansbold.ttf', 32)

screen = pg.display.set_mode((1000,600))
clock = pg.time.Clock()


bg_surface = pg.image.load('images/field.jpg').convert()
bg_surface = pg.transform.smoothscale(bg_surface, (1000, 600))

menu = False
time_bullet_creation = 20
SCORES = 0

player = Player()

zombies = pg.sprite.Group()

bullets = pg.sprite.Group()

players = pg.sprite.Group()
players.add(player)

HEALTH = sum([x.hp for x in players])

ROUND = 1

while True:
    
    if menu:
        for event in pg.event.get():
            if pg.key.get_pressed()[K_r]:
                menu = False
            if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
    else:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif pg.mouse.get_pressed()[0] == True:
                if time_bullet_creation < 0:
                    bullet = create_bullet(player, event)
                    bullets.add(bullet)
                    time_bullet_creation = 20
            if pg.key.get_pressed()[K_r]:
                menu = True

        time_bullet_creation -= 1

        # Update screen
        screen.blit(bg_surface,(0,0))

        players.update()
        players.draw(screen)
        for p in players:
            p.draw_hp_bar(screen)
        
        bullets.update()
        bullets.draw(screen)
        
        zombies.update()
        zombies.draw(screen)
        for z in zombies:
            z.draw_hp_bar(screen)

        # Display SCORES
        scores = font.render(f'SCORES {SCORES}', True, (255,255,255), (0,0,0))
        scores_text = scores.get_rect()
        scores_text.center = (100, 200)
        screen.blit(scores, scores_text)

        # Display PLAYER HEALTH
        health = font.render(f'HEALTH {HEALTH}', True, (255,255,255), (0,0,0))
        health_text = scores.get_rect()
        health_text.center = (100, 300)
        screen.blit(health, health_text)

        # Display ROUND
        round_ = font.render(f'ROUND {ROUND}', True, (255,255,255), (0,0,0))
        round_text = scores.get_rect()
        round_text.center = (100, 400)
        screen.blit(round_, round_text)
        
        
        if random.random() < 0.01:
            to_wich_player = random.choice([x for x in players])
            zombie = create_zombie(to_wich_player)
            zombies.add(zombie)


        # Check collision zombie with bullets        
        for bullet in bullets:
            hits = pg.sprite.spritecollide(bullet, zombies, False)
            if hits:
                bullet.kill()
                [z.take_dmg(5) for z in hits]
                SCORES += 1
                    
        # Check collision zombies with player
        for zombie in zombies:
            hits = pg.sprite.spritecollide(zombie, players, False)
            if hits:
                HEALTH -= zombie.dmg
                zombie.kill()

        pg.display.update()
        clock.tick(30)
