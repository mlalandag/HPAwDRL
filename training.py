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
    agent = DQNAgent(env.action_space)
    total_reward = 0
    state = env.get_state()
    
    for i in range(configuration.NUM_EPISODES):        
        # Inicializamos reward
        reward  = 0
        time_step = 0
        agent.epsilon = 0.9

        for t in range(configuration.NUM_TIMESTEPS):

            #update the time step
            time_step += 1
            
            #update the target network
            if time_step % agent.update_rate == 0:
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

            print("episode = {}, step = {}, state = {}, reward= {}, total_reward={:.2f}".format(i+1, t+1, state, reward, total_reward))      

            if len(agent.replay_buffer) > batch_size:
                agent.train(batch_size)           

        print("Saving weights ... ")
        agent.save_weights()            