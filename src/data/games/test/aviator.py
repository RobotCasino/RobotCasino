from src.infrastructure.config import BASE_DIR
from core.domain.scripts.script import Script
from core.domain.games.game import Game
from data.web.tab import Tab

class Aviator(Game):
    def __init__(self):
        name = "aviator"
        display_name = "Aviator"
        url = "https://testcasino.com"

        playing_scripts: tuple[Script, ...] = (
              Script('First Script',  f'{BASE_DIR}/games/test/scripts/first-script.js'),
              Script('Second Script', f'{BASE_DIR}/games/test/scripts/second-script.js'),
          )

        game_domain_scripts: tuple[Script, ...] = (
            Script('Domain Game Script', f'{BASE_DIR}/domain/games/scripts/aviator.js'),
        )

        super().__init__(name, display_name, url, playing_scripts, game_domain_scripts)

    async def play(self, tab: Tab):
        strategy = self.get_strategy_or_fail()
        casino = self.get_casino_or_fail()

        await self.load_scripts_to_tab_when_playing(tab)
        await casino.load_scripts_to_tab_when_playing(tab)
        await strategy.load_scripts_to_tab_when_playing(tab)