import numpy as np
import matplotlib.pyplot as plt
from rlAgent import AI_player
from snake import Board
import os
from collections import deque

os.environ['KMP_DUPLICATE_LIB_OK']='True'

width = 5
height = 5
obstacles = 0
num_last_frames = 4
input_dims = (1, num_last_frames, height, width)
history = {
    'fruits': [],
    'reward': [],
    'exploration': []
}
action_state = 3   # 1 - Maintain direction; 2 - turn left; 3 - turn right


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

def train_snake(
        show_pygame=False,
        episodes=60000,
        epsilon_decay=0.99995,
        epsilon=1., 
        min_epsilon=0.01,
        gamma=0.9,
        learning_rate=0.01
    ):
    ai_player = AI_player(
        action_state,
        width,
        height,
        num_last_frames,
        epsilon_decay=epsilon_decay,
        epsilon=epsilon,
        min_epsilon=min_epsilon,
        gamma=0.9,
        learning_rate=0.01
    )

    for e in range(episodes):
        board = Board(width, height, obstacles, num_last_frames=num_last_frames)

        state = deque(np.zeros((width, height)) for x in range(num_last_frames-1))
        state.appendleft(convert_to_numbers(board.get_board()))
        state = np.array(state).reshape(input_dims)

        done = False
        reward = 0
        total_reward = 0
        while not done:
            action = ai_player.act(state)
        
            previous_state, next_state, fruit_is_eaten, done, right_orientation = board.play_computer(action, show_pygame)

            if fruit_is_eaten:
                reward = 1
            if done:
                reward = -1
                unique, counts = np.unique(board.get_board(), return_counts = True)
                dictionary = dict(zip(unique, counts))
                snake_len = dictionary['s']+1 if 's' in dictionary else 1
                print(f'Episode {e}/{episodes}| Exploration {ai_player.epsilon} |  Fruits {snake_len-1} | Total reward {total_reward}')
                history['fruits'].append(snake_len-1)
                history['reward'].append(total_reward)
                history['exploration'].append(ai_player.epsilon)
            else:
                reward = +0.05 if right_orientation else -0.05
            total_reward += reward

            next_state = np.array([convert_to_numbers(s) for s in next_state]).reshape(input_dims)
            previous_state = np.array([convert_to_numbers(s) for s in previous_state]).reshape(input_dims)

            ai_player.memorize(state, action, reward, next_state, done)
            state = next_state

        ai_player.replay(400)
        if e%1000 == 0:
            ai_player.save_model('./model')
            print('saving the model...')

def plot_history():
    for label, data in history.items():
        plt.plot(np.arange(0, len(data)), data)
        plt.title(f'label: {label}')
        plt.show()

def load_show_agent(path, num_games=1):
    ai_player = AI_player(action_state, width, height, epsilon=0.3, min_epsilon=0)
    ai_player.load_model(path)
    for i in range(num_games):
        board = Board(width, height, obstacles)
        state = \
            np.concatenate((
                convert_to_numbers(board.get_board()),
                np.zeros((width,height))
            )) \
            .reshape(input_dims)
        done = False

        while not done:
            action = ai_player.act(state)
            previous_state, next_state, __, done = board.play_computer(action, True)
            next_state = convert_to_numbers(next_state)
            previous_state = convert_to_numbers(previous_state)
            next_state = np.concatenate((next_state, previous_state)) \
                .reshape(input_dims)
            state = next_state



if __name__=='__main__':
    train_snake()
    plot_history()
    load_show_agent('./model', 5)
    