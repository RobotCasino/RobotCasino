from typing import Callable
from domain.games.game import Game
from src.navigators import Cookie
from abc import ABC, abstractmethod

class Casino(ABC):
    def __init__(self, name: str, url: str, games: dict[str, Callable[[], Game]]) -> None:
        self.__name = name
        self.__url = url
        self.__games = games

    @abstractmethod
    def get_cookies(self) -> list[Cookie]:
        pass

    def get_name(self):
        return self.__name

    def get_url(self):
        return self.__url

    def get_game(self, game: str) -> Game:
        if game not in self.__games:
            raise ValueError(f'Game {game} not found in casino {self.get_name()}')

        return self.__games[game]()
