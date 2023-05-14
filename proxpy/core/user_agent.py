import os
import platform
import random as rand


def get_random_user_agent() -> str:
    script_dir = os.path.abspath(__file__)
    if platform.system() == 'Linux':
        sep = '/'
    else:
        sep = '\\'
    user_agents_filepath : str = sep.join(script_dir.split(sep)[:-2]) + f'{sep}data{sep}user-agents_list.txt'

    user_agents : list[str] = []
    with open(user_agents_filepath, 'r') as file:
        user_agents = file.readlines()
        
    return user_agents[rand.randint(0, len(user_agents))]


def get_user_agent_list() -> list[str]:
    script_dir = os.path.abspath(__file__)
    if platform.system() == 'Linux':
        sep = '/'
    else:
        sep = '\\'
    user_agents_filepath : str = sep.join(script_dir.split(sep)[:-2]) + f'{sep}data{sep}user-agents_list.txt'

    user_agents : list[str] = []
    with open(user_agents_filepath, 'r') as file:
        user_agents = file.readlines()
        
    return user_agents