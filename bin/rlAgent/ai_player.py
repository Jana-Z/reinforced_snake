import random
from collections import deque
import numpy as np
import tensorflow as tf
import keras
from keras.models import Sequential
from keras.layers import Conv2D, Dense, Flatten, LeakyReLU
from keras.optimizers import Adam, RMSprop

class AI_player():
  def __init__(self,
        dims:tuple,
        action_size:int,
        num_last_frames:int,
        epsilon=1., 
        min_epsilon=0.01,
        epsilon_decay=0.8,
        gamma=0.9,
        learning_rate=0.01
    ):

    self.width, self.height = dims
    self.action_size = action_size  # = 3
    self.num_last_frames = num_last_frames
    self.epsilon = epsilon
    self.min_epsilon = min_epsilon
    self.epsilon_decay = epsilon_decay
    self.gamma = gamma
    self.learning_rate = learning_rate
    self.model = self._build_model()
    self.memory = deque(maxlen=10000)

  def _build_model(self): 
    ''' Initialise the model using self.learning_rate and 
    self.state_size as input dimension, self.action_size as output dimension
    '''
    model = Sequential()

    # Convolutional layers
    model.add(Conv2D(
        10,
        kernel_size=(3, 3),
        strides=(1, 1),
        input_shape=(self.num_last_frames, self.width, self.height), 
        # activation='relu',
        data_format='channels_first'
    ))
    model.add(LeakyReLU(alpha=0.1))
    # model.add(Conv2D(
    #     20,
    #     kernel_size=(3, 3),
    #     strides=(1, 1),
    #     # activation='relu',
    #     data_format='channels_first'
    # ))
    # model.add(LeakyReLU(alpha=0.1))

    # Dense layers
    model.add(Flatten())
    model.add(Dense(100))
    model.add(LeakyReLU(alpha=0.1))
    model.add(Dense(self.action_size))

    model.summary()
    model.compile(RMSprop(), 'MSE')
    # model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate))

    return model

  def memorize(self, state, action, reward, next_state, done):
    ''' Push the state, action, reward, next_state and done into the memory.
    Used for replay later.
    '''
    self.memory.append((state, action, reward, next_state, done))

  def act(self, state):
    ''' Choose one integer between 0 and the action state.
    By a chance of epsilon the move is going to be random or 
    is going to be chosen by the NN
    '''
    if np.random.rand() < self.epsilon:
      move = np.random.randint(0, self.action_size)
    else:
      move = np.argmax(self.model.predict(state)[0])
      # print(state)
      # print(self.model.predict(state))
      # print(move)
      # print('-------------')

    return move

  def save_model(self, path):
    ''' Saves self.model at the given path.
    Checks whether saving worked using one sample.
    '''
    self.model.save(path)
    minibatch = np.array(random.sample(self.memory, 1)[0][0])
    self.check_model(path, minibatch)

  def load_model(self, path):
    ''' Sets self.model to a model at the given path.
    '''
    self.model = keras.models.load_model(path)

  def check_model(self, path, test_input):
    ''' Compares self.model and the model at the given path.
    Checks for equal predictions.
    '''
    loaded_model = keras.models.load_model(path)
    np.testing.assert_allclose(
      loaded_model.predict(test_input),
      self.model.predict(test_input)
    )
    print('model is ok')

  def replay(self, batch_size):
    ''' Replay states of the memory as specified in batch_size
    '''
    if batch_size > len(self.memory):
      batch_size = len(self.memory)
    minibatch = random.sample(self.memory, batch_size)
    for state, action, reward, next_state, done in minibatch:
      if done:
        target = reward
      else:
        input_data = np.array(next_state)
        target = reward + self.gamma * np.amax(self.model.predict(input_data)[0])

      target_f = self.model.predict(state)
      target_f[0][action] = target

      self.model.fit(state, target_f, epochs=1, verbose=False)
    
    if self.epsilon > self.min_epsilon:
      self.epsilon -= self.epsilon_decay
