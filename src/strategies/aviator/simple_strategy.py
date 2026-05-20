from src.domain.strategies.strategy import Strategy
from src.domain.scripts.script import Script

class SimpleStrategy(Strategy):

    def __init__(self):
        self.scripts: tuple[Script] = (
            Script('Simple Strategy', '/games/scripts/aviator-simple-strategy.js'),
        )

        super().__init__(self.scripts)