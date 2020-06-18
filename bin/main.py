import numpy as np
from rlAgent import AI_player
from snake import Board

width = 5
height = 5
episodes = 2000
obstacles = [(1, 1)]
input_dim = (1, width, height, 1)

def train_snake():
    ai_player = AI_player(4, width, height, epsilon_decay=0.9995)

    snake_length = []

    for e in range(episodes):
        board = Board(width, height, obstacles)
        state = board.get_board().reshape(input_dim)
        done = False
        reward = 0
        while not done:
            action = ai_player.act(state)

            _, next_state, fruit_is_eaten, done = board.play_computer(action)
            if fruit_is_eaten:
                reward = 1
            if done:
                reward = -1
                unique, counts = np.unique(board.get_board(), return_counts = True)
                dictionary = dict(zip(unique, counts))
                snake_len = dictionary[1]+1 if 1 in dictionary else 1
                print(f'Episode {e} , snake length = {snake_len}, e = {ai_player.epsilon}')
                snake_length.append(snake_len)

            next_state = next_state.reshape(input_dim)

            ai_player.memorize(state, action, reward, next_state, done)
            state = next_state

            if e > episodes-10:
                state_reshaped = state.reshape(width, height)
                for i in state_reshaped:
                    print(i)
                print('--------')

        ai_player.replay(35)


if __name__=='__main__':
    train_snake()
