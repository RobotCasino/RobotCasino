import re
import json

from os import getenv
from time import monotonic

from asyncio import StreamReader, StreamWriter

from aiohttp import web

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
from pydoll.protocol.network.types import ResourceType

class Scraper:
    def __init__(self, browser: str, casino: str , game: str, strategy: str, extra_params: dict[str, str] = {}) -> None:
        Logger.info(f"Starting scraper with browser={browser}, casino={casino}, game={game}, strategy={strategy}")

        self.__browser = browser
        self.__casino = casino
        self.__game = game
        self.__strategy = strategy

        self.__active_tab: Tab | None = None
        self.__exit_runner: web.AppRunner | None = None

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
                case "html":
                  res = await scraper.html()
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
        scraper = self

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

        await self.__start_exit_server()

        blocked_urls = (
            "doubleclick.net",
            "googletagmanager.com",
            "google-analytics.com",
            "stats.g.doubleclick.net",
            "facebook.net",
            "facebook.com/tr",
            "/analytics",
            "/collect",
        )

        memory_limit = self.__get_memory_limit_bytes()
        memory_ratio = float(getenv("MEMORY_RELOAD_RATIO", "0.85"))
        check_interval = int(getenv("MEMORY_CHECK_INTERVAL_SECONDS", "60"))
        max_session_seconds = int(getenv("MAX_SESSION_SECONDS", "3600"))

        console_enabled = False

        while True:
            await casino.prepare_before_playing(tab)
            await strategy.prepare_before_playing(tab)

            if not console_enabled:
                await tab.console(scraper.__watcher) # pyright: ignore
                console_enabled = True

            await tab.disable_request_blocking()
            await game.play(tab)

            await tab.enable_request_blocking(
                {ResourceType.IMAGE, ResourceType.MEDIA, ResourceType.FONT},
                blocked_url_substrings=blocked_urls,
            )

            session_start = monotonic()
            while True:
                await tab.sleep(check_interval)

                if max_session_seconds > 0 and (monotonic() - session_start) >= max_session_seconds:
                    Logger.info("Max session reached. Reloading to release memory.")
                    break

                if memory_limit:
                    usage = self.__get_memory_usage_bytes()
                    if usage is not None and usage >= int(memory_limit * memory_ratio):
                        Logger.warning(
                            f"Memory threshold reached: {self.__bytes_to_mb(usage)}MB / {self.__bytes_to_mb(memory_limit)}MB. Reloading."
                        )
                        break

            await tab.reload()
            await tab.sleep(5)

    async def close(self):
        await self.__stop_exit_server()
        if self.__active_tab:
            try:
                await self.__active_tab.close()
            except Exception:
                pass

    async def __handle_exit_signal(self, request: web.Request) -> web.Response:
        payload = {}
        try:
            payload = await request.json()
        except Exception:
            payload = {}

        message = payload.get("message") or payload.get("reason") or ""
        Logger.warning(f"[BROWSER] [EXIT] {message}")
        ForegroundProcess.kill(self.close)
        return web.json_response({"ok": True})

    async def __start_exit_server(self) -> None:
        if self.__exit_runner is not None:
            return

        app = web.Application()
        app.add_routes([web.post("/exit", self.__handle_exit_signal)])

        runner = web.AppRunner(app)
        await runner.setup()

        host = getenv("EXIT_SIGNAL_HOST", "127.0.0.1")
        port = int(getenv("EXIT_SIGNAL_PORT", "8081"))

        site = web.TCPSite(runner, host, port)
        await site.start()

        self.__exit_runner = runner

    async def __stop_exit_server(self) -> None:
        if self.__exit_runner is None:
            return

        await self.__exit_runner.cleanup()
        self.__exit_runner = None

    def __bytes_to_mb(self, value: int) -> int:
        return int(value / (1024 * 1024))

    def __read_cgroup_value(self, paths: tuple[str, ...]) -> int | None:
        for path in paths:
            try:
                with open(path, "r", encoding="utf-8") as handle:
                    raw_value = handle.read().strip()

                if raw_value == "max":
                    return None

                value = int(raw_value)
                if value > (1 << 60):
                    return None

                return value
            except (FileNotFoundError, ValueError, OSError):
                continue

        return None

    def __get_memory_usage_bytes(self) -> int | None:
        return self.__read_cgroup_value(
            (
                "/sys/fs/cgroup/memory.current",
                "/sys/fs/cgroup/memory/memory.usage_in_bytes",
            )
        )

    def __get_memory_limit_bytes(self) -> int | None:
        return self.__read_cgroup_value(
            (
                "/sys/fs/cgroup/memory.max",
                "/sys/fs/cgroup/memory/memory.limit_in_bytes",
            )
        )

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
            case "BET":
                Logger.info(payload)
            case "WAITING":
                Logger.info(payload)

__ALL__ = ["Scraper"]
