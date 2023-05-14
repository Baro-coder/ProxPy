from enum import Enum
from typing import NamedTuple


class ProxyType(Enum):
    HTTP    = "http"
    HTTPS   = "https"
    SOCKS4  = "socks4"
    SOCKS5  = "socks5"
    

class CountryID(Enum):
    CANADA = 'CA'
    

class Anonymity(Enum):
    HIGH    = 4
    LOW     = 1


class Proxy(NamedTuple):
    protocol : ProxyType
    address : str
    port : int
    
    def __repr__(self):
        return f'{self.protocol.value}://{self.address}:{self.port}'
