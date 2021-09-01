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
    total_reward = 0
    state = env.get_state()
    agent.epsilon = 0.99
    agent.path = 'model.' + str(configuration.MAX_NUM_PODS) + '.episodic.keras'
    
    for e in range(configuration.NUM_EPISODES):        
        # Inicializamos reward
        reward  = 0
        agent.epsilon = 0.99

        for t in range(configuration.NUM_TIMESTEPS):
            
            #update the target network
            if t % agent.update_rate == 0:
                agent.update_target_network()

            # El agente decide la siguiente accion y recoge 
            # el nuevo estado y la recompensa
            action = agent.act(state, True)
            next_state, reward = env.step(action)

            print("episode = {}, step = {}, state = {}, action = {}, reward= {}, total_reward={:.2f}".format(e, t, state, action, reward, total_reward)) 

            #store the transition information
            agent.store_transition(state, action, reward, next_state)

            state = next_state
            # agent.update_network parameters
            total_reward += reward

            if len(agent.replay_buffer) > batch_size:
                agent.train(batch_size)           

        print("Saving weights ... ")
        agent.save_weights()            