import pygame

class UI:
    def __init__(self, font):
        self.uifont = pygame.font.Font(font, 8)

    def render(self, info):
        return self.uifont.render(info, False, (0,0,0))
