from abc import ABC, abstractmethod

from typing import TYPE_CHECKING

from src.domain.strategies.strategy import Strategy
from src.domain.casinos.casino import Casino

from src.infrastructure.config import BASE_DIR
from src.domain.scripts.script import Script

if TYPE_CHECKING:
    from src.web.tab import Tab

class Game(ABC):
    def __init__(self, name: str, url: str, playing_scripts: tuple['Script', ...] | tuple[()] = tuple(), domain_scripts: tuple['Script', ...] | tuple[()] = tuple()):
        self.__name = name
        self.__url = url

        self.__strategy: Strategy | None = None
        self.__casino: Casino | None = None

        self._playing_scripts = playing_scripts
        self._domain_scripts = domain_scripts 

        self.__util_scripts: tuple['Script', ...] = (
            Script('Util Script', f'{BASE_DIR}/domain/games/scripts/util.js'),
            Script('Scraper Util Script', f'{BASE_DIR}/domain/games/scripts/scraper.js'),
        )

    @abstractmethod
    async def play(self, tab: 'Tab') -> None:
        pass

    def get_name(self):
        return self.__name

    def get_url(self):
        return self.__url
    
    def get_casino(self):
        return self.__casino

    def get_strategy(self):
        return self.__strategy
    
    def get_casino_or_fail(self) -> Casino:
        if self.__casino is None:
            raise ValueError('Casino not loaded')
        return self.__casino
    
    def get_strategy_or_fail(self) -> Strategy:
        if self.__strategy is None:
            raise ValueError('Strategy not loaded')
        return self.__strategy

    def set_strategy(self, strategy: Strategy):
        self.__strategy = strategy

    def set_casino(self, casino: Casino):
        self.__casino = casino

    def is_ready_or_fail(self) -> None:
        if self.__strategy is None or self.__casino is None:
            raise ValueError("Game is not ready. Missing strategy or casino.")
        
    async def load_scripts_to_tab_when_playing(self, tab: 'Tab'):
        for script in self.__util_scripts:
            await tab.execute_script(script)

        for script in self._playing_scripts:
            await tab.execute_script(script)
            
        for script in self._domain_scripts:
            await tab.execute_script(script)