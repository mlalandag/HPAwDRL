# from containers import  Configs, Agents, Environments
from environments.environment import K8Senvironment
from agents.DQNAgent          import DQNAgent
from config                   import NUM_EPISODES

import time
import random

if __name__ == "__main__":

    # Creamos el entorno y el agente       
    env = K8Senvironment()
    agent = DQNAgent(env.action_space)
    total_reward = 0

    for i in range(NUM_EPISODES):        
        # Inicializamos state, reward y done
        reward  = 0
        done    = False            
        past_num_tasks = 0
    

        while not done:

            # El agente decide la siguiente accion y recoge 
            # el nuevo estado y la recompensa
            action = agent.act(state, reward, done)
            next_state, reward, done, info = env.step(action)
            # agent.update_network parameters
            total_reward += reward
            state = next_state     
            print("state = {}, reward= {}, done = {}, total_reward={:.2f}".format(state, reward, done, total_reward))              