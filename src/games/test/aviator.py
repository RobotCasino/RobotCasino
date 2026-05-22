from src.infrastructure.config import BASE_DIR
from src.domain.scripts.script import Script
from src.domain.games.game import Game
from src.web.tab import Tab

class Aviator(Game):
    def __init__(self):
        name = "aviator"
        display_name = "Aviator"

        playing_scripts: tuple[Script, ...] = (
              Script('First Script',  f'{BASE_DIR}/games/test/scripts/first-script.js'),
              Script('Second Script', f'{BASE_DIR}/games/test/scripts/second-script.js'),
          )

        super().__init__(name, display_name, playing_scripts)

    async def play(self, tab: Tab):
        game = self
        casino = self.get_casino_or_fail()
        strategy = self.get_strategy_or_fail()

        await casino.load_scripts_to_tab_when_playing(tab)
        await game.load_scripts_to_tab_when_playing(tab)
        await strategy.load_scripts_to_tab_when_playing(tab)