from environments.pods_cpu_mem import K8Sstate
from configuration import configuration
import numpy as np
import datetime
import sys
import os
import re
from kubernetes import client, config

class K8Senvironment():
    
    def __init__(self):
        self.observation_space_n = 99999999
        self.action_space_n = configuration.NUM_OF_ACTIONS
        self.action_space   = [0,1,2]
        config.load_kube_config()
        self.api = client.CustomObjectsApi()
        self.reward = 0
    
    
    def step(self, action):

        if action == 0:         # if action is 2, do nothing
            self.reward += self.calculate_reward(action)     
    
        if action == 1:         # if action is 1, add Pod
            self.add_pod()
            self.reward += self.calculate_reward(action)

        if action == 2:         # if action is 2, remove Pod 
            self.remove_pod()
            self.reward += self.calculate_reward(action)      

        # retrieving the state vector       
        self.state = self.get_state()

        return self.state, self.reward

    
    def calculate_reward(self, action):
        # calculate reward after action
        reward = 0
        self.state = self.get_state()    
        number_of_pods = self.state[0]
        if action == 1:
            for i in range(number_of_pods):
                if self.state[i] > 50:
                    reward += 1
                else:
                    reward -= 1
        elif action == 2:
            for i in range(number_of_pods):
                if self.state[i] < 50:
                    reward += 1
                else:
                    reward -= 1 
        else:
            if number_of_pods < 5:
                reward += 1
            else:
                reward -= 1
                
            for i in range(number_of_pods):
                if self.state[i] < 50:
                    reward += 1
                else:
                    reward -= 1   

        return reward                     

    
    def add_pod(self):
        # add pod with scale-cluster.py
        # retrieving the state vector
        self.state = self.get_state()    
        number_of_pods = self.state[0] 
        if number_of_pods < configuration.MAX_NUM_PODS:
            number_of_pods += 1
        self.set_replicas(number_of_pods)
    
    def remove_pod(self):
        self.state = self.get_state()    
        number_of_pods = self.state[0] 
        if number_of_pods > configuration.MIN_NUM_PODS:
            number_of_pods -= 1
        self.set_replicas(number_of_pods)

    def get_state(self):

        resource = self.api.list_namespaced_custom_object(group="metrics.k8s.io",version="v1beta1", namespace="php-apache", plural="pods")

        count = 0
        cpu = []
        mem = []

        for pod in resource["items"]:
            if pod['metadata']['name'].startswith('php-apache'):
                count += 1
                cpu.append(round(float(re.sub("[^0-9]", "", pod['containers'][0]['usage']['cpu'])) / 6000, 2))
                mem.append(float(re.sub("[^0-9]", "", pod['containers'][0]['usage']['memory'])))

        cpu += [0] * (configuration.MAX_NUM_PODS - len(cpu))
        mem += [0] * (configuration.MAX_NUM_PODS - len(mem))

        state = [count] + cpu + mem
        print(state)
        return state

    def set_replicas(self, num_replicas):
        print('Number of Replicas: {}'.format(str(num_replicas)))
        # os.system('kubectl scale deployment php-apache --replicas=3')
        command = "kubectl scale deployment php-apache --replicas=" + str(num_replicas) + " -n php-apache"
        print(command)
        os.system(command)