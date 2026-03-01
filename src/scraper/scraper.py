from asyncio import StreamReader, StreamWriter, sleep as asyncio_sleep
import re
import os

from typing import Any, cast
from pydoll.browser.chromium import Chrome
import json

from src.bootstrap import get_chrome_options
from src.casinos import Game
from src.casinos.casino import Casino
from src.ipc.receiver import Receiver
from src.constants import PID_PATH, SOCKET_PATH

from pydoll.protocol.runtime.events import RuntimeEvent
from src.jarvis import Jarvis

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
                    res = self.status()
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

        await self.__tab.enable_runtime_events()

        await self.__tab.set_cookies(cast(Any, self.casino.get_cookies()))
        await self.__tab.go_to(self.game.get_url())

        await self.__tab.on(RuntimeEvent.CONSOLE_API_CALLED, self.__console_watcher)

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
        return f":camera: Screenshot saved to {path}"
    
    async def get_html(self) -> str:
        if self.__tab is None:
            return ""

        html = await self.__tab.page_source

        return html
    
    def status(self) -> str:
        lines = []
        lines.append("╭─ Scraper Status ─╮")
        lines.append(f"  Game:     {self.game.get_name().capitalize()}")
        lines.append(f"  URL:      {self.game.get_url()}")
        lines.append(f"  Strategy: {self.game.get_strategy().capitalize()}")
        lines.append("╰───────────────────╯")
        return "\n".join(lines)
    

    async def __console_watcher(self, message: dict) -> None:
        try:
            params = message.get("params")
            if not isinstance(params, dict):
                return

            args = params.get("args")
            if not isinstance(args, list) or len(args) == 0:
                return

            first = args[0]
            if not isinstance(first, dict) or "value" not in first:
                return

            msg = first['value']
            
            pattern = r'\[([^\]]+)\]'

            match = re.match(pattern, msg)
            
            if not match:
                return

            command = match.group(1)

            match command:
                case "stop":
                    await self.close()
                    SOCKET_PATH.unlink(missing_ok=True)
                    PID_PATH.unlink(missing_ok=True)
                    Jarvis.info("Bye, bye!")
                    os._exit(0)
                case "log":
                        log_message = msg[5:].strip()

                        Jarvis.info(log_message)

        except Exception as e:
            Jarvis.error("Failed to write to console log")
    
__ALL__ = ["Scraper"]