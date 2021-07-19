from dependency_injector  import providers, containers
from agents.DQNAgent      import DQAgent
from environments         import environment

class Configs(containers.DeclarativeContainer):
    config = providers.Configuration('config')

class Agents(containers.DeclarativeContainer):
    agent = providers.Singleton(DQAgent)
    # other clients 

class Environments(containers.DeclarativeContainer):
    env = providers.Singleton(environment)
    # other clients     