import requests
from itertools import cycle
from lxml.html import fromstring


def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//tbody/tr')[:100]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            #Grabbing IP and corresponding PORT
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    return proxies


# proxies = get_proxies()
proxies = ['159.89.228.253:38172',
           '167.71.241.136:33299',
           '142.54.235.9:4145',
           '95.214.26.126:8080',
           '67.201.33.10:25283',
           '68.71.254.6:4145'
           ]
proxy_pool = cycle(proxies)
url = 'https://httpbin.org/ip'

print(' Collected proxies: ' + str(len(proxies)))

for i in range(1,10):
    # Get a proxy from the pool
    proxy = next(proxy_pool)
    print(f"\n Request #{i} : --> {proxy} --> {url}")    
    try:
        response = requests.get(url,proxies={"socks4": proxy}, timeout=5)
        print('  * IP: ' + response.json()['origin'])

    except KeyboardInterrupt:
        print(' Aborted.')
        break

    except:
        # Most free proxies will often get connection errors. You will have retry the entire request using another proxy to work. 
        # We will just skip retries as its beyond the scope of this tutorial and we are only downloading a single url 
        print("  * Connection Error! Looking for another proxy...")
