from enum import Enum
import json

from asyncio import StreamReader, StreamWriter

from src.infrastructure.process.resources import Resources

from src.infrastructure.logging.logger import Logger
from src.infrastructure.ipc.receiver import Receiver
from src.infrastructure.process.foreground import ForegroundProcess

from src.web.tab import Tab
from src.web.browser import Browser

from src.navigators.navigators import Navigators
from src.games.games import Games
from src.casinos.casinos import Casinos
from src.strategies.strategies import Strategies

from src.utils.metadata import Metadata
from src.utils.browser_console import BrowserConsole

class Scraper:

    class States(Enum):
        INITIALIZING = "initializing"
        READY = "ready"
        PLAYING = "playing"
        WAITING = "waiting"
        RELOADING = "reloading"
        OBSERVING = "observing"

    def __init__(self, browser: str, casino: str , game: str, strategy: str, extra_params: dict[str, str] = {}) -> None:
        Logger.info(f"Starting scraper with browser={browser}, casino={casino}, game={game}, strategy={strategy}")

        self.__browser = browser
        self.__casino = casino
        self.__game = game
        self.__strategy = strategy

        self.__active_tab: Tab | None = None

        self.__state = Scraper.States.INITIALIZING

        Metadata.set_dictionary(extra_params)

    async def controller(self, reader: StreamReader, writer: StreamWriter):
        try:
            scraper = self
            receiver = await Receiver.create(reader)

            command = receiver.get_command()
            arg = receiver.get_parameters()

            res = None

            match command:
                case "status":
                    res = scraper.status()
                case "screenshot":
                  res = await scraper.screenshot(arg)
                case "stop":
                  res = "Stopping scraper..."
                  ForegroundProcess.kill(scraper.close) # pyright: ignore
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

        game.set_strategy(strategy)
        game.set_casino(casino)

        game.is_ready_or_fail()

        browser = Browser(navigator)

        tab = await browser.open_tab()
        self.__active_tab = tab

        if navigator.is_optimized_for_low_memory():
            await tab.enable_request_blocking()

        await tab.console(self.__watcher) # pyright: ignore

        await casino.prepare_before_playing(tab)
        await strategy.prepare_before_playing(tab)

        while True:
            await game.play(tab)

            while True:
                await tab.sleep(60)

                if Resources.is_memory_limit_reached() and self.__is_scraper_waiting():
                    memory_usage_mb = Resources.bytes_to_mb(Resources.get_memory_usage_as_bytes_or_fail())
                    memory_limit_mb = Resources.bytes_to_mb(Resources.get_memory_limit_as_bytes_or_fail())

                    Logger.warning(
                        f"Memory threshold reached: {memory_usage_mb}MB / {memory_limit_mb}MB. Reloading."
                    )
                    
                    break

            await tab.reload()
            await tab.sleep(5)

    async def close(self):
        if self.__active_tab:
            try:
                await self.__active_tab.close()
            except Exception:
                pass

    async def screenshot(self, path: str) -> str:
        if self.__active_tab is None:
            return ":warning: Tab is not initialized."
        
        await self.__active_tab.take_screenshot(path)
        return f":camera: Screenshot saved to {path}"
    
    def status(self) -> str:
        lines: list[str] = []
        lines.append("╭─ Scraper Status ─╮")
        lines.append(f"  Game:     Test")
        lines.append(f"  URL:      Test")
        lines.append(f"  Strategy: Test")
        lines.append("╰───────────────────╯")
        return "\n".join(lines)
    

    async def __watcher(self, message: object) -> None:
        parsed = BrowserConsole.parse_message(message)
        if not parsed:
            return
            
        command, payload = parsed

        match command:
            case "EXIT":
                Logger.warning(f"[BROWSER] [EXIT] {payload}")

                ForegroundProcess.kill(self.close)
            case "LOG":
                Logger.info(payload)
            case "WAITING":
                self.__state = Scraper.States.WAITING

                Logger.info(payload)
            case "PLAYING":
                self.__state = Scraper.States.PLAYING

                Logger.info(payload)
            case "OBSERVING":
                self.__state = Scraper.States.OBSERVING
                
                Logger.info(payload)

    async def __is_scraper_waiting(self) -> bool:
        return self.__state is self.States.WAITING

__ALL__ = ["Scraper"]
