from pydoll.elements.web_element import WebElement
from robotcasino.casinos import Game, Strategier, Scripter
from pydoll.browser.tab import Tab
from pydoll.constants import By
import asyncio

class Aviator(Game):

    def __init__(self, casino: str, url: str):
        super().__init__(casino, url, 'aviator')

    async def play(self, tab: Tab):
        await self.__select_and_init_game(tab)

        iframe = await self.__get_iframe(tab)
        
        asyncio.create_task(self._load_strategy(iframe))

        while True:
            await asyncio.sleep(3600)

    async def _load_strategy(self, iframe: WebElement):
        utils_script = Scripter.get_game_utils_script()
        general_script = Scripter.get_general_game_script(self.get_casino(), self.get_name())
        domain_script = Scripter.get_game_domain_script(self.get_name())
        strategy_script = Strategier.get_strategy_script_with_payload(
            self.get_name(),
            self.get_strategy(),
            self.get_user_data()
        )

        await iframe.execute_script(utils_script)
        await iframe.execute_script(domain_script)
        await iframe.execute_script(strategy_script)
        await iframe.execute_script(general_script)
        
    async def __select_and_init_game(self, tab: Tab):      
        play_btn = await tab.find_or_wait_element(
            by=By.CSS_SELECTOR,
            value='button.base_root-9EwpE.base_size-xl-9EwpE.base_variant-primary-9EwpE',
            timeout=280,
            raise_exc=True
        )

        if isinstance(play_btn, WebElement):
            await play_btn.click()

    async def __get_iframe(self, tab: Tab) -> WebElement:
        iframe_element = await tab.find_or_wait_element(by=By.TAG_NAME, value='iframe', raise_exc=False)

        if not isinstance(iframe_element, WebElement):
            raise ValueError('Aviator iframe element not found')
    
        return iframe_element

__ALL__ = ['Aviator']