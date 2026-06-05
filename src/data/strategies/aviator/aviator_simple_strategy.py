from core.domain.strategies.strategy import Strategy
from core.domain.scripts.script import Script
from common.constants.directories import BASE_DIR
from data.web.tab import Tab

class AviatorSimpleStrategy(Strategy):

    def __init__(self):
        playing_scripts: tuple[Script, ...] = (
            Script('Simple Strategy',  f'{BASE_DIR}data/strategies/scripts/aviator-simple-strategy.js'),
        )

        super().__init__("aviator_simple_strategy", "Aviator Simple Strategy", playing_scripts)
    
    async def prepare_before_playing(self, tab: Tab) -> None:
        pass