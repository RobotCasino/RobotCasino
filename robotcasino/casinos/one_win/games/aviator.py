from robotcasino.casinos import Game
from robotcasino.casinos import Strategier
from playwright.async_api import Page

from robotcasino.casinos import Casino

class Aviator(Game):

    def __init__(self, casino: str, url: str):
        super().__init__(casino, url, 'aviator')

    async def play(self, page: Page):
        await page.pause()

__ALL__ = ['Aviator']