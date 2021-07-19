import numpy as np
import random

class DQNAgent():
    
    def __init__(self, action_space):
        # Hyperparameters
        self.alpha = 0.1
        self.gamma = 0.9
        self.epsilon = 0.1
        self.action_space = action_space
        # self.network = ???
        
    def act(self, observation, reward, done):

        if random.uniform(0, 1) < self.epsilon:
            action = random.choice([0,1,2])                              # Explore action space
        else:
            action = np.argmax(self.q_table[self.state_to_index(state)]) # Exploit learned values 

        return action              