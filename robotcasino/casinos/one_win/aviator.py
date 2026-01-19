from pprint import pprint
from robotcasino.casinos import Game
from robotcasino.casinos.strategies.strategier import Strategier
from playwright.async_api import Page

class Aviator(Game):

    def __init__(self, strategy = 'default'):
        super().__init__('one_win', 'aviator', 'https://1win.com/casino/play/v_spribe:aviator', strategy)

    async def play(self, page: Page):
        strategy = Strategier.get_strategy_as_dict(self.get_casino(), self.get_name(), self.get_strategy())

        await page.context.add_cookies([{
            
        }])

        await page.goto(self.get_url())

        await page.pause()

__ALL__ = ['Aviator']