
from src.casinos import Casino
from src.casinos.one_win import OneWin
from src.casinos.mystake import MyStake

class Magnater:
    @staticmethod
    def get_casino(name: str) -> Casino:
        match name.lower():
            case "one_win":
                return OneWin()
            case "mystake":
                return MyStake()
            case _:
                raise ValueError(f"Casino {name} not found")