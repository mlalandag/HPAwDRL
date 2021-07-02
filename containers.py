from dependency_injector  import providers, containers
from agents.random_agents import RandomAgent
from environments         import environment, task_queue, worker_pool

class Configs(containers.DeclarativeContainer):
    config = providers.Configuration('config')

class Agents(containers.DeclarativeContainer):
    agent = providers.Singleton(RandomAgent)
    # other clients 

class Environments(containers.DeclarativeContainer):
    worker_p = providers.Singleton(...)
    task_q   = providers.Singleton(...)
    env = providers.Singleton(Environment, worker_pool= worker_p, task_queue= task_q)
    # other clients     