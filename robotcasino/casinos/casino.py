from abc import abstractmethod
from typing import Callable, List, Dict, Any
from robotcasino.casinos import game
from robotcasino.casinos.game import Game

class Casino():

    def __init__(self, name: str, url: str, games: dict[str, Callable]):
        self._name = name
        self._url = url
        self._games = games

    @abstractmethod
    def get_cookies(self) -> List[Dict[str, Any]]:
        pass

    def get_name(self):
        return self._name
    
    def get_url(self):
        return self._url

    def get_game(self, game: str) -> Game:
        if game not in self._games:
            raise ValueError(f'Game {game} not found in casino {self.get_name()}')

        return self._games[game]()
    
