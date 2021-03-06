import operator 

DIRECTIONS = [
    (-1, 0),  # north
    (0, +1),  # east
    (+1, 0),  # south
    (0, -1)   # west
]

SNAKE_MOVES = {
    0: 0,   # Maintain direction
    1: -1,  # Turn left
    2: +1   # Turn right
}

class Snake():
  def __init__(self, initial_position:tuple, board_layout):
    self.position = [initial_position]  # head -> body -> tail
    self.width = board_layout.shape[0]
    self.height = board_layout.shape[1]
    self.direction = 0  # index in DIRECTIONS_ARR

  def move(self, move:int, board_layout):
    ''' Move is a number (0, 1 or 2) where
        0 is maintain direction,
        1 is turn_left
        2 is turn_right
    '''
    new_head = self.position[0]
    self.direction = (self.direction + SNAKE_MOVES[move])%len(DIRECTIONS)
    new_head = tuple(map(operator.add,
        new_head,
        DIRECTIONS[self.direction]))
    new_head = (new_head[0]%self.height, new_head[1]%self.width)
    if self.is_move_possible(new_head, board_layout):
      if board_layout[new_head] == 'F':
        self.position = [new_head] + self.position
        return {
          'game_over': False,
          'eat_fruit': True,
        }
      else:
        if len(self.position) > 1:
          self.position = [new_head] + self.position[:-1]
        else:
          self.position = [new_head]
        return {
          'game_over': False,
          'eat_fruit': False,
        }
    else:
      return {
        'game_over': True,
        'eat_fruit': False,
      }
          
  def is_move_possible(self, new_head:tuple, board_layout):
    if board_layout[new_head] == '#' or board_layout[new_head] == 's':
        return False
    else:
        return True

  def get_position(self)->list:
    return self.position