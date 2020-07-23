import os
from collections import deque
import numpy as np
import csv

from rlAgent import AI_player
from snake import Board
from helpers import load_show_agent, \
    plot_history, convert_to_numbers

# Needed for pygame on mac
os.environ['KMP_DUPLICATE_LIB_OK']='True'

# Defining the board
WIDTH = 5
HEIGHT = 5
OBSTACLES = 0   # Number of randomly placed obstacles

BOARD = Board(WIDTH, HEIGHT, OBSTACLES)

def train_snake(
        show_pygame=False,
        num_last_frames=1,
        episodes=60000,
        epsilon_phase_size=0.5,
        epsilon=1.,
        min_epsilon=0.01,
        gamma=0.9,
        learning_rate=0.01,
    ):
    ''' Trains an Rl agent to play snake with the given parameters.
    Params:
        show_pygame:    the game is being plotted as a pygame (only mac)
        num_last_frames: defines the number of how many frames should be 
            in one state
        epsilon phase size:    percentage of the training process 
                at which exploration rate should reach its minimum 
    
    Returns:
        history:        a record of the training
    '''

    history = {
        'fruits': [],
        'reward': [],
        'exploration': []
    }

    input_dims = (1, num_last_frames, HEIGHT, WIDTH) 
    BOARD.set_num_last_frames(num_last_frames)
    ai_player = AI_player(
        BOARD.get_dims(),
        BOARD.get_action_size(),
        num_last_frames,
        epsilon=epsilon,
        min_epsilon=min_epsilon,
        gamma=0.9,
        learning_rate=0.01,
        epsilon_decay= ((epsilon - min_epsilon) / (episodes * epsilon_phase_size))
    )

    for e in range(episodes):
        state = deque(np.zeros((WIDTH, HEIGHT)) for x in range(num_last_frames-1))
        state.appendleft(convert_to_numbers(BOARD.get_board()))
        state = np.array(state).reshape(input_dims)

        done = False
        reward = 0
        # total_reward = 0

        while not done:

            action = ai_player.act(state)
            next_state, fruit_is_eaten, done, headed_towards_fruit = BOARD.play_computer(action, show_pygame)
            
            if fruit_is_eaten:
                reward += 1    
            if done:
                unique, counts = np.unique(BOARD.get_board(), return_counts=True)
                dictionary = dict(zip(unique, counts))
                snake_len = dictionary['s'] + 1 if 's' in dictionary else 1
                print(f'Episode {e}/{episodes}| Exploration {ai_player.epsilon} |  Fruits {snake_len-1} | Total reward {reward}')
                history['fruits'].append(snake_len-1)
                history['reward'].append(reward)
                history['exploration'].append(ai_player.epsilon)

                reward += -1
            else:
                reward = reward+0.05 if headed_towards_fruit else reward-0.05

            # total_reward = reward

            next_state = np.array([convert_to_numbers(s) for s in next_state])\
                .reshape(input_dims)
            ai_player.memorize(state, action, reward, next_state, done)
            state = next_state

        BOARD.wipe_game()
        # Retrain the snake using older states
        ai_player.replay(400)

        # Save every 1000 episodes
        if e%10 == 0:
            ai_player.save_model('./model')
            print('saving the model...')
            print('saving the history to csv file...')
            with open('./hist.csv', 'w') as f:
                w = csv.DictWriter(f, history.keys())
                w.writeheader()
                w.writerow(history)


    return history

if __name__=='__main__':

    hist = train_snake(show_pygame=False, episodes=20000, num_last_frames=4)
    plot_history(hist)
    # BOARD.set_num_last_frames(1)
    load_show_agent('./model', BOARD, 5)