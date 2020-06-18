import random

class Fruit():
  def __init__(self, width, height, snake_position, obstacles):
    self.max_width = width
    self.max_height = height
    self.position = (0, 0)
    self.be_eaten(snake_position, obstacles)

  def be_eaten(self, snake_position, obstacles):
    while True:
      self.position = (random.randint(0, self.max_width-1), random.randint(0, self.max_height-1))
      if self.position not in snake_position and self.position not in obstacles:
        break

  def get_position(self):
    return self.position