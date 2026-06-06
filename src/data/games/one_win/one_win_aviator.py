import asyncio

from common.constants.directories import BASE_DIR
from core.domain.games.game import Game
from data.web.tab import Tab
from core.domain.scripts.script import Script

class OneWinAviator(Game):

    def __init__(self):
        playing_scripts: tuple[Script, ...] = (
            Script("Game Cleaner Script", f"{BASE_DIR}core/domain/games/scripts/aviator-cleaner.js"),
            Script("Playground Script", f"{BASE_DIR}data/games/one_win/scripts/aviator-playground.js"),
        )

        game_domain_scripts: tuple[Script, ...] = (
            Script('Domain Game Script', f'{BASE_DIR}core/domain/games/scripts/aviator-domain.js'),
        )

        super().__init__("aviator", "Aviator", "https://1win.com/casino/play/v_spribe:aviator", playing_scripts=playing_scripts, domain_scripts=game_domain_scripts)

    async def play(self, tab: Tab):
        casino = self.get_casino_or_fail()
        strategy = self.get_strategy_or_fail()

        await tab.go_to(self.get_url())
    
        await tab.reload()

        await tab.sleep(2)

        async with asyncio.TaskGroup() as tg:
           tg.create_task(self.set_game_balance_currency(tab))
           tg.create_task(self.wait_for_aviator_iframe_to_load(tab))

        await tab.sleep(10)

        await self.load_scripts_to_tab_when_playing(tab)
        await casino.load_scripts_to_tab_when_playing(tab)
        await strategy.load_scripts_to_tab_when_playing(tab)

    async def set_game_balance_currency(self, tab: Tab):
        currency_panel = await tab.find_element_by_xpath_or_fail("//div[@class = 'game-play-card_currencyButton-bVSBd']/parent::div")

        await currency_panel.click()
        
        await tab.sleep(1)

        currency_button = await tab.find_element_by_xpath_or_fail("//div[text() = 'USD']/ancestor::button")

        await currency_button.click()
        
        await tab.sleep(1)

        play_button = await tab.find_element_by_xpath_or_fail("//div[text() = 'Play']/ancestor::button")

        await play_button.click_by_cdp()

    async def wait_for_aviator_iframe_to_load(self, tab: Tab) -> None:
        iframe = await tab.find_element_by_xpath_or_fail("//iframe[contains(@src, 'spribelaunch.com/aviator')]")
        # await iframe.find_element_by_css_selector_or_fail("app-bet-control")


__ALL__ = ['OneWinAviator']