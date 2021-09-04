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
        # Inicializamos la recompensa
        reward  = 0

        for t in range(configuration.NUM_TIMESTEPS):
            # Actualizamos la target network con la frecuencia deseada
            if t % agent.update_rate == 0:
                agent.update_target_network()
            # El agente decide la siguiente accion y recoge 
            # el nuevo estado y la recompensa
            action = agent.act(state, True)
            next_state, reward = env.step(action)

            print("episode = {}, step = {}, state = {}, action = {}, reward= {}, total_reward={:.2f}".format(e+1, t+1, state, action, reward, total_reward)) 

            #store the transition information
            # Guardamos la transición en el replay buffer
            agent.store_transition(state, action, reward, next_state)
            # Actualizamos estado con el nuevo estado
            state = next_state
            total_reward += reward

            # Entrenamos el agente
            if len(agent.replay_buffer) > batch_size:
                agent.train(batch_size)           

        # Salvamos los pesos del modelo al finalizar cada episodio
        print("Saving weights ... ")
        agent.save_weights()            