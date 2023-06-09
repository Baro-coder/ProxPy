import sys
import requests
from bs4 import BeautifulSoup as bs
from proxpy.models import (Proxy, ProxyType, CountryID, Anonymity)


URL = 'https://www.freeproxy.world/'


def get_proxy_list(amount : int = None, proxy_type : ProxyType = None, country_id : CountryID = None, anonymity : Anonymity = None, port : int = None):
    # Query params
    _type : str = ""
    _anonymity : str = ""
    _country : str = ""
    _speed : str = ""
    _port : str = ""
    _page : int = 0
    
    # Params normalization
    if proxy_type is not None:
        _type = proxy_type.value
    if country_id is not None:
        _country = country_id.value
    if anonymity is not None:
        _anonymity = anonymity.value
    if port is not None:
        _port = str(port)
    
    proxies : list[Proxy] = []
    
    while True:
        _page += 1
        query : str = f'{URL}?type={_type}&anonymity={_anonymity}&country={_country}&speed={_speed}&port={_port}&page={_page}'
        print(f'GET --> {query}', file=sys.stderr)
        print(f'  * Proxies : {len(proxies)}', file=sys.stderr)
        
        response = requests.get(query)
    
        if response.status_code == 200:
            soup = bs(response.content, 'html.parser')

            ips : list[str] = []
            ports : list[int] = []
            protocols : list[str] = []
            speeds : list[int] = []

            ips_results = soup.select('.show-ip-div')
            
            if len(ips_results) == 0:
                break

            for ips_result in ips_results:
                ips.append(ips_result.text.replace('\n', ''))

            a_results = soup.find_all('a')
            for a in a_results:
                _href : str = a['href']
                if _href.startswith('/?port'):
                    ports.append(int(a.text))
                if _href.startswith('/?type'):
                    protocols.append(a.text.split()[0])
                if _href.startswith('/?speed'):
                    speeds.append(int(a.text.split(' ', 1)[0]))

            for prot, ip, port, speed in zip(protocols, ips, ports, speeds):
                _protocol = None
                match(prot):
                    case 'http':
                        max_speed = 1000
                        _protocol = ProxyType.HTTP
                    case 'https':
                        max_speed = 4000
                        _protocol = ProxyType.HTTPS
                    case 'socks4':
                        max_speed = 2000
                        _protocol = ProxyType.SOCKS4
                    case 'socks5':
                        max_speed = 3000
                        _protocol = ProxyType.SOCKS5
                        
                if speed > max_speed:
                    continue

                if _protocol:
                    if amount is not None:
                        if len(proxies) == amount:
                            return proxies
                    proxies.append(Proxy(_protocol, ip, port))

        else:
            break
        
    return proxies
