import sys
import os
import pygame

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
        self.obsticals = []

        self.f.open('data/score.txt', 'r')
        self.highscore = int(self.f)
        self.f.close

        self.score = 0

        self.player = PhysicsEntity(self, 'bike', (50, 50), (8, 15), 3)

        self.ui = UI("PressStart2P-vaV7.ttf")

        self.tilemap = Tilemap(self)

        self.currentlevel = 1

        self.leveldistance = self.currentlevel * 100

        self.playerdistance = 0

        self.mousepos = (0, 0)

        self.textbox = []

        self.scroll = [0, 0]

    def run(self, running, gamemode):
        for enemy in self.currentlevel:
            self.obsticals.append(GravatyEntity(self, 'tree', (0, 0), (16, 16), self.currentlevel))
        while running:
            self.display.blit(self.assets['background'], (0, 0))

            self.tilemap.render(self.display, offset=(0,0))

            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], self.movement[2] - self.movement[3]))
            self.player.render(self.display, offset=(0,0))

            self.clouds.update()
            self.clouds.render(self.display, offset=(0,self.playerdistance))

            self.screen.blit(self.ui.render(self.display, "Score:" + str(self.score), (1, 1)))
            if gamemode == 1:
                self.screen.blit(self.ui.render(self.display, "Health:" + str(self.player.health), (100, 1)))
            self.screen.blit(self.ui.render(self.display, "High Score:" + str(self.highscore), (200, 1)))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.f.open("data/score.txt", 'w')
                    if self.score > self.highscore:
                        self.f.write(self.score)
                    self.f.close
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

            self.playerdistance += 1
            if self.playerdistance > self.leveldistance:
                self.ui.render("Level Beat", 100, 100)

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

    def menu(self, running):
        while running:
            self.mousepos = pygame.mouse.get_pos()
            self.display.blit(self.assets['background'], (0, 0))

            self.clouds.update()
            self.clouds.render(self.display, offset=(0,0))

            self.playClassic = UI.render(self, self.display, "Play Classic", ((self.display.get_width/2)-100, 100))
            self.playComprehension = UI.render(self, self.display, "Play Comprehension", ((self.display.get_width/2)-100, 150))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.playClassic.get_rect().collide(self.mousepos):
                        Game().run(1,1)
                    if self.playComprehension.get_rect().collide(self.mousepos):
                        Game().run(1,2)
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)


Game().menu(1,0)
