from abc import ABC, abstractmethod
from pydoll.browser.tab import Tab as PydollTab

class Navigator(ABC):
    
    @abstractmethod
    async def open_tab(self) -> PydollTab:
        pass

    @abstractmethod
    async def close(self) -> None:
        pass

    @abstractmethod
    def is_optimized_for_low_memory(self) -> bool:
        pass

    async def get_memory_usage_bytes(self) -> int | None:
        return None

__ALL__ = ['Navigator']