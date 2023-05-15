import sys
import time
import requests
import itertools
import proxpy as prx
from bs4 import BeautifulSoup as bs

def main():
    print('-- ProxPy --\n')
    
    print('  * Collecting proxies...')
    proxies : list[prx.Proxy] = prx.get_proxy_list(amount=150,
                                                   speed=600,
                                                   proxy_type=prx.ProxyType.SOCKS4)
    
    proxies_http_count : int = 0
    proxies_https_count : int = 0
    proxies_socks4_count : int = 0
    proxies_socks5_count : int = 0
    
    for proxy in proxies:
        match(proxy.protocol):
            case prx.ProxyType.HTTP:
                proxies_http_count += 1
            case prx.ProxyType.HTTPS:
                proxies_https_count += 1
            case prx.ProxyType.SOCKS4:
                proxies_socks4_count += 1
            case prx.ProxyType.SOCKS5:
                proxies_socks5_count += 1
    
    print(f'\n  * Collected proxies: {len(proxies)}')        
    print(f'    - HTTP   : {proxies_http_count}')
    print(f'    - HTTPS  : {proxies_https_count}')
    print(f'    - SOCKS4 : {proxies_socks4_count}')
    print(f'    - SOCKS5 : {proxies_socks5_count}')
    
    if len(proxies) == 0:
        print(' * Error : Need more proxies...')
        sys.exit(1)
    
    print()
    
    CHECK_IP_URL = 'https://httpbin.org/ip'
    
    s_max = 3
    sessions : list[requests.Session] = [] 
    
    print(f'  * Collecting sessions...')
    while len(sessions) < s_max:
        s, r = prx.proxy_session_request(
            proxy_list=proxies,
            url=CHECK_IP_URL,
            timeout=6,
            verify=False
        )
        
        sessions.append(s)
    
    
    URL = 'https://www.google.com/search/'
    query = {
        'q' : 'Facebook'
    }

    responses : list

    print('\n Cycle sessions requests:')
    while True:
        for i in range(len(sessions)):
            try:
                r = sessions[i].get(method='GET', url=URL, params=query, timeout=3)
            except Exception as err:
                responses.append(None)
            else:
                responses.append(r)
        
        _none_count = 0
        for i in range(len(sessions)):
            if responses[i] is not None:
                print(f' - Session[{i}] : {responses[i].status_code}')
            else:
                _none_count += 1
                print(f' - Session[{i}] : Error')
        print()
        
        if _none_count == len(sessions):
            break

        
    sys.exit(0)
    
if __name__ == '__main__':
    main()