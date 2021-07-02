# from containers import  Configs, Agents, Environments
from environments.environment import EpisodicDiscretizedEnvironment
from environments.task_queue  import TaskQueue, Task
from environments.worker_pool import WorkerPool, Worker
from agents.random_agents     import RandomAgent
from agents.td_agents         import QLearningAgent
from config                   import NUM_EPISODES

import time
import random

if __name__ == "__main__":

    # Creamos el entorno y el agente       
    env = EpisodicDiscretizedEnvironment()
    agent = QLearningAgent(env.observation_space_n, env.action_space,  env.action_space_n)
    total_reward = 0

    for i in range(NUM_EPISODES):        
        # Inicializamos state, reward y done
        state   = env.reset()
        reward  = 0
        done    = False            
        past_num_tasks = 0
    

        while not done:

            # Creamos una tarea cada cierto tiempo 
            # (cambiar el divisor en la operación % para variar la frecuencia)
            num = random.randint(1, 100)
            if num % 1 == 0:
                task = Task("Fichero")
                env.task_queue.add_task(task)

            # Si hay tareas en la cola y hay algun worker libre 
            # le asignamos la primera tarea pendiente 
            for wrk in env.worker_pool.pool:
                if not wrk.is_running():
                    if env.task_queue.get_num_tasks() > 0:
                        wrk.run_task(env.task_queue.take_task())

            # El agente decide la siguiente accion y recoge 
            # el nuevo estado y la recompensa
            action = agent.act(state, reward, done)
            next_state, reward, done, info = env.step(action, state[2], state[3])
            agent.update_q_table(state, next_state, action, reward)

            total_reward += reward
            state = next_state     
            print("state = {}, reward= {}, done = {}, total_reward={:.2f}, Qtime={:.2f}".format(state, reward, done, total_reward, info.get('avg_time_in_queue')))              