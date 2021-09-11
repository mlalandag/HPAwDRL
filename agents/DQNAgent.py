import numpy as np
import random
import tensorflow as tf
from collections import deque
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.initializers import Zeros
from configuration import configuration

class DQNAgent():
    
    def __init__(self, alpha, gamma, action_size, min_epsilon, epsilon, epsilon_decay):

        # Hiperparámetros
        self.alpha = alpha
        self.gamma = gamma
        self.action_size = action_size
        self.min_epsilon = min_epsilon   
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay

        # Replay buffer
        self.replay_buffer = deque(maxlen=5000)
        
        # Tasa de actualización de la target network
        self.update_rate = configuration.UPDATE_RATE  
        
        # Main network
        self.main_network = self.build_network()
        
        # Target network
        self.target_network = self.build_network()
        
        # Directorio donde almacenar el modelo de la Red
        self.path = configuration.PATH_MODEL


    def act(self, state, train):

        if train:
            self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)
            print("Epsilon = {}".format(self.epsilon))

            if random.uniform(0,1) < self.epsilon:
                return np.random.randint(self.action_size) + 1
        
        Q_values = self.main_network.predict(state)
        print("Q_values = {}".format(Q_values))
        
        return np.argmax(Q_values[0]) + 1      


    def build_network(self):

        model = Sequential()
        model.add(Dense(configuration.MAX_NUM_PODS + 1, activation='relu', input_shape=(configuration.MAX_NUM_PODS + 1,), kernel_initializer='glorot_uniform'))
        model.add(Dense(32, activation='relu', kernel_initializer='glorot_uniform'))        
        model.add(Dense(16, activation='relu', kernel_initializer='glorot_uniform'))
        model.add(Dense(self.action_size, kernel_initializer='glorot_uniform'))        
        model.compile(loss='mse', optimizer=Adam(), metrics=['accuracy'])        

        return model


    # Guardamos los datos de la transición o "step" en el Replay Buffer
    def store_transition(self, state, action, reward, next_state):
        self.replay_buffer.append((state, action, reward, next_state))

    
    # Entrenamiento de la red
    def train(self, batch_size):
        
        print("Training with batch_size = {}".format(configuration.BATCH_SIZE))

        # Muestreamos un mini batch de transiciones 
        minibatch = random.sample(self.replay_buffer, batch_size)
        
        # Calculamos el Q value basándonos en la Target network
        for state, action, reward, next_state in minibatch:

            print("state = {}, action = {}, reward= {}, next_state = {}".format(state, action, reward, next_state)) 
            Q_target_values = self.target_network.predict(next_state)
            print("Q_values = {}".format(Q_values)) 
            target_Q = (reward + self.gamma * np.amax(Q_target_values))
            print("target_Q >>> {} = {} + {} * {}".format(target_Q, reward, self.gamma,np.amax(Q_target_values)))                        
                
            # Calculamos el Q value utilizando la Main network 
            Q_values = self.main_network.predict(state)
            print("Q_values >> " + str(Q_values))
            
            # Actualizamos el valor predicho por la Main con el target_Q 
            print("Q_values[0][action - 1] >> " + str(Q_values[0][action - 1]))            
            print("delta                   >> " + str(self.alpha * (target_Q - Q_values[0][action - 1])))                     
            Q_values[0][action - 1] += self.alpha * (target_Q - Q_values[0][action - 1])
            print("Q_values >> " + str(Q_values))            
            
            # Entrenamos la Main network
            self.main_network.fit(state, Q_values, epochs=1, verbose=0)

            
    # Actualiza los parámetros de la Target network con los de la Main network
    def update_target_network(self):
        print("Updating target weights")
        self.target_network.set_weights(self.main_network.get_weights())        

    def save_weights(self):
        self.main_network.save_weights(self.path)

    def load_weights(self):
        self.main_network.load_weights(self.path)