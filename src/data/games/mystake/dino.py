from src.infrastructure.config import BASE_DIR
from core.domain.games.game import Game
from data.web.tab import Tab
from core.domain.scripts.script import Script

class Dino(Game):

    def __init__(self):
        name = "dino"
        display_name = "Dino"
        url = "https://m.mystake.com/es/casino/gamepage?gameid=12489"

        playing_scripts: tuple[Script, ...] = (
        )

        game_domain_scripts: tuple[Script, ...] = (
        )

        super().__init__(name, display_name, url, playing_scripts, game_domain_scripts)

    async def play(self, tab: Tab):
        casino = self.get_casino_or_fail()
        strategy = self.get_strategy_or_fail()

        await tab.go_to(self.get_url())
    
        await tab.reload()

        await self.load_scripts_to_tab_when_playing(tab)
        await casino.load_scripts_to_tab_when_playing(tab)
        await strategy.load_scripts_to_tab_when_playing(tab)


__ALL__ = ['Dino']