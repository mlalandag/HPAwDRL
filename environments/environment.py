from environments.task_queue  import TaskQueue, Task
from environments.worker_pool import WorkerPool, Worker
from config import *
import numpy as np
import datetime

class EpisodicDiscretizedEnvironment():
    
    def __init__(self):
        # Creamos el Pool con un tope de 10 workers
        self.worker_pool    = WorkerPool(MAX_NUM_WORKERS, INITIAL_WORKERS)
        # Cola donde ir encolando las tareas        
        self.task_queue     = TaskQueue() 
        self.info           =  {'avg_time_in_queue': 0}
        self.good_latency_init_datetime = datetime.datetime.now()
        self.observation_space_n = 99999999
        self.action_space_n = NUM_OF_ACTIONS
        self.action_space   = [0,1,2]
        self.state          = [self.worker_pool.get_num_workers(), 0, 0, 0]    
    
    def reset(self):
        self.worker_pool    = WorkerPool(MAX_NUM_WORKERS, INITIAL_WORKERS)
        self.task_queue     = TaskQueue() 
        self.info           =  {'avg_time_in_queue': 0}
        self.good_latency_init_datetime = datetime.datetime.now()
        self.state          = [self.worker_pool.get_num_workers(), 0, 0, 0]        
        return self.state
        
    
    def step(self, action, last_num_tasks, last_latency_level):

        reward, done = 0, False

        # Discretizamos el tiempo medio de estancia en la cola en varios niveles
        queue_latency_level = np.digitize(self.task_queue.avg_time_in_queue, BINS, right=False)
        # Si excedemos el límite de tiempo de tarea encolada terminamos el episodio (loose)
        if queue_latency_level >= len(BINS):
            done = True     
            print("Terminado por exceso de latencia en Cola")         

        if self.task_queue.get_num_tasks() > MAX_NUM_QUEUED_TASKS:
            done = True     
            print("Terminado por exceso tareas encoladas")                       

        # Si volvemos a buenos niveles de respuesta reiniciamos el contador para buena latencia
        if last_latency_level > GOOD_LATENCY_THRESOLD and queue_latency_level <= GOOD_LATENCY_THRESOLD:
            self.good_latency_init_datetime = datetime.datetime.now()

        # Si el sistema lleva un buen rato en buenos niveles de respuesta terminamos el episodio (win)
        if queue_latency_level <= GOOD_LATENCY_THRESOLD:
            time_in_good_latency = (datetime.datetime.now() - self.good_latency_init_datetime).total_seconds()    
            if  time_in_good_latency >= GOOD_LATENCY_LAPSE:
                done = True           
                print("Terminado por mantener buenos tiempos de latencia en Cola")                

        # Asignamos recompensas en función de las acciones y estado
        if action == 0:         # if action is 0, do nothing, check status and give reward
            if self.task_queue.get_num_tasks() > last_num_tasks:
                reward += ACTION_0_TASK_UP_REWARD
            else:
                reward += ACTION_0_TASK_DOWN_REWARD

            if queue_latency_level < last_latency_level:
                reward += ACTION_0_TIME_UP_REWARD
            else:
                reward += ACTION_0_TIME_DOWN_REWARD                
    
        if action == 1:         # if action is 1, add Worker to the Pool
            wrk = Worker()
            self.worker_pool.add_worker(wrk)
            reward += ACTION_1_REWARD        

        if action == 2:         # if action is 2, remove Worker from the Pool 
            self.worker_pool.remove_worker()
            reward += ACTION_2_REWARD      


        # creating the state vector
        self.state = [self.worker_pool.get_num_workers(),
                      self.worker_pool.get_num_workers_running(),        
                      self.task_queue.get_num_tasks(), 
                      queue_latency_level]              


        # Devolvemos también el tiempo medio de espera en la cola
        self.info['avg_time_in_queue'] = self.task_queue.avg_time_in_queue

        return self.state, reward, done, self.info

    def get_observation_space_n(self):        
        return self.observation_space_n
