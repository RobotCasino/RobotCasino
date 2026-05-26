from src.domain.strategies.strategy import Strategy
from src.domain.scripts.script import Script
from src.infrastructure.config import BASE_DIR
from src.web.tab import Tab

class SimpleStrategy(Strategy):

    def __init__(self):
        playing_scripts: tuple[Script, ...] = (
        )

        super().__init__(playing_scripts)
    
    async def prepare_before_playing(self, tab: Tab) -> None:
        pass