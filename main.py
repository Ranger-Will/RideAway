import pygame
import sys

def load_img(path):
  img = pygame.image.load(path)
  img.set_color_key((0,0,0))
  return img

class Game:
  def __init__():
    pygame.init
    pygame.display.set_caption("Ride Away")
    self.display = pygame.display.set_mode((320, 640))

    self.assests = {
      "player": load_img('bike.png')
    }

    self.clock = pygame.time.Clock()

  def run():
    while True:
      self.display.fill((0, 50, 30))

      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()


      pygame.display.update()
      self.clock.tick = 60
    
Game().run()
