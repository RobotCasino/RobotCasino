from typing import Any, Dict, List
from src.infrastructure.config import get_environment
from src.infrastructure.browser import Cookie
from src.domain import Casino
from src.casinos.one_win.games import Aviator
from time import time

class OneWin(Casino):

    __name = 'one_win'
    __display_name = '1Win'
    __domain = '1win.com'
    __url = 'https://1win.com/'

    __games = {
        'aviator': lambda: Aviator(OneWin.__name, 'https://1win.com/casino/play/v_spribe:aviator'),
    }

    def __init__(self):
        super().__init__(self.__name, self.__url, self.__games)

    def get_cookies(self) -> List[Dict[str, Any]]:
        token = Cookie() \
            .set_name("1w_token") \
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
    
__ALL__ = ['OneWin']