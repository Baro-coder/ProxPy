import os
import random as rand


def _get_user_agent_list() -> list[str]:
    sep = os.sep
    script_dir = os.path.abspath(__file__)
    user_agents_filepath : str = sep.join(script_dir.split(sep)[:-2]) + f'{sep}data{sep}user-agents_list.txt'

    user_agents : list[str] = []
    with open(user_agents_filepath, 'r') as file:
        lines = file.readlines()
        for line in lines:
            user_agents.append(line[:-1])

    return user_agents


USER_AGENT_LIST : list[str] = _get_user_agent_list()


def get_random_user_agent() -> str:
    min, max = 0, len(USER_AGENT_LIST)
    index = rand.randint(min, max)
    return USER_AGENT_LIST[index]


def get_user_agent_list() -> list[str]:
    return USER_AGENT_LIST