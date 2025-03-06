import random

import pygame

questions = {
    "What did was Jonas's full job title?": {"Receiver of Memories", "Receiver of Kittens", "The Giver",
                                          "The Receiver-in-training"},
    "What was the first color Jonas saw?": {"Blue", "Red", "Yellow", "Dark orange"},
    "How many kids were in an average age group?": {"50", "25", "33", "100"},
    "Where are all the records of private cerimonies?": {"Hall of Open Records", "Hall of Closed Records",
                                                         "Department of Bicylce Repairs", "Elsewhere"},
    "How many Recivers have there been?": {"15", "50", "3", "Too many to count"},
    "How did Jonas escape?": {"on foot", "on his bike", "on his father's bike", "on his mother's bike"},
    "Where did his father inject the baby?": {"it's arm", "it's forehead", "it's stomach", "it's leg"},
    "What did Gabriel mistake for a plane?": {"a deer", "a bird", " a snake", "an insect"},
    "How long before the Ceremony was Jonas supposed to escape?": {"The night before", "a month before",
                                                                   "3 days before", "during the ceremony"},
    "How far into Rosemary's training was she released": {"5 weeks", "7 days", " a year", "3 weeks"},
    "Children get their assingments at 12": {"True", "False"},
    "Jonas was allowed to lie": {"True", "False"},
    "Lily's comfort object was a snake": {"False","True"},
    "": {"Yes", "No"},
    "": {"Yes", "No"}
}

class Question:
    def __init__(self):
        self.screen = pygame.surface.Surface((320, 240))
        self.rects = []

    def randomizeanswers(self, question):
        copied = []
        for anwers in questions[question]:
            copied.append(anwers)
        random.shuffle(copied)
        return copied

    def showquestion(self, question, game):

        answers = self.randomizeanswers(question)
        game.display.blit(game.ui.render(question).get_rect, (160, 50))
        ah = game.ui.render(question).get_rect#, (160, 50)
        ah[0] = 160
        ah[1] = 50
        ah[0] *= 2
        ah[1] *= 2
        ah[2] *= 2
        ah[3] *= 2
        self.rects.append(ah)
        for answer in answers:
            game.display.blit(game.ui.render(answer), (80, 70 + (answer * 20)))
            rect = game.ui.render(answer).get_rect()
            rect[0] = 80
            rect[1] = 70 + (answer*20)
            rect[0] *= 2
            rect[1] *= 2
            rect[2] *= 2
            rect[3] *= 2
            self.rects.append(rect)

        return self.rects
    