from src.infrastructure.config import BASE_DIR
from core.domain.games.game import Game
from data.web.tab import Tab
from data.web.element import Element
from core.domain.scripts.script import Script

class Aviator(Game):

    def __init__(self):
        playing_scripts: tuple[Script, ...] = (
            Script("Cleaner Script", f"{BASE_DIR}/games/one_win/scripts/aviator-cleaner.js"),
            Script("Playground Script", f"{BASE_DIR}/games/one_win/scripts/aviator-playground.js"),
        )

        game_domain_scripts: tuple[Script, ...] = (
            Script('Domain Game Script', f'{BASE_DIR}/domain/games/scripts/aviator.js'),
        )

        super().__init__("aviator", "Aviator", "https://1win.com/casino/play/v_spribe:aviator", playing_scripts=playing_scripts, domain_scripts=game_domain_scripts)

    async def play(self, tab: Tab):
        casino = self.get_casino_or_fail()
        strategy = self.get_strategy_or_fail()

        await tab.go_to(self.get_url())
    
        await tab.reload()

        await tab.sleep(5)

        await self.set_game_balance_currency(tab)
        await self.wait_for_aviator_iframe_to_load(tab)

        await tab.sleep(2)

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

        await tab.sleep(2)

    async def wait_for_aviator_iframe_to_load(self, tab: Tab) -> None:
        iframe = await tab.find_element_by_xpath_or_fail("//iframe[contains(@src, 'spribelaunch.com/aviator')]")
        await iframe.find_element_by_xpath_or_fail("//div[@class = 'game-logo']")

__ALL__ = ['Aviator']