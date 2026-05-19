from pydoll.browser.tab import Tab as PydollTab
from pydoll.protocol.runtime.events import RuntimeEvent
from collections.abc import Callable

from src.navigators import Cookie
from src.domain import Script

from src.web.element import Element

class Tab:
    def __init__(self, tab: PydollTab) -> None:
        self.__cookies: list[Cookie] = []

        self.__page = tab

    async def add_cookie(self, cookie: Cookie):
        self.__cookies.append(cookie)

        return await self.update_cookies()
    
    async def clear_cookies(self):
        self.__cookies.clear()

        return await self.update_cookies()

    async def go_to(self, url: str):
        await self.__page.go_to(url)

    async def update_cookies(self) -> None:
        if len(self.__cookies) == 0:
            await self.__page.delete_all_cookies()
            return

        cookies = [c.to_dict() for c in self.__cookies]

        await self.__page.set_cookies(cookies) # pyright: ignore
    
    async def take_screenshot(self, path: str) -> None:
        await self.__page.take_screenshot(path=path)
    
    async def close(self) -> None:
        await self.__page.close()

    async def html(self) -> str:
        return await self.__page.page_source
    
    async def console(self, callback: Callable[[dict[str, str]], None]) -> None:
        await self.__page.enable_runtime_events()

        await self.__page.on(RuntimeEvent.CONSOLE_API_CALLED, callback) # pyright: ignore

    async def find_element(self, element: str) -> Element | None:
        pass

    async def execute_script(self, script: Script) -> None:
        await self.__page.execute_script(script)

__ALL__ = ['Tab']