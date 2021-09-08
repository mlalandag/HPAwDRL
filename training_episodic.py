# from containers import  Configs, Agents, Environments
from environments.environment   import K8Senvironment
from agents.DQNAgent            import DQNAgent
from configuration              import configuration
import matplotlib.pyplot        as plt
import numpy                    as np
import datetime

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
    agent.path = './models/model.' + str(configuration.MAX_NUM_PODS) + '.episodic.keras' 
    
    for e in range(configuration.NUM_EPISODES):        
        # Inicializamos la recompensa
        reward  = 0
        buffer_number_of_pods  = []
        buffer_total_cpu_usage = [] 
        buffer_datetime = [] 

        for t in range(configuration.NUM_TIMESTEPS):
            # Actualizamos la target network con la frecuencia deseada
            if t % agent.update_rate == 0:
                agent.update_target_network()
            # El agente decide la siguiente accion y recoge 
            # el nuevo estado y la recompensa
            action = agent.act(state, True)
            next_state, reward = env.step(action)
            
            total_reward += reward
            print("episode = {}, step = {}, state = {}, action = {}, reward= {}, next_state = {}, total_reward={:.2f}".format(e+1, t+1, state, action, reward, next_state, total_reward)) 

            #store the transition information
            # Guardamos la transición en el replay buffer
            agent.store_transition(state, action, reward, next_state)
            # Actualizamos estado con el nuevo estado
            state = next_state

            # Entrenamos el agente
            if len(agent.replay_buffer) > batch_size:
                agent.train(batch_size)

            number_of_pods = int(state[0][0])
            cpu_usage = state[0][1:configuration.MAX_NUM_PODS + 1]
            total_cpu_usage = np.sum(cpu_usage)
            buffer_number_of_pods.append(number_of_pods)
            buffer_total_cpu_usage.append(total_cpu_usage)
            buffer_datetime.append(datetime.datetime.now())

        # Salvamos los pesos del modelo al finalizar cada episodio
        print("Saving weights ... ")
        agent.save_weights()
        
        print("Plotting pods vs cpu")
        graph = plt.figure()
        plt.ylabel('number of pods')
        plt.xlabel('cpu usage')
        plt.yticks(range(1, configuration.MAX_NUM_PODS + 1))
        plt.plot(buffer_total_cpu_usage, buffer_number_of_pods, 'o', color='black')
        plotfile = "./graphs/drl/performance_train_" + str(e) + ".jpg"
        graph.savefig(plotfile)  

        print("Plotting pods vs time")
        graph = plt.figure()
        plt.ylabel('number of pods')
        plt.xlabel('time')
        plt.yticks(range(1, configuration.MAX_NUM_PODS + 1))
        plt.plot(buffer_datetime, buffer_number_of_pods)
        plt.gcf().autofmt_xdate()
        plotfile = "./graphs/drl/performance_train_pods_time_" + str(e) + ".jpg"
        graph.savefig(plotfile)    

        print("Plotting cpu vs time")
        graph = plt.figure()
        plt.ylabel('cpu')
        plt.xlabel('time')
        plt.yticks(range(1, configuration.MAX_NUM_PODS + 1))
        plt.plot(buffer_datetime, buffer_total_cpu_usage)
        plt.gcf().autofmt_xdate()
        plotfile = "./graphs/drl/performance_train_cpu_time_" + str(e) + ".jpg"
        graph.savefig(plotfile)        