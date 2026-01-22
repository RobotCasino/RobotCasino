from asyncio import StreamReader, StreamWriter, sleep as asyncio_sleep
import os
import sys
from time import sleep
from typing import Any, cast
from pydoll.browser.chromium import Chrome
from pydoll.browser.options import ChromiumOptions
import rich
import rich.box
import rich.table
import json

from robotcasino.casinos import Game
from robotcasino.casinos.casino import Casino
from robotcasino.ipc.receiver import Receiver

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
        options = ChromiumOptions()
        
        options.headless = True
        options.binary_location = "/usr/bin/google-chrome-stable"
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-web-security")
        options.add_argument("--disable-features=IsolateOrigins,site-per-process")
        options.add_argument("--disable-blink-features=AutomationControlled")
        
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-software-rasterizer")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-plugins")
        options.add_argument("--disable-background-networking")
        options.add_argument("--disable-background-timer-throttling")
        options.add_argument("--disable-backgrounding-occluded-windows")
        options.add_argument("--disable-breakpad")
        options.add_argument("--disable-component-extensions-with-background-pages")
        options.add_argument("--disable-features=TranslateUI,BlinkGenPropertyTrees")
        options.add_argument("--disable-ipc-flooding-protection")
        options.add_argument("--disable-renderer-backgrounding")
        options.add_argument("--enable-features=NetworkService,NetworkServiceInProcess")
        options.add_argument("--force-color-profile=srgb")
        options.add_argument("--hide-scrollbars")
        options.add_argument("--metrics-recording-only")
        options.add_argument("--mute-audio")
        
        # Resource limits
        options.add_argument("--max-old-space-size=512")
        options.add_argument("--memory-pressure-off")
        
        # Minimal viewport
        options.add_argument("--window-size=800,600")
        options.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        self.__chrome = Chrome(options=options)
        await self.__chrome.__aenter__()
        
        self.__tab = await self.__chrome.start()
        
        await self.__tab.set_cookies(cast(Any, self.casino.get_cookies()))
        await self.__tab.go_to(self.game.get_url())

        # Event listeners can be added here if needed
        # await self.__tab.on("console", lambda msg: print(msg.text, file=sys.stderr))

        await asyncio_sleep(5)

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
    
__ALL__ = ["Scraper"]