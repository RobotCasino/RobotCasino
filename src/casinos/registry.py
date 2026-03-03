from src.domain.casino import Casino
from src.casinos.one_win import OneWin
from src.casinos.mystake import MyStake

class CasinoRegistry:
    @staticmethod
    def get_casino(name: str) -> Casino:
        match name.lower():
            case "one_win":
                return OneWin()
            case "mystake":
                return MyStake()
            case _:
                raise ValueError(f"Casino {name} not found")
