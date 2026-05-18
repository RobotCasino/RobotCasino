from src.strategies.aviator.simple_strategy import AviatorSimpleStrategy

from enum import Enum

class Strategies(Enum):
    AVIATOR_SIMPLE_STRATEGY = AviatorSimpleStrategy()
    
    @staticmethod
    def get_strategy_or_fail(game: str, strategy_name: str):
        match f"{game.lower()}-{strategy_name.lower()}":
            case "aviator-simple-strategy":
                return Strategies.AVIATOR_SIMPLE_STRATEGY.value
            case _:
                raise ValueError(f"Unknown strategy: {strategy_name}")