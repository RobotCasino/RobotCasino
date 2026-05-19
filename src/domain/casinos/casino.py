from src.navigators import Cookie
from abc import ABC, abstractmethod

class Casino(ABC):
    def __init__(self, name: str, url: str) -> None:
        self.__name = name
        self.__url = url

    @abstractmethod
    def get_cookies(self) -> list[Cookie]:
        pass

    def get_name(self):
        return self.__name

    def get_url(self):
        return self.__url