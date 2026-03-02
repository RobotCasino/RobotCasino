from asyncio import StreamReader, StreamWriter, sleep as asyncio_sleep
import asyncio
import gc
import logging
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
    
    def __init__(
        self,
        casino: Casino,
        game: Game,
        proxy_server: str | None = None,
        proxy_username: str | None = None,
        proxy_password: str | None = None,
    ) -> None:
        self.__chrome = None
        self.__tab = None
        self.casino = casino
        self.game = game
        self.proxy_server = proxy_server
        self.proxy_username = proxy_username
        self.proxy_password = proxy_password

        self.isBetting = False

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
        # Suppress pydoll's verbose DEBUG logging to save memory
        logging.getLogger('pydoll').setLevel(logging.WARNING)

        self.__chrome = Chrome(
            options=get_chrome_options(
                proxy_server=self.proxy_server,
                proxy_username=self.proxy_username,
                proxy_password=self.proxy_password,
            )
        )
        
        await self.__chrome.__aenter__()
        
        self.__tab = await self.__chrome.start()

        await self.__tab.enable_runtime_events()

        await self.__tab.set_cookies(cast(Any, self.casino.get_cookies()))
        await self.__tab.go_to(self.game.get_url())

        await self.__tab.on(RuntimeEvent.CONSOLE_API_CALLED, self.__console_watcher)

        await asyncio_sleep(2)

        asyncio.get_event_loop().create_task(self._periodic_cleanup())

        reload_interval = 30*60
        while True:
            try:
                play_task = asyncio.create_task(self.game.play(self.__tab))
                await asyncio.wait_for(asyncio.shield(play_task), timeout=reload_interval)
            except asyncio.TimeoutError:
                if self.isBetting:
                    Jarvis.info("Still betting, skipping reload...")
                    continue
                
                play_task.cancel()
                try:
                    await play_task
                except asyncio.CancelledError:
                    pass

                Jarvis.info("Reloading page to free memory...")

                try:
                    await self.__tab._execute_command(
                        {"method": "Runtime.discardConsoleEntries", "params": {}}
                    )
                except Exception:
                    pass

                await self.__tab.go_to(self.game.get_url())
                await asyncio_sleep(5)

                gc.collect()

                Jarvis.info("Page reloaded. Restarting game...")

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

    async def _periodic_cleanup(self, interval_seconds=120):
        """Periodically discard Chrome's retained console entries and force GC."""
        while True:
            await asyncio_sleep(interval_seconds)
            try:
                if self.__tab:
                    # Discard retained console entries — Chrome holds strong references
                    # to every object logged via console.log() when Runtime is enabled
                    await self.__tab._execute_command(
                        {"method": "Runtime.discardConsoleEntries", "params": {}}
                    )
                    # Run JS-side cleanup
                    await self.__tab.execute_script("""
                        if (typeof gc === 'function') gc();
                        performance.clearResourceTimings();
                        performance.clearMeasures();
                        performance.clearMarks();
                    """)
                gc.collect()
            except Exception:
                pass

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

                    self.isBetting = False
                case "log":
                    log_message = msg[5:].strip()

                    Jarvis.info(log_message)

                    self.isBetting = False
                case "bet":
                    amount = msg[5:].strip()

                    Jarvis.info(f"Betting {amount}")

                    self.isBetting = True
                case "waiting":
                    self.isBetting = False

        except Exception as e:
            Jarvis.error("Failed to write to console log")
    
__ALL__ = ["Scraper"]
