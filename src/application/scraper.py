import re
import json

from pathlib import Path
from asyncio import StreamReader, StreamWriter

from src.infrastructure.logging.logger import Logger
from src.infrastructure.ipc.receiver import Receiver
from src.infrastructure.config import PID_PATH, SOCKET_PATH

from src.web.tab import Tab
from src.web.browser import Browser

from src.navigators import Navigators
from src.games import Games
from src.casinos import Casinos
from src.strategies import Strategies

class Scraper:
    def __init__(self, browser: str, casino: str , game: str, strategy: str, session: str) -> None:
        Logger.info(f"Starting scraper with browser={browser}, casino={casino}, game={game}, strategy={strategy}, session={session}")

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
                case "html":
                  res = await self.html()
                case _:
                  res = f"Unknown command: {command}"
            
            writer.write(json.dumps({"result": res}).encode() + b"\n")
        
        finally:
            writer.close()
            await writer.wait_closed()

    async def run(self):
        navigator = Navigators.get_navigator_or_fail(self.__browser)
        casino = Casinos.get_casino_or_fail(self.__casino)
        game = Games.get_game_or_fail(self.__casino, self.__game)
        strategy = Strategies.get_strategy_or_fail(self.__game, self.__strategy)

        game.load_strategy(strategy)

        browser = Browser(navigator)

        tab = await browser.open_tab()

        await tab.console(self.__watcher) # pyright: ignore

        await game.play(tab)

    async def close(self):
        if self.__active_tab:
            try:
                await self.__active_tab.close()
            except Exception:
                pass
            self.__active_tab = None

    async def screenshot(self, path: str) -> str:
        if self.__active_tab is None:
            return ":warning: Tab is not initialized."
        
        await self.__active_tab.take_screenshot(path)
        return f":camera: Screenshot saved to {path}"
    
    async def html(self) -> str:
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
    

    async def __watcher(self, message: object) -> None:
        params = message.get("params")
        if not isinstance(params, dict):
            return
        
        args = params.get("args")
        if not isinstance(args, list) or not args:
            return

        first_arg = args[0]
        if not isinstance(first_arg, dict):
            return

        msg = first_arg.get("value")
        if not isinstance(msg, str):
            return
            
        match = re.search(r'\[([^\]]+)\]', msg)
        if not match:
            return

        command = match.group(1)
        payload = msg[len(match.group(0)):].strip()

        match command:
            case "stop":
                await self.close()
                Path(SOCKET_PATH).unlink(missing_ok=True)
                Path(PID_PATH).unlink(missing_ok=True)
                Logger.info("Bye, bye!")
                
                if hasattr(self, "isBetting"):
                    self.isBetting = False # type: ignore
            case "log":
                Logger.info(payload)
                if hasattr(self, "isBetting"):
                    self.isBetting = False # type: ignore
            case "bet":
                Logger.info(f"Betting {payload}")
                if hasattr(self, "isBetting"):
                    self.isBetting = True # type: ignore
            case "waiting":
                if hasattr(self, "isBetting"):
                    self.isBetting = False # type: ignore

__ALL__ = ["ScraperService"]
