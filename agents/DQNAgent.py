import numpy as np
import random
import tensorflow as tf
from collections import deque
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.initializers import Zeros
from configuration import configuration

class DQNAgent():
    
    def __init__(self, action_space):
        # Hyperparameters
        self.alpha = 0.1
        self.gamma = 0.9
        self.action_size = configuration.NUM_OF_ACTIONS
        
        #define the replay buffer
        self.replay_buffer = deque(maxlen=5000)
        
        #define the discount factor
        self.gamma = 0.9  
        
        #define the epsilon value
        self.min_epsilon = 0.1   
        self.epsilon = 0.9
        self.epsilon_decay = 0.99
        
        #define the update rate at which we want to update the target network
        self.update_rate = 5  
        
        #define the main network
        self.main_network = self.build_network()
        
        #define the target network
        self.target_network = self.build_network()
        
        #copy the weights of the main network to the target network
        # self.target_network.set_weights(self.main_network.get_weights())  

        self.path = configuration.PATH_MODEL
        
    def act(self, state):

        self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)
        print("Epsilon = {}".format(self.epsilon))

        if random.uniform(0,1) < self.epsilon:
            return np.random.randint(self.action_size)
        
        # print(state.shape)
        Q_values = self.main_network.predict(state)
        print("Q_values act = {}".format(Q_values))
        
        return np.argmax(Q_values[0])        


    def build_network(self):

        model = Sequential()
        initializer = Zeros()
        model.add(Dense(21, activation='relu', input_shape=(21,), kernel_initializer=initializer))
        model.add(Dense(32, activation='relu', kernel_initializer=initializer))        
        model.add(Dense(16, activation='relu', kernel_initializer=initializer))
        # model.add(Dense(self.action_size, activation='softmax'))
        # model.compile(loss='categorical_crossentropy', optimizer=Adam(), metrics=['accuracy'])
        model.add(Dense(self.action_size, kernel_initializer=initializer))        
        model.compile(loss='mse', optimizer=Adam(), metrics=['accuracy'])        

        return model

    #We learned that we train DQN by randomly sampling a minibatch of transitions from the
    #replay buffer. So, we define a function called store_transition which stores the transition information
    #into the replay buffer

    def store_transition(self, state, action, reward, next_state):
        self.replay_buffer.append((state, action, reward, next_state))

    
    #train the network
    def train(self, batch_size):
        
        print("Training...")

        #sample a mini batch of transition from the replay buffer
        minibatch = random.sample(self.replay_buffer, batch_size)
        
        #compute the Q value using the target network
        for state, action, reward, next_state in minibatch:
            target_Q = (reward + self.gamma * np.amax(self.target_network.predict(next_state)))
                
            #compute the Q value using the main network 
            Q_values = self.main_network.predict(state)
            # print("Q_values train = {}".format(Q_values))
            
            Q_values[0][action] = target_Q
            
            #train the main network
            self.main_network.fit(state, Q_values, epochs=1, verbose=0)
            
    #update the target network weights by copying from the main network
    def update_target_network(self):
        self.target_network.set_weights(self.main_network.get_weights())        

    def save_weights(self):
        self.main_network.save_weights(self.path)

    def load_weights(self):
        self.main_network.load_weights(self.path)