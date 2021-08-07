from environments.pods_cpu_mem import K8Sstate
from configuration import configuration
import numpy as np
import datetime

class K8Senvironment():
    
    def __init__(self):
        self.observation_space_n = 99999999
        self.action_space_n = configuration.NUM_OF_ACTIONS
        self.action_space   = [0,1,2]
    
    
    def step(self, action):

        reward, done = 0, False
    
        if action == 1:         # if action is 1, add Pod
            self.add_pod()
            reward += self.calculate_reward()

        if action == 2:         # if action is 2, remove Pod 
            self.remove_pod()
            reward += self.calculate_reward()      

        # retrieving the state vector
        k8sState = K8Sstate()        
        self.state = k8sState.get_state()

        return self.state, reward

    
    def calculate_reward(self):
        # calculate reward after action
        pass

    
    def add_pod(self):
        # add pod with scale-cluster.py
        pass        

    
    def remove_pod(self):
        # add pod with scale-cluster.py
        pass 

    def get_state(self):
        k8sState = K8Sstate()        
        self.state = k8sState.get_state()