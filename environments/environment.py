from environments.pods_cpu_mem  import K8Sstate
from config import *
import numpy as np
import datetime

class K8Senvironment():
    
    def __init__(self):
        self.observation_space_n = 99999999
        self.action_space_n = NUM_OF_ACTIONS
        self.action_space   = [0,1,2]
        self.state          = K8Sstate.get_state()    
    
    
    def step(self, action):

        reward, done = 0, False
    
        if action == 1:         # if action is 1, add Pod
            self.add_pod()
            reward += self.calculate_reward()

        if action == 2:         # if action is 2, remove Pod 
            self.remove_pod()
            reward += self.calculate_reward()      

        # creating the state vector
        self.state = K8Sstate.get_state()

        return self.state, reward, done, self.info

    
    def calculate_reward(self):
        # calculate reward after action
        pass

    
    def add_pod(self):
        # add pod with scale-cluster.py
        pass        

    
    def remove_pod(self):
        # add pod with scale-cluster.py
        pass            