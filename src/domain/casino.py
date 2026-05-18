from typing import Callable
from src.domain.game import Game
from src.infrastructure.browser import Cookie

class Casino():
    def __init__(self, name: str, url: str, games: dict[str, Callable[[], Game]]) -> None:
        self.__name = name
        self.__url = url
        self.__games = games

    def get_cookies(self) -> list[Cookie]:
        return []

    def get_name(self):
        return self.__name

    def get_url(self):
        return self.__url

    def get_game(self, game: str) -> Game:
        if game not in self.__games:
            raise ValueError(f'Game {game} not found in casino {self.get_name()}')

        return self.__games[game]()
