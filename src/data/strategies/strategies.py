from data.strategies.aviator.aviator_simple_strategy import AviatorSimpleStrategy
from data.strategies.dino.dino_simple_strategy import DinoSimpleStrategy

from enum import Enum

class Strategies(Enum):
    AVIATOR_SIMPLE_STRATEGY = AviatorSimpleStrategy()
    DINO_SIMPLE_STRATEGY = DinoSimpleStrategy()
    
    @staticmethod
    def get_strategy_or_fail(game: str, strategy_name: str):
        match f"{game.lower()}-{strategy_name.lower()}":
            case "aviator-simple-strategy":
                return Strategies.AVIATOR_SIMPLE_STRATEGY.value
            case "dino-simple-strategy":
                return Strategies.DINO_SIMPLE_STRATEGY.value
            case _:
                raise ValueError(f"Unknown strategy: {strategy_name}")