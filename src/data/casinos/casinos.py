from enum import Enum

from data.casinos.test.test import Test
from data.casinos.one_win.one_win import OneWin
from core.domain.casinos.casino import Casino
from data.casinos.mystake.mystake import Mystake

class Casinos(Enum):
    ONE_WIN = OneWin()
    TEST = Test()
    MYSTAKE = Mystake()

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
            case "mystake":
                return Casinos.MYSTAKE.value
            case _:
                return None