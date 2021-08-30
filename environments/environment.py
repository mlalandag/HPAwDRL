from configuration import configuration
import numpy as np
import datetime
import time
import sys
import os
import re
from kubernetes import client, config

class K8Senvironment():
    
    def __init__(self):
        config.load_kube_config()
        self.api = client.CustomObjectsApi()
    
    def step(self, action):

        state  = self.get_state()
        self.set_replicas(action)
        time.sleep(10)                   
        new_state  = self.get_state()
        reward = self.calculate_reward_state(state, action)

        return new_state, reward    

    def calculate_reward_state(self, state, action):
        # calculate reward after action
        reward = 0
        
        number_of_pods = int(state[0][0])
        if number_of_pods > configuration.MAX_NUM_PODS:
            number_of_pods = configuration.MAX_NUM_PODS   
        pods_high_cpu = 0
        pods_medium_cpu = 0
        pods_low_cpu = 0
        pods_not_spawned = configuration.MAX_NUM_PODS - number_of_pods
        
        for i in range(number_of_pods):
            if state[0][i+1] > 200:
                pods_high_cpu += 1    
            elif state[0][i+1] < 50:
                pods_low_cpu += 1
            else:
                pods_medium_cpu += 1

        # print("pods = {}, pods_high_cpu = {}, pods_medium_cpu = {}, pods_low_cpu={}".format(number_of_pods, pods_high_cpu, pods_medium_cpu, pods_low_cpu))

        # Penalizaciones por decisiones incorrectas
        if pods_high_cpu > 0 and pods_low_cpu == 0 and pods_medium_cpu == 0 and pods_not_spawned > 0 and action <= number_of_pods:
            reward -= 10
        if pods_high_cpu == 0 and pods_low_cpu > 1 and pods_medium_cpu == 0 and action >= number_of_pods:
            reward -= 10
        if pods_high_cpu > pods_medium_cpu and pods_not_spawned > 0 and action <= number_of_pods:
            reward -= 5
        if pods_medium_cpu == number_of_pods and pods_not_spawned > 0 and action > number_of_pods:
            reward -= 5 
        if pods_low_cpu > pods_medium_cpu and action >= number_of_pods:
            reward -= 5                   

        # Recompensas por decisiones correctas
        if pods_high_cpu > 0 and pods_low_cpu == 0 and pods_not_spawned > 0 and action > number_of_pods:
            reward += 10
        if pods_medium_cpu == number_of_pods and action == number_of_pods:
            reward += 10                 
        if pods_high_cpu == configuration.MAX_NUM_PODS and number_of_pods == configuration.MAX_NUM_PODS:
            reward += 5   
        if pods_medium_cpu == number_of_pods and action < number_of_pods:
            reward -= 5 
        if pods_low_cpu > 1 and pods_high_cpu == 0 and pods_medium_cpu == 0 and action < number_of_pods:
            reward += 10
        if pods_low_cpu != 0 and pods_high_cpu == 0 and pods_medium_cpu != 0 and action <= number_of_pods:
            reward += 5

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

        cpu += [0] * (configuration.MAX_NUM_PODS - len(cpu))
        mem += [0] * (configuration.MAX_NUM_PODS - len(mem))

        # state = np.reshape(np.asarray([count] + cpu + mem), (1, 21))
        state = np.reshape(np.asarray([count] + cpu), (1, configuration.MAX_NUM_PODS + 1))        
        #print(state)
        return state

    def set_replicas(self, num_replicas):
        print('Setting number of Replicas to: {}'.format(str(num_replicas)))
        # os.system('kubectl scale deployment php-apache --replicas=3')
        command = "kubectl scale deployment php-apache --replicas=" + str(num_replicas) + " -n php-apache"
        # print(command)
        os.system(command)

"""     def step(self, action):

        if action == 0:         # if action is 2, do nothing
            self.reward = self.calculate_reward(action)     
    
        if action == 1:         # if action is 1, add Pod
            self.add_pod()
            time.sleep(5)             
            self.reward = self.calculate_reward(action)

        if action == 2:         # if action is 2, remove Pod 
            self.remove_pod()
            time.sleep(5)            
            self.reward = self.calculate_reward(action)      

        # retrieving the state vector
        time.sleep(2)                   
        self.state = self.get_state()

        return self.state, self.reward

    def calculate_reward_action(self, action):
        # calculate reward after action
        reward = 0
        total_reward = 0
        self.state = self.get_state()    
        number_of_pods = int(self.state[0][0])
        if number_of_pods > 10:
            number_of_pods = 10
        if action == 1:
            for i in range(number_of_pods):
                if self.state[0][i+1] > 150:
                    reward = min(int((configuration.MAX_NUM_PODS - number_of_pods) * self.state[0][i+1]), 100)
                else:
                    reward = - min(int(number_of_pods * self.state[0][i+1]), 100)    
                print("action = {}, pod = {}, cpu={}, reward= {}".format(action, i+1, self.state[0][i+1], reward))
                total_reward += reward
        elif action == 2:
            for i in range(number_of_pods):
                if self.state[0][i+1] != 0:
                    if self.state[0][i+1] < 200:
                        reward = min(int((configuration.MAX_NUM_PODS - number_of_pods) * (( 1 / self.state[0][i+1]) * 100)), 100)
                    else:
                        reward = - min(int(number_of_pods * (( 1 / self.state[0][i+1]) * 100)), 100)
                    print("action = {}, pod = {}, cpu={}, reward= {}".format(action, i+1, self.state[0][i+1], reward))
                    total_reward += reward                    
        else:
            for i in range(number_of_pods):
                if self.state[0][i+1] != 0:               
                    if (self.state[0][i+1] < 100 and number_of_pods > 5) or (self.state[0][i+1] > 150 and number_of_pods < 5):
                        reward = - min(int((configuration.MAX_NUM_PODS - number_of_pods) * ( 1 / self.state[0][i+1]) * 100), 100)
                    else:                        
                        reward = min(int((configuration.MAX_NUM_PODS - number_of_pods) * ( 1 / self.state[0][i+1]) * 100), 100)                        
                print("action = {}, pod = {}, cpu={}, reward= {}".format(action, i+1, self.state[0][i+1], reward))   
                total_reward += reward                                         

        print("Action = {}, Total reward= {}".format(action, total_reward))
        return total_reward                     

    
    def add_pod(self):
        # add pod with scale-cluster.py
        # retrieving the state vector
        self.state = self.get_state()    
        number_of_pods = int(self.state[0][0])
        if number_of_pods < configuration.MAX_NUM_PODS:
            number_of_pods += 1
            print("Adding pod number {}".format(number_of_pods))
        self.set_replicas(number_of_pods)
    
    def remove_pod(self):
        self.state = self.get_state()    
        number_of_pods = int(self.state[0][0])
        if number_of_pods > configuration.MIN_NUM_PODS:
            number_of_pods -= 1
            print("Removing pod number {}".format(number_of_pods + 1))            
        self.set_replicas(number_of_pods) """
