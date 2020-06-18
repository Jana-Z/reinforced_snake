class Snake():
  def __init__(self, initial_position:tuple, width:int, height:int):
    self.position = [initial_position]  # head -> body -> tail
    self.width = width
    self.height = height

  def move(self, direction:int, fruit_position:tuple, obstacles:list):
    new_head = self.position[0]
    if direction == 3:  # left
      new_head = new_head[0], (new_head[1]-1)%self.width
    if direction == 2:  # right
      new_head = new_head[0], (new_head[1]+1)%self.width
    if direction == 0:  # up
      new_head = (new_head[0]-1)%self.height, new_head[1]
    if direction == 1:  # down
      new_head = (new_head[0]+1)%self.height, new_head[1]

    if self.is_move_possible(new_head, obstacles):
      if new_head == fruit_position:
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
          
  def is_move_possible(self, new_head:tuple, obstacles:list):
    if new_head in self.position or new_head in obstacles:
      return False
    else:
      return True

  def get_position(self)->list:
    return self.position