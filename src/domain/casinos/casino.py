from src.domain.scripts.script import Script
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from src.web.tab import Tab

class Casino(ABC):
    def __init__(self, name: str, url: str, display_name: str, domain: str) -> None:
        self.__name = name
        self.__url = url
        self.__display_name = display_name
        self.__domain = domain
        self.__metadata: dict[str, Any] = {}

    def set_metadata(self, key: str, value: Any) -> None:
        self.__metadata[key] = value

    def get_metadata(self, key: str) -> Any:
        return self.__metadata.get(key)

    @abstractmethod
    async def prepare(self, tab: "Tab") -> None:
        pass

    def get_name(self):
        return self.__name

    def get_url(self):
        return self.__url
    
    def get_display_name(self):
        return self.__display_name
    
    def get_domain(self):
        return self.__domain
    
    def _set_game_scripts(self, scripts: tuple[Script]):
        self._game_scripts = scripts

    async def load_scripts_to_tab_when_playing(self, tab: "Tab") -> None:
        for script in self._game_scripts:
            await tab.execute_script(script)
