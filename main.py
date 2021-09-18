from environments.environment   import K8Senvironment
from agents.DQNAgent            import DQNAgent
from configuration              import configuration
from collections                import deque
import matplotlib.pyplot        as plt
import numpy                    as np
import datetime
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
    buffer_datetime = []  
    count = 0

    while True:  

        count += 1
        print("count = {}".format(count))

        action = agent.act(state, False)
        next_state, reward = env.step(state, action)
        total_reward += reward        
        print("state = {}, action = {}, reward= {}, total_reward={:.2f}".format(state, action, reward, total_reward))       
        time.sleep(15)
        state = next_state
        
        #number_of_pods = int(state[0][0])
        number_of_pods = sum(1 for i in state[0] if i != 0)
        cpu_usage = state[0][0:configuration.MAX_NUM_PODS]
        total_cpu_usage = np.sum(cpu_usage)
        buffer_number_of_pods.append(number_of_pods)
        buffer_total_cpu_usage.append(total_cpu_usage)    
        buffer_datetime.append(datetime.datetime.now()) 

        if count % 4 == 0:
            print("Plotting pods vs cpu")
            graph = plt.figure()
            plt.ylabel('number of pods')
            plt.xlabel('cpu usage')
            plt.yticks(range(1, configuration.MAX_NUM_PODS))
            plt.plot(buffer_total_cpu_usage,buffer_number_of_pods, 'o', color='black')
            graph.savefig('./graphs/drl/main_performance.jpg') 

            print("Plotting pods vs time")
            graph = plt.figure()
            plt.ylabel('number of pods')
            plt.xlabel('time')
            plt.yticks(range(1, configuration.MAX_NUM_PODS))
            plt.plot(buffer_datetime, buffer_number_of_pods)
            plt.gcf().autofmt_xdate()
            plotfile = "./graphs/drl/main_performance_pods_time.jpg"
            graph.savefig(plotfile)    

            print("Plotting cpu vs time")
            graph = plt.figure()
            plt.ylabel('cpu')
            plt.xlabel('time')
            plt.yticks(range(1, configuration.MAX_NUM_PODS))
            plt.plot(buffer_datetime, buffer_total_cpu_usage)
            plt.gcf().autofmt_xdate()
            plotfile = "./graphs/drl/main_performance_cpu_time.jpg"
            graph.savefig(plotfile)       
                