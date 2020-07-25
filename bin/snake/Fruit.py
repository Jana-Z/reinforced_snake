import random

class Fruit():
  def __init__(self, board_layout):
    self.position = (0, 0)
    self.be_eaten(board_layout)

  def be_eaten(self, board_layout):
    while True:
      self.position = (random.randint(0, board_layout.shape[0]-1), random.randint(0, board_layout.shape[1]-1))
      if board_layout[self.position] == '.':   # Tile is unoccupied
        break

  def get_position(self):
    return self.position