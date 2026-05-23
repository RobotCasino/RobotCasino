from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from src.domain.scripts.script import Script

if TYPE_CHECKING:
    from src.web.tab import Tab

class Strategy(ABC):

    def __init__(self, playing_scripts: tuple[Script, ...] | tuple[()] = tuple()):
        self._playing_scripts = playing_scripts

    async def load_scripts_to_tab_when_playing(self, tab: "Tab") -> None:
        for script in self._playing_scripts:
           await tab.execute_script(script)

    @abstractmethod
    async def prepare_before_playing(self, tab: "Tab") -> None:
        pass