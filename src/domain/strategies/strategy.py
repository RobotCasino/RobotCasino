from abc import ABC
from typing import TYPE_CHECKING, Any
from src.domain.scripts.script import Script

if TYPE_CHECKING:
    from src.web.tab import Tab

class Strategy(ABC):

    def __init__(self, scripts: tuple[Script]):
        self._scripts = scripts
        self.__metadata: dict[str, Any] = {}

    def set_metadata(self, key: str, value: Any) -> None:
        self.__metadata[key] = value

    def get_metadata(self, key: str) -> Any:
        return self.__metadata.get(key)

    async def load_scripts_to_tab_when_playing(self, tab: "Tab") -> None:
        for script in self._scripts:
           await tab.execute_script(script)