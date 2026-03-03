from abc import ABC, abstractmethod
from typing import Any, Dict, List


class BrowserPort(ABC):
    """Interface defining what the domain expects from a browser implementation.
    
    This port establishes the contract between the domain layer and any browser
    automation adapter. Currently, game implementations still use pydoll's Tab
    directly for fine-grained control, but this interface defines the high-level
    operations used by the application layer (ScraperService).
    """

    @abstractmethod
    async def start(self) -> None:
        """Initialize the browser and open a new tab."""
        pass

    @abstractmethod
    async def navigate(self, url: str) -> None:
        """Navigate the active tab to the given URL."""
        pass

    @abstractmethod
    async def set_cookies(self, cookies: List[Dict[str, Any]]) -> None:
        """Set cookies on the browser before navigation."""
        pass

    @abstractmethod
    async def take_screenshot(self, path: str) -> None:
        """Capture a screenshot and save it to the given path."""
        pass

    @abstractmethod
    async def get_page_source(self) -> str:
        """Return the full HTML source of the current page."""
        pass

    @abstractmethod
    async def close(self) -> None:
        """Close the browser and clean up resources."""
        pass
