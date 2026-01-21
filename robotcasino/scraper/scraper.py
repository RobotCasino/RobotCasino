from asyncio import StreamReader, StreamWriter
import os
import sys
from time import sleep
from typing import Any, cast
from playwright.async_api import async_playwright as _async_playwright
import rich
import rich.box
import rich.table
import json

from robotcasino.casinos import Game
from robotcasino.casinos.casino import Casino
from robotcasino.ipc.receiver import Receiver

class Scraper:
    
    def __init__(self, casino: Casino , game: Game) -> None:
        self.__browser = None
        self.__page = None
        self.__playwright = None
        self.__context = None
        self.casino = casino
        self.game = game
        

    async def controller(self, reader: StreamReader, writer: StreamWriter):
        try:
            receiver = await Receiver.create(reader)

            command = receiver.get_command()
            arg = receiver.get_parameters()

            res = None

            match command:
                case "status":
                    self.status()
                case "screenshot":
                  res = await self.screenshot(arg)
                case "get_html":
                  res = await self.get_html()
            
            if res is not None:
                writer.write(json.dumps({"result": res}).encode() + b"\n")
        
        finally:
            writer.close()
            await writer.wait_closed()

    async def run(self):
        self.__playwright = await _async_playwright().start()

        self.__browser = await self.__playwright.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--mute-audio",
                "--disable-web-security",
                "--disable-features=IsolateOrigins,site-per-process",
                "--disable-blink-features=AutomationControlled",
            ],
        )

        self.__context = await self.__browser.new_context(
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080},
            locale="es-MX",
            timezone_id="America/Mexico_City",
        )

        self.__page = await self.__context.new_page()
        self.__page.set_default_navigation_timeout(5000)

        await self.__page.context.add_cookies(cast(Any, self.casino.get_cookies()))

        await self.__page.goto(self.game.get_url())

        # self.__page.on("console", lambda msg: print(msg.text, file=sys.stderr))
        # self.__page.on("pageerror", lambda exc: print("PageError:", exc, file=sys.stderr))

        await self.__page.wait_for_timeout(5000)

        await self.game.play(self.__page)
        
    async def close(self):
        if self.__page:
            try:
                await self.__page.close()
            except Exception:
                pass
            self.__page = None

        if self.__browser:
            try:
                await self.__browser.close()
            except Exception:
                pass
            self.__browser = None

        if self.__playwright:
            try:
                await self.__playwright.stop()
            except Exception:
                pass
            self.__playwright = None

    async def screenshot(self, path: str) -> str:
        if self.__page is None:
            return ":warning: Page is not initialized."
        
        await self.__page.screenshot(path=path)
        return f":camera: Screenshot saved to [bold]{path}[/bold]"
    
    async def get_html(self) -> str:
        if self.__page is None:
            return ""

        html = await self.__page.content()

        return html
    
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