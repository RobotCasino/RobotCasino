from src.domain.strategies.strategy import Strategy
from src.domain.scripts.script import Script
from src.infrastructure.config import BASE_DIR

class SimpleStrategy(Strategy):

    def __init__(self):
        playing_scripts: tuple[Script] = (
            Script('Simple Strategy',  f'{BASE_DIR}/games/scripts/aviator-simple-strategy.js'),
        )

        super().__init__(playing_scripts)