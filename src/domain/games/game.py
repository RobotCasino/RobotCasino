from abc import ABC, abstractmethod
from src.web import Tab

from src.domain.games.vo import Strategy

class Game(ABC):
    def __init__(self, casino: str, url: str, name: str):
        self.__casino = casino
        self.__url = url
        self.__name = name
        self.__strategy: Strategy | None = None

    @abstractmethod
    async def play(self, tab: Tab):
        pass

    def get_name(self):
        return self.__name

    def get_url(self):
        return self.__url

    def get_strategy(self):
        return self.__strategy
    
    def get_casino(self):
        return self.__casino
    
    def load_strategy(self, strategy: Strategy):
        self.__strategy = strategy