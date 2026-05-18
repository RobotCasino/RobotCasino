from abc import ABC, abstractmethod
from pydoll.browser.tab import Tab as PydollTab

class Navigator(ABC):
    
    @abstractmethod
    async def open_tab(self) -> PydollTab:
        pass

    @abstractmethod
    async def close(self) -> None:
        pass

__ALL__ = ['Navigator']