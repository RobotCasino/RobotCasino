from enum import Enum

from src.casinos.test.test import Test
from src.casinos.one_win.one_win import OneWin
from src.domain.casinos.casino import Casino

class Casinos(Enum):
    ONE_WIN = OneWin()
    TEST = Test()

    @staticmethod
    def get_casino_or_fail(name: str) -> Casino:
        casino = Casinos.get_casino(name)
        if casino is None:
            raise ValueError(f"Unknown casino: {name}")
        return casino

    @staticmethod
    def get_casino(name: str) -> Casino | None:
        match name.lower():
            case "one-win":
                return Casinos.ONE_WIN.value
            case "test":
                return Casinos.TEST.value
            case _:
                return None