import os
from pathlib import Path

import signal
import asyncio

from os import getpid

from src.infrastructure.config import PID_PATH, SOCKET_PATH

from typing import Callable, Coroutine, Any

class ForegroundProcess:
    def __init__(self, start_callback, close_callback): # pyright: ignore
        self.start_callback = start_callback
        self.close_callback = close_callback
        self._loop = None

        self.pidpath = Path(PID_PATH)
        self.socketpath = Path(SOCKET_PATH)

    def start(self):
        self.pidpath.parent.mkdir(parents=True, exist_ok=True)
        self.pidpath.write_text(str(getpid()))

        signal.signal(signal.SIGINT, self._handle_terminate) # pyright: ignore
        signal.signal(signal.SIGTERM, self._handle_terminate) # pyright: ignore

        try:
            asyncio.run(self.start_callback()) # pyright: ignore
        except KeyboardInterrupt:
            pass
        finally:
            self._cleanup()

    def _handle_terminate(self, signum, frame): # pyright: ignore
        if self.close_callback is not None:
            if asyncio.iscoroutinefunction(self.close_callback): # pyright: ignore
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    loop.create_task(self.close_callback()) # pyright: ignore 
                else:
                    asyncio.run(self.close_callback()) # pyright: ignore
            else: 
                self.close_callback() # pyright: ignore

        self._cleanup()
        raise SystemExit(0)

    def _cleanup(self):
        self.socketpath.unlink(missing_ok=True)
        self.pidpath.unlink(missing_ok=True)

    @staticmethod
    def is_running() -> bool:
        return Path(PID_PATH).is_file()

    @staticmethod
    def kill(close_callback: Callable[[], Coroutine[Any, Any, Any] | Any] | None = None):
        async def shutdown():
            await asyncio.sleep(0.1)

            if close_callback:
                if asyncio.iscoroutinefunction(close_callback): # pyright: ignore
                    await close_callback()
                else:
                    close_callback()
            Path(SOCKET_PATH).unlink(missing_ok=True)
            Path(PID_PATH).unlink(missing_ok=True)
            os._exit(0)
            
        asyncio.create_task(shutdown())

__ALL__ = ["ForegroundProcess"]
