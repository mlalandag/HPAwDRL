# from containers import  Configs, Agents, Environments
from environments.environment  import K8Senvironment
from agents.DQNAgent           import DQNAgent
from configuration             import configuration

import time
import random

if __name__ == "__main__":


    # Creamos el entorno y el agente       
    env = K8Senvironment()
    agent = DQNAgent(configuration.ALPHA, configuration.GAMMA, configuration.MAX_NUM_PODS,
                           configuration.MIN_EPSILON, configuration.EPSILON, configuration.EPSILON_DECAY)
    agent.path = 'model.5.1.continuous.keras'
    agent.load_weights()
    total_reward = 0
    reward  = 0
    state = env.get_state()

    while True:        

        # El agente decide la siguiente accion y recoge 
        # el nuevo estado y la recompensa
        action = agent.act(state, False)
        next_state, reward = env.step(action)

        state = next_state
        # agent.update_network parameters
        total_reward += reward

        print("state = {}, reward= {}, total_reward={:.2f}".format(state, reward, total_reward))             

        time.sleep(30)                