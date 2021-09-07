from configuration import configuration
import numpy as np
import datetime
import time
import sys
import os
import re
from kubernetes import client, config
from environments import rewards

class K8Senvironment():
    
    def __init__(self):
        config.load_kube_config()
        self.api = client.CustomObjectsApi()
    
    def step(self, action):

        state  = self.get_state()
        self.set_replicas(action)
        time.sleep(5)                   
        new_state  = self.get_state()
        reward = self.calculate_reward(state, action)

        return new_state, reward    

    def calculate_reward(self, state, action):
        # calculate reward after action
        reward = 0
        
        number_of_pods = int(state[0])
        if number_of_pods > configuration.MAX_NUM_PODS:
            number_of_pods = configuration.MAX_NUM_PODS   
        pods_high_cpu = 0
        pods_medium_cpu = 0
        pods_low_cpu = 0
        pods_not_spawned = configuration.MAX_NUM_PODS - number_of_pods
        
        # for i in range(number_of_pods):
        #     if state[i+1] > 300:
        #         pods_high_cpu += 1    
        #     elif state[i+1] < 100:
        #         pods_low_cpu += 1
        #     else:
        #         pods_medium_cpu += 1

        for cpu_usage in state[1:configuration.MAX_NUM_PODS + 1]:
            if cpu_usage == 3:
                pods_high_cpu += 1    
            elif cpu_usage == 1:
                pods_low_cpu += 1
            else:
                pods_medium_cpu += 1

        print("State = {}".format(state))
        print("pods_low_cpu = {}, pods_medium_cpu = {}, pods_high_cpu = {}, action={}".format(pods_low_cpu, pods_medium_cpu, pods_high_cpu, action))
        pods_state = [pods_low_cpu, pods_medium_cpu, pods_high_cpu, action]
        print("Pods state = {}".format(pods_state))
        key = "["+str(pods_low_cpu)+", "+str(pods_medium_cpu)+", "+str(pods_high_cpu)+", "+str(action)+"]"
        print("Key >>> {}".format(key))
        reward = rewards.state_rewards[key]
        print("Reward >>> {}".format(reward))

        # print("pods = {}, pods_high_cpu = {}, pods_medium_cpu = {}, pods_low_cpu={}".format(number_of_pods, pods_high_cpu, pods_medium_cpu, pods_low_cpu))

        # Penalizaciones por decisiones incorrectas
        # if pods_high_cpu > 0 and pods_low_cpu == 0 and pods_medium_cpu == 0 and pods_not_spawned > 0 and action <= number_of_pods:
        #     reward -= 1
        #     print("Penalizacion 1")
        # if pods_high_cpu == 0 and pods_low_cpu > 1 and pods_medium_cpu == 0 and action >= number_of_pods:
        #     reward -= 1
        #     print("Penalizacion 2")
        # if pods_high_cpu > pods_medium_cpu and pods_not_spawned > 0 and action <= number_of_pods:
        #     reward -= 0.5
        #     print("Penalizacion 3")
        # if pods_medium_cpu == number_of_pods and pods_not_spawned > 0 and action > number_of_pods:
        #     reward -= 0.5
        #     print("Penalizacion 4")
        # if pods_medium_cpu > 1 and pods_low_cpu == 0 and pods_high_cpu == 0 and action - number_of_pods > 1:
        #     reward -= 1 
        #     print("Penalizacion 5")
        # if pods_low_cpu > pods_medium_cpu and action >= number_of_pods:
        #     reward -= 0.5
        #     print("Penalizacion 6")
        # if pods_low_cpu > 1 and pods_medium_cpu == 0 and pods_high_cpu == 0 and action - number_of_pods > 1:
        #     reward -= 1
        #     print("Penalizacion 7")         

        # # Recompensas por decisiones correctas
        # if pods_high_cpu > 0 and pods_low_cpu == 0 and pods_not_spawned > 0 and action > number_of_pods:
        #     reward += 1
        #     print("Recompensa 1")
        # if pods_medium_cpu == number_of_pods and action == number_of_pods:
        #     reward += 1
        #     print("Recompensa 2")            
        # if pods_high_cpu == configuration.MAX_NUM_PODS and number_of_pods == configuration.MAX_NUM_PODS:
        #     reward += 0.5
        #     print("Recompensa 3")
        # if pods_medium_cpu == number_of_pods and action < number_of_pods:
        #     reward -= 0.5
        #     print("Recompensa 4")
        # if pods_low_cpu > 1 and pods_high_cpu == 0 and pods_medium_cpu == 0 and action < number_of_pods:
        #     reward += 1
        #     print("Recompensa 5")
        # if pods_low_cpu != 0 and pods_high_cpu == 0 and pods_medium_cpu != 0 and action <= number_of_pods:
        #     reward += 0.5
        #     print("Recompensa 6")

        # print("State = {}, Action = {}, reward= {}".format(state, action, reward))
        return reward

    def get_state(self):

        resource = self.api.list_namespaced_custom_object(group="metrics.k8s.io",version="v1beta1", namespace="php-apache", plural="pods")

        count = 0
        cpu = []
        mem = []

        for pod in resource["items"]:
            if pod['metadata']['name'].startswith('php-apache'):
                count += 1
                if count <= configuration.MAX_NUM_PODS and pod['containers']:
                    # print("Pods >> {}".format(pod['containers']))
                    cpu.append(round(float(re.sub("[^0-9]", "", pod['containers'][0]['usage']['cpu'])) / 1000000, 2))
                    mem.append(float(re.sub("[^0-9]", "", pod['containers'][0]['usage']['memory'])))

        if count > configuration.MAX_NUM_PODS:
            count = configuration.MAX_NUM_PODS

        cpu += [0] * (configuration.MAX_NUM_PODS - len(cpu))
        mem += [0] * (configuration.MAX_NUM_PODS - len(mem))

        state = np.reshape(np.asarray([count] + cpu), (1, configuration.MAX_NUM_PODS + 1)) 
        print("State = {}".format(state))

        discretized_state = [count]
        for cpu_usage in state[0][1:configuration.MAX_NUM_PODS + 1]:
            if cpu_usage > 300:
                discretized_state.append(3)    
            elif cpu_usage < 100 and cpu_usage > 0:
                discretized_state.append(1)
            elif cpu_usage == 0.0:
                discretized_state.append(0)
            else:
                discretized_state.append(2)

        print("Discretized state = {}".format(discretized_state))
        return discretized_state

    def set_replicas(self, num_replicas):
        print('Setting number of Replicas to: {}'.format(str(num_replicas)))
        command = "kubectl scale deployment php-apache --replicas=" + str(num_replicas) + " -n php-apache"
        os.system(command)