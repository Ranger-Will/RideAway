import sys
import os
import pygame
import random

from scripts.entities import PhysicsEntity, GravatyEntity
from scripts.tilemap import Tilemap
from scripts.clouds import Clouds
from scripts.ui import UI

BASE_IMG_PATH = 'data/images/'

def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey((0, 0, 0))
    return img

def load_images(path):
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        images.append(load_image(path + '/' + img_name))
    return images

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('ninja game')
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((320, 240))

        self.clock = pygame.time.Clock()

        self.movement = [False, False, False, False]

        self.assets = {
            'bike': load_image('entities/bike.png'),
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
            'player': load_image('entities/player.png'),
            'background': load_image('background.png'),
            'clouds': load_images('clouds'),
        }

        self.clouds = Clouds(self.assets['clouds'], count=10)
        self.obsticals = {}

        with open('data/score.txt', 'r') as f:
            self.highscore = f.read()
        f.close()

        self.score = 0

        self.player = PhysicsEntity(self, 'bike', (50, 50), (16, 16), 3)

        self.ui = UI("PressStart2P-vaV7.ttf")

        self.tilemap = Tilemap(self)

        self.currentlevel = 1

        self.hasupdatedenemies = 0

        self.leveldistance = self.currentlevel * 1000

        self.playerdistance = 0

        self.mousepos = (0, 0)

    def run(self, running, gamemode):
        while running:
            if self.hasupdatedenemies == 0:
                for enemy in range(int(self.leveldistance / 10)):
                    self.obsticals.update({enemy: GravatyEntity(self, 'tree', (0, 0), (16, 16), self.currentlevel)})
                    self.hasupdatedenemies = 1   

            if (self.playerdistance // 10) == 0:
              self.obsticals[0].pos[0] = random.randrange(16, self.screen.get_width() - 16)
              self.obsticals[0].grav = 1

            if self.obsticals[0].pos[1] > 240:
                self.obsticals.pop(0)

            self.display.blit(self.assets['background'], (0, 0))

            self.tilemap.render(self.display, offset=(0,0))

            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], self.movement[2] - self.movement[3]))
            self.player.render(self.display, offset=(0,0))

            for enemies in self.obsticals:
               self.obsticals[enemies].render(self.display)

            self.clouds.update()
            self.clouds.render(self.display, offset=(0,-self.playerdistance))

            self.display.blit(self.ui.render("Score:" + str(self.score)), (1, 1))
            if gamemode == 1:
                self.display.blit(self.ui.render("Health:" + str(self.player.health)), (100, 1))
            self.display.blit(self.ui.render("High Score:" + str(self.highscore)), (200, 1))
    
            if self.playerdistance >= self.leveldistance:
                self.display.blit(self.ui.render("Level Beat"), (100, 100))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    with open("data/score.txt", 'w') as f:
                        if self.score > int(self.highscore):
                            f.write(str(self.score))
                    f.close()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_UP:
                        self.movement[3] = True
                    if event.key == pygame.K_DOWN:
                        self.movement[2] = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False
                    if event.key == pygame.K_UP:
                        self.movement[3] = False
                    if event.key == pygame.K_DOWN:
                        self.movement[2] = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 1:
                        self.currentlevel += 1
                        self.playerdistance = 0
                        
            

            self.playerdistance += 1

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

    def menu(self, running):
        while running:
            self.mousepos = pygame.mouse.get_pos()
            self.display.blit(self.assets['background'], (0, 0))

            self.clouds.update()
            self.clouds.render(self.display, offset=(0,0))

            self.display.blit(self.ui.render("Play Classic"), ((self.display.get_width()/2)-100, 100))
            self.display.blit(self.ui.render("Play Comprehension"), ((self.display.get_width()/2)-100, 150))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 2:
                        Game().run(1,1)
                    if 1:
                        Game().run(1,2)
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

Game().menu(1)
