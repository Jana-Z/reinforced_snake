import random
import numpy as np
from .Snake import Snake
from .Fruit import Fruit

class Board():
  def __init__(self, width, height, obstacles=None):
    self.width = width
    self.height = height
    self.snake = Snake((width//2, height//2), width, height)
    self.previous_board = np.zeros((width,height))
    if not obstacles:
      self.obstacles = self._create_obstacles(width*height // 5)
    else:
      self.obstacles = obstacles
    self.fruit = Fruit(width, height, [(width//2, height//2)], self.obstacles)

  def _create_obstacles(self, n:int):
    obstacles = []
    while len(obstacles) < n:
      new_obstacle =  \
      (random.randint(0, self.height-1), random.randint(0, self.width-1))
      if new_obstacle not in obstacles:
        obstacles.append(new_obstacle)
    return obstacles

  def get_board(self):
    current_board = np.zeros((self.width, self.height))
    fruit_pos = self.fruit.get_position()
    current_board[fruit_pos] = 3
    snake_pos = self.snake.get_position()
    for i in snake_pos:
      current_board[i] = 1
    for i in self.obstacles:
      current_board[i] = -1
    current_board[snake_pos[0]] = 2
    return current_board

  def play_computer(self, action:int):
    if action < 0 or action > 3:
        print(f'Entered wrong action: {action}')
    result = self.snake.move(action, self.fruit.get_position(), self.obstacles)
    if result['eat_fruit']:
        self.fruit.be_eaten(self.snake.get_position(), self.obstacles)
    local_previous_board = self.previous_board
    self.previous_board = self.get_board()
    return (local_previous_board, self.get_board(), result['eat_fruit'], result['game_over'])

  def print_board(self):
      board = self.get_board()
      for line in board:
          print(line, sep='|')

  def play_human(self):
    self.print_board()
    while True:
      move = int(input(f'Enter your move here:\n\
        0 for up/1 for down/2 for right/3 for left'))
      result = self.snake.move(move, self.fruit.get_position(), self.obstacles)
      if result['game_over']:
        print("Game over!")
        break
      elif result['eat_fruit']:
        self.fruit.be_eaten(self.snake.get_position())
      self.print_board()