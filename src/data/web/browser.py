
from data.web.tab import Tab

from data.navigators.navigator import Navigator

class Browser:
    def __init__(self, navigator: Navigator) -> None:
        self.__navigator = navigator

    async def open_tab(self) -> Tab:
        tab = await self.__navigator.open_tab()

        return Tab(tab)
    
    async def close(self):
        await self.__navigator.close()

__ALL__ = ['Browser']