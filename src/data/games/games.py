from enum import Enum

from core.domain.games.game import Game
from data.games.one_win.aviator import Aviator as OneWinAviator
from data.games.test.aviator import Aviator as TestAviator
from data.games.mystake.dino import Dino as MystakeDino

class Games(Enum):
    ONE_WIN_AVIATOR = OneWinAviator()
    TEST_AVIATOR = TestAviator()
    MYSTAKE_DINO = MystakeDino()

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
            case "test-aviator":
                return Games.TEST_AVIATOR.value
            case "mystake-dino":
                return Games.MYSTAKE_DINO.value
            case _:
                return None