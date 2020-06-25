from collections import deque
import random
import numpy as np
import tensorflow as tf
import keras
from keras.models import Sequential
from keras.layers import Conv2D, Dense, Flatten
from keras.optimizers import Adam

class AI_player():
  def __init__(self,
        action_size:int,
        width:int,
        height:int,
        epsilon=1., 
        min_epsilon=0.01,
        epsilon_decay=0.995,
        gamma=0.9,
        learning_rate=0.01
    ):
    self.width = width
    self.height = height
    self.action_size = action_size
    self.epsilon = epsilon
    self.min_epsilon = min_epsilon
    self.epsilon_decay = epsilon_decay
    self.gamma = gamma
    self.learning_rate = learning_rate
    self.model = self._build_model()
    self.memory = deque(maxlen=10000)

  def _build_model(self): 
    ''' initialise the model using self.learning_rate and 
    self.state_size as input dimension, self.action_size as output dimension
    '''
    model = Sequential()
    # model.add(Dense(24, input_shape = (self.width*self.height,), activation='relu'))
    # model.add(Dense(24, activation='relu'))
    # model.add(Dense(self.action_size, activation='softmax'))
    # model.compile(loss='mse',optimizer=Adam(lr=self.learning_rate))

    model.add(Conv2D(
        16,
        kernel_size=(3, 3),
        strides=(1, 1),
        input_shape=(2, self.width, self.height), 
        activation='relu',
        data_format='channels_first'
    ))
    model.add(Conv2D(
        32,
        kernel_size=(3, 3),
        strides=(1, 1),
        activation='relu',
        data_format='channels_first'
    ))

    # Dense layers.
    model.add(Flatten())
    model.add(Dense(256, activation='relu'))
    model.add(Dense(self.action_size, activation='relu'))

    model.summary()
    model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate))

    return model

  def memorize(self, state, action, reward, next_state, done):
    ''' push the state, action, reward, next_state and done into the memory.
    Used for replay later.
    '''
    self.memory.append((state, action, reward, next_state, done))

  def act(self, state):
    ''' Choose one integer between 0 and the action state.
    By a chance of epsilon the move is going to be random or 
    is going to be chosen by the NN
    '''
    if np.random.rand() < self.epsilon:
      return np.random.randint(0, self.action_size-1)
    else:
      recommended_move = np.argmax(self.model.predict(state)[0])
      return recommended_move

  def save_model(self, path):
    self.model.save(path)
    minibatch = np.array(random.sample(self.memory, 1)[0][0])
    self.check_model(path,minibatch)

  def load_model(self, path):
    self.model = keras.models.load_model(path)

  def check_model(self, path, test_input):
    loaded_model = keras.models.load_model(path)
    np.testing.assert_allclose(loaded_model.predict(test_input), self.model.predict(test_input))
    print('model is ok')

  def replay(self, batch_size):
    ''' Replay states of the memory as specified in batch_size.
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
      self.epsilon *= self.epsilon_decay
