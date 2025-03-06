import sys
import os
import pygame
import random

from scripts.entities import PhysicsEntity, GravatyEntity
from scripts.tilemap import Tilemap
from scripts.clouds import Clouds
from scripts.ui import UI
from scripts.questions import questions

BASE_IMG_PATH = 'data/images/'

questionlist = ["What did was Jonas's full job title?", 'What was the first color Jonas saw?',
                'How many kids were in an average age group?', 'Where are all the records of private cerimonies?',
                'How many Recivers have there been?', 'How did Jonas escape?',
                'Where did his father inject the baby?', 'What did Gabriel mistake for a plane?',
                'How long before the Ceremony was Jonas supposed to escape?',
                "How far into Rosemary's training was she released", 'Children get their assingments at 12',
                'Jonas was allowed to lie', "Lily's comfort object was a snake",
                'Nobody can find the biclycle repair department',
                "Did Jonas's assingment Ceremony go smoothly"]

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

        self.answeringquestion = False

        self.player = PhysicsEntity(self, 'bike', (160,120), (16, 16), 3)
        self.ui = UI("PressStart2P-vaV7.ttf")
        self.tilemap = Tilemap(self)
        self.showquestion = False
        self.isCorrect = False

        self.currentlevel = 1
        self.hasupdatedenemies = 0
        self.levelbeat = False
        self.leveldistance = self.currentlevel * 1000
        self.playerdistance = 0

        self.mousepos = (0, 0)

        self.rects = []

    def randomizeanswers(self, question):
        copied = []
        for anwers in questions[question]:
            copied.append(anwers)
        random.shuffle(copied)
        return copied

    def run(self, gamemode):
        while True:
            self.mousepos = pygame.mouse.get_pos()
            self.display.blit(self.assets['background'], (0, 0))

            self.tilemap.render(self.display, offset=(0,0))

            if (self.playerdistance % 300) == 0:
                self.showquestion = True
                self.question = questionlist[random.randrange(0,14)]
                self.correctAnswer = list(questions[self.question])[0]
                answers = self.randomizeanswers(self.question)
                self.switchquestion = 1

            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], self.movement[2] - self.movement[3]))
            self.player.render(self.display, offset=(0,0))

            self.clouds.update()
            self.clouds.render(self.display, offset=(0,-self.playerdistance))

            if self.showquestion:
                self.display.blit(self.ui.render(self.question), (30, 20))
                ah = self.ui.render(self.question).get_rect()
                ah[0] = 30
                ah[1] = 20
                ah[0] *= 2
                ah[1] *= 2
                ah[2] *= 2
                ah[3] *= 2
                self.rects.append(ah)
                for answer in range(len(answers)):
                    self.display.blit(self.ui.render(answers[answer]), (30, 30 + (answer * 20)))
                    rect = self.ui.render(answers[answer]).get_rect()
                    rect[0] = 30
                    rect[1] = 30 + (answer * 20)
                    rect[0] *= 2
                    rect[1] *= 2
                    rect[2] *= 2
                    rect[3] *= 2
                    self.rects.append(rect)
            for enemy in self.obsticals:
                self.obsticals[enemy].update(self.tilemap)
                self.obsticals[enemy].render(self.display)

            self.display.blit(self.ui.render("Score:" + str(self.score)), (1, 1))
            if gamemode == 1:
                self.display.blit(self.ui.render("Health:" + str(self.player.health)), (100, 1))
            self.display.blit(self.ui.render("High Score:" + str(self.highscore)), (200, 1))

            if self.playerdistance >= self.leveldistance:
                self.display.blit(self.ui.render("Level Beat"), (100, 100))
                self.levelbeat = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    with open("data/score.txt", 'w') as f:
                        if self.score > int(self.highscore):
                            f.write(str(self.score))
                        else:
                            f.write(self.highscore)
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
                    if self.levelbeat and not self.answeringquestion:
                        self.currentlevel += 1
                        self.playerdistance = 0
                        self.levelbeat = False
                    for rect in self.rects:
                        if rect.collidepoint(self.mousepos):
                            for answer in range(len(answers)):
                                if answers[self.rects.index(rect) - 1] == self.correctAnswer:
                                    self.isCorrect = True
                                    self.score += 1

            if self.isCorrect:
                self.display.blit(self.ui.render("Correct!"), (160, 40))
            if self.switchquestion == 1:
                self.isCorrect = False

            if not self.levelbeat and not self.answeringquestion:
                self.playerdistance += 1
            self.switchquestion = 0

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

    def menu(self):
        while True:
            self.mousepos = pygame.mouse.get_pos()
            self.display.blit(self.assets['background'], (0, 0))

            rectClassic = self.ui.render("Play Classic").get_rect()
            rectComprehension = self.ui.render("Play Comprehension").get_rect()
            rectClassic[0] = ((self.display.get_width() / 2) - 100) * 2
            rectClassic[1] = 100 * 2
            rectClassic[2] *= 2
            rectClassic[3] *= 2
            rectComprehension[0] = ((self.display.get_width()/2)-100) * 2
            rectComprehension[1] = 150 * 2
            rectComprehension[2] *= 2
            rectComprehension[3] *= 2

            self.display.blit(self.ui.render("Play Classic"), ((self.display.get_width()/2)-100, 100))
            self.display.blit(self.ui.render("Play Comprehension"), ((self.display.get_width()/2)-100, 150))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if rectClassic.collidepoint(self.mousepos):
                            Game().run(1)
                        if rectComprehension.collidepoint(self.mousepos):
                            Game().run(2)

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

Game().menu()
