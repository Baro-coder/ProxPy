import sys
import requests
import itertools
from proxpy.models import Proxy, ProxyType


def get_proxy_session(
    proxy : Proxy,
    user_agent : str = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0'
    ) -> requests.Session:
    
    print(f' * Session via {proxy}', file=sys.stderr)
    
    s = requests.Session()
    
    headers = requests.utils.default_headers()
    headers.update(
        {
            'User-Agent' : user_agent,
        }
    )
    
    s.headers = headers
    
    proxies = {
        'http' : f'{proxy.address}:{proxy.port}',
        'https' : f'{proxy.address}:{proxy.port}'
    }
    s.proxies = proxies
    
    return s


def proxy_session_request(
    proxy_list : list[Proxy],
    url : str | bytes,
    http_method : str | bytes = 'get',
    user_agent : str = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0',
    **kwargs
    ) -> tuple[requests.Session, requests.Response]:
    
    load_seq = ['\\', '|', '/', '-']
    load_pool = itertools.cycle(load_seq)
    
    proxy_pool = itertools.cycle(proxy_list)
    while True:
        proxy = next(proxy_pool)
        
        session = get_proxy_session(
            proxy=proxy,
            user_agent=user_agent
        )

        print(f'  * Client(Session) --> [{proxy.protocol.value.upper()}] --> {proxy.address}:{proxy.port} --> {url}', file=sys.stderr)

        try:
            print(f'{next(load_pool)}', end='\r', file=sys.stdout)
            response = session.request(
                url=url,
                method=http_method,
                **kwargs
            )

        except Exception as err:
            # print(f'   - Error: {type(err)} : {err}', file=sys.stderr)
            print(f'   - {type(err)} : Looking for another proxy...\n', file=sys.stderr)
            
        else:
            print('    - Collected session!')
            return (session, response)
