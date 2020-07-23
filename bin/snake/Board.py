import random
from collections import deque
import numpy as np
import pygame

from .Snake import Snake
from .Fruit import Fruit

WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)
BLOCK_PIXELS = 20

class Board():
  def __init__(self, width, height, obstacles=None, num_last_frames=4):
    self.width = width
    self.height = height
    self.obstacles = obstacles
    self.num_last_frames = num_last_frames
    self.previous_frames = deque(np.full((width, height), '.') for x in range(num_last_frames))
    self.game_started = False
    self.fruit = Fruit(width, height, [(width//2, height//2)], self.obstacles)
    self.snake = Snake((width//2, height//2), width, height)
    self.dst = self.calculate_dst()

  def set_num_last_frames(self, num_last_frames):
    # Wipes all previous_frames
    self.num_last_frames = num_last_frames
    self.previous_frames = deque(np.full((self.width, self.height), '.') for x in range(num_last_frames))

  def get_dims(self):
    return self.width, self.height

  def get_num_last_frames(self):
    return self.num_last_frames

  def get_action_size(self):
    return 3  # 1 - Maintain direction; 2 - turn left; 3 - turn right

  def get_board(self):
    current_board = np.full((self.width, self.height), '.')
    fruit_pos = self.fruit.get_position()
    current_board[fruit_pos] = 'F'
    snake_pos = self.snake.get_position()
    for i in snake_pos:
      current_board[i] = 's'
    if self.obstacles:
      for i in self.obstacles:
        current_board[i] = '#'
    current_board[snake_pos[0]] = 'S'
    return current_board

  def wipe_game(self):
    self.previous_frames = deque(np.full((self.width, self.height), '.') for x in range(self.num_last_frames))
    self.game_started = False
    self.fruit = Fruit(self.width, self.height, [(self.width//2, self.height//2)], self.obstacles)
    self.snake = Snake((self.width//2, self.height//2), self.width, self.height)
    self.dst = self.calculate_dst()
    
  def _create_obstacles(self, n:int):
    obstacles = []
    while len(obstacles) < n:
      new_obstacle =  \
        (random.randint(0, self.height), random.randint(0, self.width))
      if new_obstacle not in obstacles:
        obstacles.append(new_obstacle)
    return obstacles

  def render_pygame(self):
    if not self.game_started:
      self.game_started = True
      pygame.init()
      self.score_font = pygame.font.SysFont("arialttf", 35)
      flags = pygame.DOUBLEBUF | pygame.HWSURFACE
      self.dis = pygame.display.set_mode((self.width*BLOCK_PIXELS, self.height*BLOCK_PIXELS), flags)
      self.dis.set_alpha(None)
      pygame.display.set_caption('Snake Game by Rita and Jana')
      pygame.event.pump()
      events = pygame.event.get()

    pygame.event.pump()
    events = pygame.event.get()
    self.dis.fill(WHITE)
    pygame.display.set_caption(str(self.dst))
    fruit_position = self.fruit.get_position()
    pygame.draw.rect(
      self.dis, RED, 
      [fruit_position[0]*BLOCK_PIXELS, fruit_position[1]*BLOCK_PIXELS, BLOCK_PIXELS, BLOCK_PIXELS]
    )
    for pos in self.snake.get_position():
      pygame.draw.rect(
        self.dis,
        BLACK,
        [pos[0]*BLOCK_PIXELS, pos[1]*BLOCK_PIXELS, BLOCK_PIXELS, BLOCK_PIXELS]
      )
    pygame.draw.rect(
      self.dis, GREEN, 
      [self.snake.get_position()[0][0]*BLOCK_PIXELS, self.snake.get_position()[0][1]*BLOCK_PIXELS, BLOCK_PIXELS, BLOCK_PIXELS]
    )

    pygame.display.update()
    pygame.time.wait(1000)

  def play_computer(self, action:int, showPygame=False):
    if action < 0 or action > 2:
        print(f'Entered wrong action: {action}')
        return

    # Show score, fruit and snake before move
    if showPygame and not self.game_started:
      self.render_pygame()

    result = self.snake.move(action, self.fruit.get_position(), self.obstacles)
    if result['eat_fruit']:
        self.fruit.be_eaten(self.snake.get_position(), self.obstacles)

    self.previous_frames.popleft()
    self.previous_frames.append(self.get_board())

    # check whether snake moves towards the fruit
    dst = self.calculate_dst()
    headed_towards_fruit = dst < self.dst  # check whether distance now is smaller than before
    self.dst = dst

     # Show score, fruit and snake after move
    if showPygame:
      if result['game_over']:
        pygame.quit()
      else:
        self.render_pygame()

    return self.previous_frames, result['eat_fruit'], result['game_over'], headed_towards_fruit

  def calculate_dst(self):
    '''calculating the distance between the head of the snake
    and the position of the fruit.
    used to give a reward in ../main.py
    '''
    fruit_pos = self.fruit.get_position()
    snake_head_pos = self.snake.get_position()[0]
    dst_fruit_snake = np.sqrt(
      ((fruit_pos[0] - snake_head_pos[0])**2)
      + ((fruit_pos[1] - snake_head_pos[1])**2)
    )
    return dst_fruit_snake

  def print_board(self):
      board = self.get_board()
      for line in board:
          print(line, sep='|')

  # NOT WORKING PROPERLY
  def play_human(self):
    self.print_board()
    while True:
      move = int(input(f'Enter your move here:\n\
        0 for maintain direction/1 for turn left/2 for turn right'))
      if 0 <= move <= 2:
        result = self.snake.move(move, self.fruit.get_position(), self.obstacles)
        if result['game_over']:
          print("Game over!")
          break
        elif result['eat_fruit']:
          self.fruit.be_eaten(self.snake.get_position(), self.obstacles)
        self.print_board()