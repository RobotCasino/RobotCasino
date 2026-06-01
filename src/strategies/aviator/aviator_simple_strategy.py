from src.domain.strategies.strategy import Strategy
from src.domain.scripts.script import Script
from src.infrastructure.config import BASE_DIR
from src.web.tab import Tab

class AviatorSimpleStrategy(Strategy):

    def __init__(self):
        playing_scripts: tuple[Script, ...] = (
            Script('Simple Strategy',  f'{BASE_DIR}/strategies/scripts/aviator-simple-strategy.js'),
        )

        super().__init__("aviator_simple_strategy", "Aviator Simple Strategy", playing_scripts)
    
    async def prepare_before_playing(self, tab: Tab) -> None:
        pass