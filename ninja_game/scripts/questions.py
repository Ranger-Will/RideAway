import random

import pygame

import ui

questions = {
    "What did was Jonas's full job title?": {"16", "3", "8", "1"},
    "": {"", "", "", ""},
    "": {"", "", "", ""},
    "": {"", "", "", ""},
    "": {"", "", "", ""},
    "": {"", "", "", ""},
    "": {"", "", "", ""},
    "": {"", "", "", ""},
    "": {"", "", "", ""},
    "": {"", "", "", ""},
    "": {"", "", "", ""},
    "": {"", "", "", ""},
    "": {"", "", "", ""},
    "": {"", "", "", ""},
    "": {"", "", "", ""}
}


class Question:
    def __init__(self, game):
        self.game = game
        self.list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
        self.sack = self.list
        random.shuffle(self.sack)
        self.screen = pygame.surface.Surface((320, 240))
        self.ui = ui.UI("PressStart2P-vaV7.ttf")

    def randomizeanswers(self, question):
        copied = []
        for anwers in questions[question]:
            copied.append(anwers)
        random.shuffle(copied)
        return copied
    def showquestion(self, question):
        answers = self.randomizeanswers(question)
        self.screen.blit(self.ui.render(question), (160, 50))
        self.screen.blit(self.ui.render(answers[0]), (100, 70))
        self.screen.blit(self.ui.render(answers[1]), (100, 90))
        self.screen.blit(self.ui.render(answers[2]), (100, 110))
        self.screen.blit(self.ui.render(answers[3]), (100, 130))
        return self.screen

