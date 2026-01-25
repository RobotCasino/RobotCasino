import asyncio

from robotcasino.bootstrap import get_game_error_script, get_game_js_script
from robotcasino.casinos import Game, Strategier
from pydoll.browser.tab import Tab
from pydoll.constants import By
from pydoll.elements.web_element import WebElement

class Aviator(Game):

    def __init__(self, casino: str, url: str):
        super().__init__(casino, url, 'aviator')

    async def play(self, tab: Tab):
        await self.__select_and_init_game(tab)

        iframe = await self.__get_iframe(tab)
        
        asyncio.create_task(self.__load_script(iframe))

        while True:
            await asyncio.sleep(3600)

    async def __load_script(self, iframe: WebElement):
        error = get_game_error_script()
        script = get_game_js_script(self.get_casino(), self.get_name())

        script = script.replace('[strategy]', Strategier.get_strategy_as_string(self.get_name(), self.get_strategy()))

        await iframe.execute_script(error)
        await iframe.execute_script(script)
    
    async def __select_and_init_game(self, tab: Tab):      
        play_btn = await tab.find_or_wait_element(
            by=By.CSS_SELECTOR,
            value='button.base_root-9EwpE.base_size-xl-9EwpE.base_variant-primary-9EwpE',
            timeout=10,
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