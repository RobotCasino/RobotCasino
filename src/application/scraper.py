import re
import json

from os import remove
from asyncio import StreamReader, StreamWriter

from src.infrastructure.logging.logger import Logger
from src.infrastructure.ipc.receiver import Receiver
from src.infrastructure.config import PID_PATH, SOCKET_PATH

from src.application.tab import Tab
from src.application.browser import Browser
from src.infrastructure.web_navigator import Navigators

class Scraper:
    def __init__(self, browser: str, casino: str , game: str, strategy: str, session: str) -> None:
        self.__browser = browser
        self.__casino = casino
        self.__game = game
        self.__strategy = strategy
        self.__session = session

        self.__active_tab: Tab | None = None

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
                case _:
                  res = f"Unknown command: {command}"
            
            writer.write(json.dumps({"result": res}).encode() + b"\n")
        
        finally:
            writer.close()
            await writer.wait_closed()

    async def run(self):
        navigator = Navigators.get_navigator(self.__browser)

        browser = Browser(navigator)

        tab = await browser.open_tab()

        await tab.console(lambda msg: Logger.info(f"Console log: {msg}"))

        await tab.go_to('https://google.com')

        self.__active_tab = tab

    async def close(self):
        if self.__active_tab:
            try:
                await self.__active_tab.close()
            except Exception:
                pass
            self.__active_tab = None

        if self.__chrome:
            try:
                await self.__chrome.__aexit__(None, None, None) # pyright: ignore
            except Exception:
                pass
            self.__chrome = None

    async def screenshot(self, path: str) -> str:
        if self.__active_tab is None:
            return ":warning: Tab is not initialized."
        
        await self.__active_tab.take_screenshot(path)
        return f":camera: Screenshot saved to {path}"
    
    async def get_html(self) -> str:
        if self.__active_tab is None:
            return ""

        return await self.__active_tab.html()
    
    def status(self) -> str:
        lines: list[str] = []
        lines.append("╭─ Scraper Status ─╮")
        lines.append(f"  Game:     Test")
        lines.append(f"  URL:      Test")
        lines.append(f"  Strategy: Test")
        lines.append("╰───────────────────╯")
        return "\n".join(lines)
    

    async def __console_watcher(self, message: dict[str, str]) -> None: #pyright: ignore
        try:
            params = message.get("params")
            if not isinstance(params, dict):
                return

            args = params.get("args") # pyright: ignore
            if not isinstance(args, list) or len(args) == 0: # pyright: ignore
                return

            first = args[0] # pyright: ignore
            if not isinstance(first, dict) or "value" not in first:
                return

            msg = first['value'] # pyright: ignore
            
            pattern = r'\[([^\]]+)\]'

            match = re.match(pattern, msg) # pyright: ignore
            
            if not match:
                return

            command = match.group(1)

            match command: # pyright: ignore
                case "stop":
                    await self.close()
                    
                    remove(SOCKET_PATH)
                    remove(PID_PATH)

                    Logger.info("Bye, bye!")

                    self.isBetting = False
                case "log":
                    log_message = msg[5:].strip() # pyright: ignore

                    Logger.info(log_message) # pyright: ignore

                    self.isBetting = False
                case "bet":
                    unknown_text: object = msg[5:].strip() # pyright: ignore

                    amount: str = msg[5:].strip() # pyright: ignore

                    if not isinstance(amount, str):
                        return

                    Logger.info(f"Betting {amount}")

                    self.isBetting = True
                case "waiting":
                    self.isBetting = False

        except Exception:
            Logger.error("Failed to write to console log")
    
__ALL__ = ["ScraperService"]
