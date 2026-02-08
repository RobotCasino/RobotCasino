from abc import ABC, abstractmethod
from pydoll.browser.tab import Tab

from robotcasino.casinos.strategier import Strategier
from pydoll.elements.web_element import WebElement

class Game(ABC):

    __casino: str
    __name: str
    __url: str
    __strategy: str = 'default'
    __user_data: dict = {}

    def __init__(self, casino, url, name):
        self.__casino = casino
        self.__url = url
        self.__name = name

    @abstractmethod
    async def play(self, tab: Tab):
        pass

    @abstractmethod
    async def _load_strategy(self, iframe: WebElement):
        pass

    def get_name(self):
        return self.__name

    def get_url(self):
        return self.__url

    def get_strategy(self):
        return self.__strategy
    
    def get_casino(self):
        return self.__casino
    
    def get_user_data(self):
        return self.__user_data
    
    def set_user_data(self, data: dict):
        self.__user_data = data
    
    def set_strategy(self, strategy: str):
        if not Strategier.is_strategy(self.get_name(), strategy):
            raise ValueError(f"Strategy {strategy} not found for game {self.get_name()} in casino {self.get_casino()}")
        
        self.__strategy = strategy