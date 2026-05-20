from abc import ABC, abstractmethod

from typing import TYPE_CHECKING, Any

from src.domain.strategies.strategy import Strategy
from src.domain.casinos.casino import Casino

if TYPE_CHECKING:
    from src.web.tab import Tab

class Game(ABC):
    def __init__(self, name: str, url: str):
        self.__name = name
        self.__url = url
        self.__metadata: dict[str, Any] = {}

        self.__strategy: Strategy | None = None
        self.__casino: Casino | None = None

    def set_metadata(self, key: str, value: Any) -> None:
        self.__metadata[key] = value

    def get_metadata(self, key: str) -> Any:
        return self.__metadata.get(key)

    @abstractmethod
    async def play(self, tab: 'Tab'):
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