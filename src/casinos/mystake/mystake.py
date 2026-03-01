from typing import Any, Dict, List
from src.bootstrap import get_environment
from src.browser import Cookie
from src.casinos import Casino
from src.casinos.mystake.games import Dino
from time import time

class MyStake(Casino):

    __name = 'mystake'
    __display_name = 'MyStake'
    __domain = 'mystake.com'
    __url = 'https://mystake.com/'

    __games = {
        'dino': lambda: Dino(MyStake.__name, 'https://mystake.com/es/casino/gamepage?gameid=12489'),
    }

    def __init__(self):
        super().__init__(self.__name, self.__url, self.__games)

    def get_cookies(self) -> List[Dict[str, Any]]:
        token = Cookie() \
            .set_name("AppAuth") \
            .set_value(get_environment("SESSION_TOKEN")) \
            .set_domain(f"{self.__domain}") \
            .set_path("/") \
            .set_expires(time() + 365 * 24 * 3600) \
            .set_http_only(False) \
            .set_secure(True) \
            .set_same_site("None") \
            .build()
        
        return [
            token
        ]
    
__ALL__ = ['MyStake']