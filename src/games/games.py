from enum import Enum

from src.domain import Game
from src.games import OneWinAviator

class Games(Enum):
    ONE_WIN_AVIATOR = OneWinAviator()

    @staticmethod
    def get_game_or_fail(casino: str, name: str) -> Game:
        game = Games.get_game(casino, name)
        if game is None:
            raise ValueError(f"Unknown game: {name}")
        return game

    @staticmethod
    def get_game(casino: str, name: str) -> Game | None:
        match f"{casino.lower()}-{name.lower()}":
            case "one-win-aviator":
                return Games.ONE_WIN_AVIATOR.value
            case _:
                return None
