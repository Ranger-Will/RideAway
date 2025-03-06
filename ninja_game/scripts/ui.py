import pygame

class UI:
    def __init__(self, font):
        self.uifont = pygame.font.Font(font, 8)

    def render(self, info, color=(0,0,0)):
        return self.uifont.render(info, False, color)
