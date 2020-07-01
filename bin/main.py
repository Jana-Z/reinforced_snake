import numpy as np
import matplotlib.pyplot as plt
from rlAgent import AI_player
from snake import Board
import os

os.environ['KMP_DUPLICATE_LIB_OK']='True'

width = 5
height = 5
episodes = 60000
obstacles = 0
input_dims = (1, 2, height, width)
history = {
    'fruits': [],
    'reward': [],
    'exploration': []
}
action_state = 3   # 1 - Maintain direction; 2 - turn left; 3 - turn right
num_last_frames = 2
# TODO make number variable

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

def train_snake(show_pygame = False):
    ai_player = AI_player(action_state, width, height, epsilon_decay=0.99995)

    for e in range(episodes):
        board = Board(width, height, obstacles)
        state = \
            np.concatenate((
                convert_to_numbers(board.get_board()),
                np.zeros((width,height))
            )) \
            .reshape(input_dims)
        done = False
        reward = 0
        total_reward = 0
        while not done:
            action = ai_player.act(state)
        
            previous_state, next_state, fruit_is_eaten, done = board.play_computer(action, show_pygame)
            if fruit_is_eaten:
                total_reward += 1
                reward = 1
            if done:
                total_reward -= 1
                reward = -1
                unique, counts = np.unique(board.get_board(), return_counts = True)
                dictionary = dict(zip(unique, counts))
                snake_len = dictionary['s']+1 if 's' in dictionary else 1
                print(f'Episode {e}/{episodes}| Exploration {ai_player.epsilon} |  Fruits {snake_len-1} | Total reward {total_reward}')
                history['fruits'].append(snake_len-1)
                history['reward'].append(total_reward)
                history['exploration'].append(ai_player.epsilon)

            next_state = convert_to_numbers(next_state) 
            previous_state = convert_to_numbers(previous_state)

            if e > episodes-10:
                state_reshaped = next_state.reshape(width, height)
                for i in state_reshaped:
                    print(i)
                print('--------')

            next_state = np.concatenate((next_state, previous_state)) \
                .reshape(input_dims)

            # next_state =  tf.transpose(
            #     np.concatenate((next_state, previous_state)).reshape(input_dims),
            #     [0, 2, 3, 1]
            # )

            ai_player.memorize(state, action, reward, next_state, done)
            state = next_state

        ai_player.replay(100)
    ai_player.save_model('./model')

def plot_history():
    for label, data in zip(history):
        plt.line(np.arange(0, len(data)), data)
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
    # train_snake()
    #plot_progress()
    load_show_agent('./model', 5)
    