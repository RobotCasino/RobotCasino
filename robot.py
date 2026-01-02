import os
from playwright.async_api import async_playwright

class Robot:
    
    def __init__(self) -> None:
        self.__browser = None
        self.__page = None
        self.__playwright = None

    async def run(self):

        self.__playwright = await async_playwright().start()

        self.__browser = await self.__playwright.chromium.launch(headless=False)

        self.__page = await self.__browser.new_page()

        await self.__page.goto("https://1win.lat/")

        await self.__page.pause()

    async def close(self):
        if self.__browser:
            await self.__browser.close()
        if self.__playwright:
            await self.__playwright.stop()

    async def screenshot(self, path: str) -> None:
        if self.__page:
            await self.__page.screenshot(path=path)

    def get_pid(self) -> int:
        return os.getpid()

__ALL__ = ["Robot"]