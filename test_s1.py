import sys
import httpx
import asyncio
import proxpy as prx


class Client():
    def __init__(self, proxy : prx.Proxy = None) -> None:
        self._proxy = proxy

        proxy = str(proxy) if proxy else None
        
        timeout = httpx.Timeout(10.0, connect=20.0)
        
        self._handler = httpx.AsyncClient(proxies=proxy, timeout=timeout, verify=False)
        self._handler.headers.update(
            {
                'User-Agent' : prx.get_random_user_agent(),
            }
        )
    
    def __repr__(self) -> str:
        _repr = f'Client : {self._proxy}' if self._proxy else 'Client : Native'
        return _repr
    
    async def request(self, method : str, url : str, **kwargs) -> httpx.Response | Exception:
        try:
            r = await self._handler.request(method=method, url=url, **kwargs)
            return r
        except Exception as err:
            return err


async def main() -> None:
    url = 'https://httpbin.org/ip'
    method = 'get'
    
    print('  * Collecting proxies...')
    proxies : list[prx.Proxy] = prx.get_proxy_list_freeproxyworld(proxy_type=prx.ProxyType.SOCKS5,
                                                                  country_id=prx.CountryID.UNITED_STATES,
                                                                  speed=100)

    clients_count = len(proxies)

    print('  * Collected proxies: ' + str(len(proxies)))    
    if clients_count == 0:
        print('Need more proxies!')
        sys.exit(1)
    
    for proxy in proxies:
        print(f'    - {proxy}')
        
        
    clients : list[Client] = []
    print('\n  * Setting up the clients...')
    for i in range(clients_count):
        clients.append(Client(proxies[i]))
    
    
    print('  * Clients:')
    coros = []
    for client in clients:
        coros.append(client.request(method, url, timeout=8))
        print('    - ' + str(client))


    print('\n  * Making requests...')
    for coro in asyncio.as_completed(coros):
        result = await coro
        if type(result) is httpx.Response:
            if result.status_code == 200:
                print(f'    - {result.status_code} : {result.json()}')
            else:
                print(f'    - {result.status_code}')
        else:
            print(f'    - {type(result)} : {str(result)}')

if __name__ == '__main__':
    asyncio.run(main())