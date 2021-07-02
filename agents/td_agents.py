import numpy as np
import random

class TdAgent():
    
    def __init__(self):
        pass
        
    def act(self, observation, reward, done):

        pass


class SarsaAgent():
    
    def __init__(self):
        pass
        
    def act(self, observation, reward, done):

        pass       


class QLearningAgent():
    
    def __init__(self, state_space_n, action_space, action_space_n):
        # Hyperparameters
        self.alpha = 0.1
        self.gamma = 0.6
        self.epsilon = 0.1
        self.action_space = action_space
        self.q_table = np.zeros([state_space_n, action_space_n])
        
    def act(self, state, reward, done):

        if random.uniform(0, 1) < self.epsilon:
            action = random.choice([0,1,2])                              # Explore action space
        else:
            action = np.argmax(self.q_table[self.state_to_index(state)]) # Exploit learned values 

        return action

    def update_q_table(self, old_state, new_state, action, reward):

        old_value = self.q_table[self.state_to_index(old_state), action]
        next_max = np.max(self.q_table[self.state_to_index(new_state)])
        new_value = (1 - self.alpha) * old_value + self.alpha * (reward + self.gamma * next_max)
        self.q_table[self.state_to_index(old_state), action] = new_value

    def state_to_index(self, state):
        s = [str(i).zfill(2) for i in state] 
        return int("".join(s))



class DeepQLearningAgent():
    
    def __init__(self):
        pass
        
    def act(self, observation, reward, done):

        pass                