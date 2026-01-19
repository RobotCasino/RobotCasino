from abc import ABC, abstractmethod
from playwright.async_api import Page

class Game(ABC):

    __casino: str
    __name: str
    __url: str
    __strategy: str

    def __init__(self, casino, name, url, strategy):
        self.__casino = casino
        self.__name = name
        self.__url = url
        self.__strategy = strategy

    @abstractmethod
    async def play(self, page: Page):
        pass
    

    def get_name(self):
        return self.__name

    def get_url(self):
        return self.__url

    def get_strategy(self):
        return self.__strategy
    
    def get_casino(self):
        return self.__casino