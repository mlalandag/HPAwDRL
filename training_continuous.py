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
    agent = DQNAgent(configuration.ALPHA, configuration.GAMMA, configuration.MAX_NUM_PODS,
                           configuration.MIN_EPSILON, configuration.EPSILON, configuration.EPSILON_DECAY)
    #agent.path = 'model.5.1.continuous.keras'
    #agent.load_weights()
    total_reward = 0
    state = env.get_state()
    agent.epsilon = 0.99
    agent.path = 'model.' + str(configuration.MAX_NUM_PODS) + '.continuous.keras'
    count = 0
    
    while True:  

        count += 1

        #update the target network
        if count % configuration.UPDATE_RATE == 0:
            agent.update_target_network()

        # El agente decide la siguiente accion y recoge 
        # el nuevo estado y la recompensa
        action = agent.act(state, True)
        next_state, reward = env.step(action)

        print("step = {}, state = {}, action = {}, reward= {}, total_reward={:.2f}".format(count, state, action, reward, total_reward)) 

        #store the transition information
        agent.store_transition(state, action, reward, next_state)

        state = next_state
        total_reward += reward     

        if len(agent.replay_buffer) > batch_size:
            agent.train(batch_size)           

        if count % configuration.SAVE_RATE == 0:
            print("Saving weights")
            agent.save_weights()            