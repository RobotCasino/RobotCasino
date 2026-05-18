
from src.application.tab import Tab

from src.infrastructure.web_navigator import Navigator

class Browser:
    def __init__(self, navigator: Navigator) -> None:
        self.__navigator = navigator

    async def open_tab(self) -> Tab:
        tab = await self.__navigator.open_tab()

        return Tab(tab)

__ALL__ = ['Browser']