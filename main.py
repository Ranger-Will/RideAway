import pygame
import sys

class Game:
  def __init__():
    pygame.init
    pygame.display.set_caption("Ride Away")
    display = pygame.display.set_mode((320, 640))
    clock = pygame.time.Clock()

  def run():
    while True:

      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()


      pygame.display.update()
      clock.tick = 60
    
Game().run()
