from src.domain.strategies.strategy import Strategy
from src.domain.scripts.script import Script
from src.web.tab import Tab

class DinoSimpleStrategy(Strategy):

    def __init__(self):
        playing_scripts: tuple[Script, ...] = (
        )

        super().__init__("dino_simple_strategy", "Dino Simple Strategy", playing_scripts)
    
    async def prepare_before_playing(self, tab: Tab) -> None:
        pass