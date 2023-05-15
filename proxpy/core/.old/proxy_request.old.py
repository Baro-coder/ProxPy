import sys
import requests
import itertools
from proxpy.models import Proxy

def proxy_request(proxy_list : list[Proxy], 
                  url : str | bytes, 
                  http_method : str | bytes = 'get', 
                  user_agent : str = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0', 
                  **kwargs) -> requests.Response:
        
    proxy_pool = itertools.cycle(proxy_list)
    
    while True:
        proxy = next(proxy_pool)
        proxies : dict = {
            'http' : f'{proxy.address}:{proxy.port}',
            'https' : f'{proxy.address}:{proxy.port}'
            }
        
        headers = requests.utils.default_headers()
        headers.update(
            {
                'User-Agent' : user_agent,
            }
        )
        
        try:
            print(f'  * Client --> [{proxy.protocol.value.upper()}] --> {proxy.address}:{proxy.port} --> {url}', file=sys.stderr)
            response = requests.request(method=http_method,
                                        url=url,
                                        proxies=proxies,
                                        headers=headers,
                                        **kwargs)
            return response
        
        except Exception as err:
            print(f'   - Error: {type(err)} : {err}', file=sys.stderr)
            print('   - Looking for another proxy...\n', file=sys.stderr)
