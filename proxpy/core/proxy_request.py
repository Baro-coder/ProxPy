import requests
import itertools
import random as rand
from proxpy.core.user_agent import get_user_agent_list
from proxpy.models import Proxy

def proxy_request(proxy_list : list[Proxy], url : str | bytes, http_method : str | bytes = 'get', **kwargs) -> requests.Response:
    user_agents_list = get_user_agent_list()
    rand.shuffle(user_agents_list)
    
    proxy_pool = itertools.cycle(proxy_list)
    user_agent_pool = itertools.cycle(user_agents_list)
    
    while True:
        proxy = next(proxy_pool)
        proxies : dict = {
            'http' : f'{proxy.address}:{proxy.port}',
            'https' : f'{proxy.address}:{proxy.port}'
            }
        
        headers = requests.utils.default_headers()
        headers.update(
            {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0',
            }
        )
        
        try:
            print(f' * {http_method.upper()} --> {proxy} --> {url}')
            response = requests.request(method=http_method,
                                        url=url,
                                        proxies=proxies,
                                        headers=headers,
                                        **kwargs)

        except Exception as err:
            print(f'   - Error: {type(err)} : {err}')
            print('   - Error : Looking for another proxy configuration...\n')
        
        else:
            break

        
    return response
