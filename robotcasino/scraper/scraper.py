from asyncio import StreamReader, StreamWriter
import os
from typing import Any, cast
from playwright.async_api import async_playwright as _async_playwright
import rich
import rich.box
import rich.table

from robotcasino.casinos import Game
from robotcasino.casinos.casino import Casino
from robotcasino.ipc.receiver import Receiver

class Scraper:
    
    def __init__(self, casino: Casino , game: Game) -> None:
        self.__browser = None
        self.__page = None
        self.__playwright = None
        self.casino = casino
        self.game = game
        

    async def controller(self, reader: StreamReader, writer: StreamWriter):
        try:
            receiver = await Receiver.create(reader)

            command = receiver.get_command()
            arg = receiver.get_parameters()

            match command:
                case "screenshot":
                    return await self.screenshot(arg)
                case "status":
                    return self.status()
        finally:
            writer.close()
            await writer.wait_closed()

    async def run(self):
        self.__playwright = await _async_playwright().start()

        self.__browser = await self.__playwright.chromium.launch(headless=False)

        self.__page = await self.__browser.new_page()

        await self.__page.goto(self.game.get_url())

        await self.__page.context.add_cookies(cast(Any, self.casino.get_cookies()))

        await self.__page.reload()

        await self.game.play(self.__page)
        
    async def close(self):
        if self.__browser:
            await self.__browser.close()
        if self.__playwright:
            await self.__playwright.stop()

    async def screenshot(self, path: str) -> None:
        if self.__page:
            await self.__page.screenshot(path=path)
            rich.print(f":camera: Screenshot saved to [bold]{path}[/bold]")
    
    def status(self) -> None:
        table = rich.table.Table(title="Scraper Status", box=rich.box.ROUNDED, show_edge=True)
        table.add_column("Prop", style="cyan", no_wrap=True)
        table.add_column("Value", style="magenta")
        table.add_row("Game", self.game.get_name().capitalize())
        table.add_row("URL", self.game.get_url())
        table.add_row("Strategy", self.game.get_strategy().capitalize())
        rich.print(table)

    def get_pid(self) -> int:
        return os.getpid()
    
__ALL__ = ["Scraper"]