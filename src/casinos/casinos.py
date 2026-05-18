from enum import Enum

from src.casinos.one_win import OneWin
from src.domain import Casino

class Casinos(Enum):
    ONE_WIN = OneWin()

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
            case _:
                return None