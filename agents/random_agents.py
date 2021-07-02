import random

class RandomAgent():
    
    def __init__(self):
        pass
        
    def act(self, observation, reward, done):

        return random.choice([0,1,2])