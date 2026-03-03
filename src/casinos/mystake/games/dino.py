from src.domain import Game
from pydoll.browser.tab import Tab
import asyncio

class Dino(Game):
    def __init__(self, casino: str, url: str):
        super().__init__(casino, url, 'dino')
    
    async def play(self, tab: Tab):
        asyncio.create_task(self._load_strategy(tab))

        while True:
            await asyncio.sleep(3600)
    
    async def _load_strategy(self, tab: Tab):
        pass