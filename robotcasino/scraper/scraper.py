from asyncio import StreamReader, StreamWriter, sleep as asyncio_sleep
import os
from pathlib import Path
import signal
import sys
from time import sleep
from typing import Any, cast
from pydoll.browser.chromium import Chrome
import rich
import rich.box
import rich.table
import json

from robotcasino.bootstrap import get_chrome_options
from robotcasino.casinos import Game
from robotcasino.casinos.casino import Casino
from robotcasino.ipc.receiver import Receiver
from robotcasino.constants import PID_PATH, SOCKET_PATH

class Scraper:
    
    def __init__(self, casino: Casino , game: Game) -> None:
        self.__chrome = None
        self.__tab = None
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
        self.__chrome = Chrome(options=get_chrome_options())
        
        await self.__chrome.__aenter__()
        
        self.__tab = await self.__chrome.start()
        
        await self.__tab.set_cookies(cast(Any, self.casino.get_cookies()))
        await self.__tab.go_to(self.game.get_url())
        
        await asyncio_sleep(2)
        

        await self.game.play(self.__tab)

    async def close(self):
        if self.__tab:
            try:
                await self.__tab.close()
            except Exception:
                pass
            self.__tab = None

        if self.__chrome:
            try:
                await self.__chrome.__aexit__(None, None, None)
            except Exception:
                pass
            self.__chrome = None
            
    async def screenshot(self, path: str) -> str:
        if self.__tab is None:
            return ":warning: Tab is not initialized."
        
        await self.__tab.take_screenshot(path=path)
        return f":camera: Screenshot saved to [bold]{path}[/bold]"
    
    async def get_html(self) -> str:
        if self.__tab is None:
            return ""

        html = await self.__tab.page_source

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
    
    def __console_watcher(self, message: Any) -> None:
        Path("./logs/scraper_console.log").parent.mkdir(parents=True, exist_ok=True)
        with Path("./logs/scraper_console.log").open("a", encoding="utf-8") as f:
            f.write(str(message) + "\n")
    
__ALL__ = ["Scraper"]