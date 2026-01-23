import asyncio

from robotcasino.bootstrap import get_game_js_script
from robotcasino.casinos import Game
from pydoll.browser.tab import Tab
from pydoll.constants import By
from pydoll.elements.web_element import WebElement
from pydoll.exceptions import IFrameNotFound
from asyncio import sleep

class Aviator(Game):

    def __init__(self, casino: str, url: str):
        super().__init__(casino, url, 'aviator')

    async def play(self, tab: Tab):
        await self.__select_and_init_game(tab)

        iframe = await self.__get_iframe(tab)
        
        await self.__close_chat(iframe)
             
        asyncio.create_task(self.__load_script(iframe))

        while True:
            await asyncio.sleep(3600)

    async def __close_chat(self, iframe: Tab):
        close_btn = await iframe.find_or_wait_element(
            by=By.CSS_SELECTOR,
            value='button.close',
            timeout=10,
            raise_exc=False
        )

        if isinstance(close_btn, WebElement):
            await close_btn.click()
    
    async def __load_script(self, iframe: Tab):
        script = get_game_js_script(self.get_casino(), self.get_name())

        await iframe.execute_script(script)
    
    async def __select_and_init_game(self, tab: Tab):
        # document.querySelector('button.base_root-9EwpE.base_size-xl-9EwpE.base_variant-primary-9EwpE')
        
        play_btn = await tab.find_or_wait_element(
            by=By.CSS_SELECTOR,
            value='button.base_root-9EwpE.base_size-xl-9EwpE.base_variant-primary-9EwpE',
            timeout=10,
            raise_exc=True
        )

        await play_btn.click()

    async def __get_iframe(self, tab: Tab) -> Tab:
        iframe_element = await tab.find_or_wait_element(by=By.TAG_NAME, value='iframe', raise_exc=True)

        if not isinstance(iframe_element, WebElement):
            raise ValueError('Aviator iframe element not found')
        
        src = iframe_element.get_attribute('src')
        
        if not src or src.strip() == '':
            raise ValueError('Iframe src attribute is empty or invalid')
        
        frame = None
        
        for _ in range(40):
            try:
                frame = await tab.get_frame(iframe_element)

                

            except IFrameNotFound:
                await asyncio.sleep(0.25) 
        
        if frame is None:
            raise IFrameNotFound('Aviator iframe not found after multiple attempts')

        iframe = frame

        return iframe

  

__ALL__ = ['Aviator']