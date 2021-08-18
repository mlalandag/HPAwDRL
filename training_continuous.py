# from containers import  Configs, Agents, Environments
from environments.environment  import K8Senvironment
from agents.DQNAgent           import DQNAgent
from configuration             import configuration

import time
import random

if __name__ == "__main__":

    batch_size = configuration.BATCH_SIZE
    # Creamos el entorno y el agente       
    env = K8Senvironment()
    agent = DQNAgent()
    total_reward = 0
    state = env.get_state()
    agent.epsilon = 0.99
    agent.path = 'model.' + str(configuration.MAX_NUM_PODS) + 'continuous.keras'
    count = 0
    
    while True:  

        count += 1

        #update the target network
        if count % configuration.UPDATE_RATE == 0:
            agent.update_target_network()

        # El agente decide la siguiente accion y recoge 
        # el nuevo estado y la recompensa
        action = agent.act(state)
        next_state, reward = env.step(action)

        #store the transition information
        agent.store_transition(state, action, reward, next_state)

        state = next_state
        # agent.update_network parameters
        total_reward += reward

        print("step = {}, state = {}, reward= {}, total_reward={:.2f}".format(count, state, reward, total_reward))      

        if len(agent.replay_buffer) > batch_size:
            agent.train(batch_size)           

        if count % configuration.SAVE_RATE == 0:
            print("Saving weights")
            agent.save_weights()            