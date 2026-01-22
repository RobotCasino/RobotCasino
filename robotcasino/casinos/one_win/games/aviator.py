from robotcasino.casinos import Game
from robotcasino.casinos import Strategier
from pydoll.browser.tab import Tab
from asyncio import sleep

from robotcasino.casinos import Casino

class Aviator(Game):

    def __init__(self, casino: str, url: str):
        super().__init__(casino, url, 'aviator')

    async def play(self, tab: Tab):
        await sleep(999999)  # Sleep indefinitely for debugging

__ALL__ = ['Aviator']