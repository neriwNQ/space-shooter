from pygame import *
from random import randint
import pygame_menu
from time import time as timer

init()

width = 1200
hight = 800

window = display.set_mode((width, hight))
display.set_caption('Space Shooter')
background = transform.scale(image.load('image/background.jpg'), (width, hight))

lost = 0

class GameSprite(sprite.Sprite):
    def __init__(self, rect_x, rect_y, width, hight, speed, picture):
        super().__init__()
        self.image = transform.scale(image.load(picture), (width, hight))
        self.rect = self.image.get_rect()
        self.rect.x = rect_x
        self.rect.y = rect_y
        self.speed = speed
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 100:
            self.rect.x -= self.speed

        if keys_pressed[K_d] and self.rect.x < 1048:
            self.rect.x += self.speed
    
    def fire(self):
        global bullet
        bullet = Bullet(self.rect.centerx, self.rect.top, 15, 25, -15, 'image/bullet1.png')
        bullets.add(bullet)

    def bossfire(self):
        bulletboss = Bullet(self.rect.centerx, self.rect.top, 15, 25, -15, 'image/bulletboss1.png')
        bulletsboss.add(bulletboss)
        

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > hight:
            lost += 1
            self.rect.x = randint(100, 780)
            self.rect.y = 0

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 730:
            self.kill()

class Wall(sprite.Sprite):
    def __init__(self, color, wall_x, wall_y, wall_width, wall_hieght):
        super().__init__()
        self.color = color
        self.width = wall_width
        self.height = wall_hieght
        self.image = Surface((self.width, self.height))
        self.image.fill((color))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))



font.init()
mixer.init()
mixer.music.set_volume(1)
mixer.music.load('space.ogg')
mixer.music.play()
explode = mixer.Sound('image/shoot2.ogg')


font = font.SysFont('comicsansms', 45)

clock = time.Clock()
FPS = 60
bulletsboss = sprite.Group()
bullets = sprite.Group()
def main():
    counter = 0
    life = 6
    player = Player(550, 720, 80, 80, 10, 'image/player.png')

    asteroids = sprite.Group()
    monsters1 = sprite.Group()
    monsters2 = sprite.Group()
    monsters3 = sprite.Group()
    bossGroup = sprite.Group()

    life_bar = Wall((0, 0, 0), 950, 75, 200, 20)
    life_barG = Wall((14, 156, 26), 950, 75, 200, 20)
    life_barDG = Wall((3, 48, 15), 950, 75, 175, 20)
    life_barY = Wall((235, 255, 56), 950, 75, 150, 20)
    life_barDY = Wall((79, 72, 5), 950, 75, 125, 20)
    life_barR = Wall((240, 17, 20), 950, 75, 100, 20)
    life_barDR = Wall((79, 5, 5), 950, 75, 75, 20)
    life_barDeath = Wall((0, 0, 0), 950, 75, 200, 20)


    for _ in range(2):
        enemy1 = Enemy(randint(100, 1000), 0,  70, 70, randint(1, 3), 'image/enemy1_1.png')
        monsters1.add(enemy1)

    for _ in range(2):
        enemy2 = Enemy(randint(100, 1000), 0,  70, 70, randint(1, 3), 'image/enemy2_2.png')
        monsters2.add(enemy2)

    for _ in range(2):
        enemy3 = Enemy(randint(100, 1000), 0, 70, 70, randint(1, 3), 'image/enemy1_2.png')
        monsters3.add(enemy3)

    for _ in range(1):
        boss = Enemy(randint(100, 1000), 0,  100, 100, randint(1, 3), 'image/boss1.png')
        bossGroup.add(boss)
    
    for _ in range(1):
        asteroid = Asteroid(randint(100, 1000), 0, 85, 85, 2, 'image/meteor_3.png')
        asteroids.add(asteroid)

    num_fire = 0
    rel_time = False
    num_fireBoss = 0
    rel_timeBoss = False

    finish = False

    while True:
        for e in event.get():
            if e.type == QUIT:
                return

            if e.type == KEYDOWN:
                if e.key == K_SPACE:
                    if num_fire < 7 and rel_time == False:
                        player.fire()
                        explode.play()
                        num_fire += 1
                    if num_fire >=7 and rel_time == False:
                        rel_time = True
                        start = timer()

                if e.key == K_q:
                    if num_fireBoss < 3 and rel_timeBoss == False:
                        player.bossfire()
                        explode.play()
                        num_fireBoss += 1
                    if num_fireBoss >=3 and rel_timeBoss == False:
                        rel_timeBoss = True
                        startBoss = timer()
        
                
        if not finish:
            window.blit(background, (0, 0))

            


            player.reset()
            player.update()
            monsters1.update()
            monsters2.update()
            monsters3.update()
            bossGroup.update()
            bullets.update()
            bulletsboss.update()
            monsters1.draw(window)
            monsters2.draw(window)
            monsters3.draw(window)
            bossGroup.draw(window)
            bullets.draw(window)
            bulletsboss.draw(window)
            asteroids.update()
            asteroids.draw(window)
            life_bar.draw_wall()
            if rel_time == True:
                end = timer()
                if end - start < 3:
                    reload_text = font.render('wait, reload', True, (255, 255, 255))
                    window.blit(reload_text, (550, 700))
                else:
                    num_fire = 0
                    rel_time = False
            
            if rel_timeBoss == True:
                endBoss = timer()
                if endBoss - startBoss < 4:
                    reload_textBoss = font.render('wait, reload', True, (255, 255, 255))
                    window.blit(reload_textBoss, (550, 700))
                
                else:
                    num_fireBoss = 0
                    rel_timeBoss = False

            bullets_list1 = sprite.groupcollide(monsters1, bullets, True, True) or sprite.groupcollide(monsters1, bulletsboss, True, True)
            bullets_list2 = sprite.groupcollide(monsters2, bullets, True, True) or sprite.groupcollide(monsters2, bulletsboss, True, True)
            bullets_list3 = sprite.groupcollide(monsters3, bullets, True, True) or sprite.groupcollide(monsters3, bulletsboss, True, True)
            bossbullets_list = sprite.groupcollide(bossGroup, bulletsboss, True, True)
            asteroids_list = sprite.groupcollide(asteroids, bulletsboss, True, True)

            for _ in bullets_list1:
                counter += 1
                enemy1 = Enemy(randint(100, 1000), 0,  70, 70, randint(1, 3), 'image/enemy1_1.png')
                monsters1.add(enemy1)
            
            for _ in bullets_list2:
                counter += 1
                enemy2 = Enemy(randint(100, 1000), 0,  70, 70, randint(1, 3), 'image/enemy2_2.png')
                monsters2.add(enemy2)
            
            for _ in bullets_list3:
                counter += 1
                enemy3 = Enemy(randint(100, 1000), 0, 70, 70, randint(1, 3), 'image/enemy1_2.png')
                monsters3.add(enemy3)
            
            for _ in bossbullets_list:
                counter += 1
                boss = Enemy(randint(100, 1000), 0,  100, 100, randint(1, 3), 'image/boss1.png')
                bossGroup.add(boss)

            for _ in asteroids_list:
                asteroid = Asteroid(randint(100, 1000), 0, 85, 85, 2, 'image/meteor_3.png')
                asteroids.add(asteroid)
            
            if sprite.spritecollide(player, monsters1, True) or sprite.spritecollide(player, monsters2, True) or sprite.spritecollide(player, monsters3, True): 
                life -= 1
            
            if sprite.spritecollide(player, bossGroup, True) or sprite.spritecollide(player, asteroids, True):
                life -= 2

            if counter >= 10:
                win = font.render('YOU WIN!', True, (255, 255, 255))
                window.blit(win, (400, 600))
                finish = True

            if lost >= 3 or life == 0:
                lose = font.render('WASTED!', True, (255, 255, 255))
                window.blit(lose, (400, 600))
                finish = True
            lost_counter = font.render(f'Пропущено: {lost}', True, (255, 255, 255))
            count = font.render(f'Счет: {counter}', True, (255, 255, 255))

        
            window.blit(lost_counter, (50, 50))
            window.blit(count, (50, 100))

            if life == 6:
                life_barG.draw_wall()
            elif life == 5:
                life_barDG.draw_wall()
            elif life == 4:
                life_barY.draw_wall()
            elif life == 3:
                life_barDY.draw_wall()
            elif life == 2:
                life_barR.draw_wall()
            elif life == 1:
                life_barDR.draw_wall()
            else:
                life_barDeath.draw_wall()

                

            display.update()
            
        clock.tick(FPS)




def start_menu():
    menu = pygame_menu.Menu('Shooter', width, hight, theme = pygame_menu.themes.THEME_SOLARIZED)
    menu.add.button('Начать', main)
    menu.add.button('Выйти', pygame_menu.events.EXIT)
    menu.mainloop(window)
start_menu()
