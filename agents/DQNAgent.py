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
    
    def __init__(self, alpha, gamma, action_size, min_epsilon, epsilon, epsilon_decay):

        # Hyperparameters
        self.alpha = alpha
        self.gamma = gamma
        self.action_size = action_size
        self.min_epsilon = min_epsilon   
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay

        #define the replay buffer
        self.replay_buffer = deque(maxlen=5000)
        
        #define the update rate at which we want to update the target network
        self.update_rate = configuration.UPDATE_RATE  
        
        #define the main network
        self.main_network = self.build_network()
        
        #define the target network
        self.target_network = self.build_network()
        
        #copy the weights of the main network to the target network
        # self.target_network.set_weights(self.main_network.get_weights())  

        self.path = configuration.PATH_MODEL
        
    def act(self, state, train):

        if train:
            self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)
            print("Epsilon = {}".format(self.epsilon))

            if random.uniform(0,1) < self.epsilon:
                return np.random.randint(self.action_size) + 1
        
        # print(state.shape)
        Q_values = self.main_network.predict(state)
        # print("Action = {}, Q_values = {}".format(np.argmax(Q_values[0]) + 1, Q_values))
        
        return np.argmax(Q_values[0]) + 1      


    def build_network(self):

        model = Sequential()
        # initializer = Zeros()
        model.add(Dense(21, activation='relu', input_shape=(configuration.MAX_NUM_PODS + 1,), kernel_initializer='glorot_uniform'))
        model.add(Dense(32, activation='relu', kernel_initializer='glorot_uniform'))        
        model.add(Dense(16, activation='relu', kernel_initializer='glorot_uniform'))
        # model.add(Dense(self.action_size, activation='softmax'))
        # model.compile(loss='categorical_crossentropy', optimizer=Adam(), metrics=['accuracy'])
        model.add(Dense(self.action_size, kernel_initializer='glorot_uniform'))        
        model.compile(loss='mse', optimizer=Adam(), metrics=['accuracy'])        

        return model


    def store_transition(self, state, action, reward, next_state):
        self.replay_buffer.append((state, action, reward, next_state))

    
    #train the network
    def train(self, batch_size):
        
        print("Training")

        #sample a mini batch of transition from the replay buffer
        minibatch = random.sample(self.replay_buffer, batch_size)
        
        #compute the Q value using the target network
        for state, action, reward, next_state in minibatch:
            target_Q = (reward + self.gamma * np.amax(self.target_network.predict(next_state)))
            # print("target_Q >> " + str(target_Q))
                
            #compute the Q value using the main network 
            Q_values = self.main_network.predict(state)
            # print("Q_values train = {}".format(Q_values))
            # print("Q_values >> " + str(Q_values))
            
            Q_values[0][action - 1] = target_Q
            
            #train the main network
            self.main_network.fit(state, Q_values, epochs=1, verbose=0)
            
    #update the target network weights by copying from the main network
    def update_target_network(self):
        print("Updating target weights")
        self.target_network.set_weights(self.main_network.get_weights())        

    def save_weights(self):
        self.main_network.save_weights(self.path)

    def load_weights(self):
        self.main_network.load_weights(self.path)