from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from src.infrastructure.config import BASE_DIR
from src.core.domain.scripts.script import Script

if TYPE_CHECKING:
    from data.web.tab import Tab

class Strategy(ABC):

    def __init__(self, name: str, display_name: str, playing_scripts: tuple[Script, ...] | tuple[()] = tuple()):
        verification_scripts: tuple[Script, ...] = (
            Script("Provider", f"{BASE_DIR}/domain/strategies/scripts/provider.js"),
        )
       
        self._playing_scripts = verification_scripts + playing_scripts
        
        self.__name = name
        self.__display_name = display_name

    def get_name(self):
        return self.__name
    
    def get_display_name(self):
        return self.__display_name

    async def load_scripts_to_tab_when_playing(self, tab: "Tab") -> None:
        for script in self._playing_scripts:
           await tab.execute_script(script)

    @abstractmethod
    async def prepare_before_playing(self, tab: "Tab") -> None:
        pass

