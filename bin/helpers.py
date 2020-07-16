from collections import deque
import numpy as np
import matplotlib.pyplot as plt

from rlAgent import AI_player
from snake import Board

def load_show_agent(path, board, num_games=1):
    ''' Loads the model situated at path and shows num_games pygame plots
        on how the rl agent plays snake.
        Only works on mac.
    '''
    input_dims = (1, board.get_num_last_frames(), *board.get_dims()) 
    ai_player = AI_player(board.get_dims(), board.get_action_size(), board.get_num_last_frames(), epsilon=0, min_epsilon=0)
    ai_player.load_model(path)
    for i in range(num_games):
        state = deque(np.zeros(board.get_dims()) for x in range(board.get_num_last_frames()-1))
        state.appendleft(convert_to_numbers(board.get_board()))
        state = np.array(state).reshape(input_dims)
        done = False

        while not done:
            action = ai_player.act(state)
            next_state, _, done, __ = board.play_computer(action, True)
            next_state = np.array([convert_to_numbers(s) for s in next_state]).reshape(input_dims)
            state = next_state

def plot_history(history:dict):
    for label, data in history.items():
        plt.plot(np.arange(0, len(data)), data)
        plt.title(f'label: {label}')
        plt.show()

def convert_to_numbers(arr):
    converted_arr = []
    map_symbol = {
        '.': 0.,
        '#': 4.,
        's': 3.,
        'S': 2.,
        'F': 1.
    }
    for line in arr:
        converted_arr.append([
            map_symbol[x] for x in line
        ])
    return np.array(converted_arr)