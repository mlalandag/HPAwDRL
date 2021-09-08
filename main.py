from environments.environment   import K8Senvironment
from agents.DQNAgent            import DQNAgent
from configuration              import configuration
from collections                import deque
import matplotlib.pyplot        as plt
import numpy                    as np

import time
import random

if __name__ == "__main__":

    # Creamos el entorno y el agente       
    env = K8Senvironment()
    agent = DQNAgent(configuration.ALPHA, configuration.GAMMA, configuration.MAX_NUM_PODS,
                           configuration.MIN_EPSILON, configuration.EPSILON, configuration.EPSILON_DECAY)
    # Cargamos el modelo
    agent.path = './models/model.5.episodic.keras'
    agent.load_weights()
    total_reward = 0
    reward  = 0
    state = env.get_state()
    buffer_number_of_pods  = []
    buffer_total_cpu_usage = []    
    count = 0

    while True:  

        count += 1
        print("count = {}".format(count))

        action = agent.act(state, False)
        next_state, reward = env.step(action)
        total_reward += reward        
        print("state = {}, action = {}, reward= {}, total_reward={:.2f}".format(state, action, reward, total_reward))       
        time.sleep(30)
        state = env.get_state()
        
        number_of_pods = int(state[0][0])
        cpu_usage = state[0][1:configuration.MAX_NUM_PODS + 1]
        print("cpu_usage = {}".format(cpu_usage))
        total_cpu_usage = np.sum(cpu_usage)
        print("total_cpu_usage = {}".format(total_cpu_usage))
        buffer_number_of_pods.append(number_of_pods)
        buffer_total_cpu_usage.append(total_cpu_usage)     

        if count % 3 == 0:
            print("Plotting")
            graph = plt.figure()
            plt.ylabel('number of pods')
            plt.xlabel('cpu usage')
            plt.yticks(range(1, configuration.MAX_NUM_PODS + 1))
            plt.plot(buffer_total_cpu_usage,buffer_number_of_pods, 'o', color='black')
            graph.savefig('./graphs/dlr/performance.jpg')   
                