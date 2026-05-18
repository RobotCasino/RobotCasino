from domain.game import Game
from src.infrastructure.config import get_environment
from src.infrastructure.browser import Cookie
from src.domain import Casino
from src.casinos.one_win.games import Aviator
from time import time
from typing import Callable

class OneWin(Casino):

    def __init__(self):
        self.__name = 'one_win'
        self.__display_name = '1Win'
        self.__domain = '1win.com'
        self.__url = 'https://1win.com/'
        
        self.__games: dict[str, Callable[[], Game]] = {
            'aviator': lambda: Aviator(self.__name, 'https://1win.com/casino/play/v_spribe:aviator'),
        }

        super().__init__(self.__name, self.__url, self.__games)

    def get_cookies(self) -> list[Cookie]:
        token = Cookie() \
            .set_name("1w_token") \
            .set_value(get_environment("SESSION_TOKEN")) \
            .set_domain(f"{self.__domain}") \
            .set_path("/") \
            .set_expires(time() + 365 * 24 * 3600) \
            .set_http_only(False) \
            .set_secure(True) \
            .set_same_site("None")
        
        return [
            token
        ]
    
__ALL__ = ['OneWin']