import signal
import asyncio

from os import getpid, path, remove, _exit

from common.constants.directories import TMP_DIR

from typing import Callable, Coroutine, Any

class ForegroundProcess:
    def __init__(self, start_callback, close_callback): # pyright: ignore
        self.start_callback = start_callback
        self.close_callback = close_callback
        self._loop = None

        self.pidFilePath = TMP_DIR + "process.pid"
        self.socketFilePath = TMP_DIR + ".robotcasino.socket"

    def start(self):
        if path.isdir(TMP_DIR) is False:
            raise Exception(f"A problem occured with the tmp directory path: {TMP_DIR}")
        
        with open(self.pidFilePath, "w") as f:
            f.write(str(getpid()))

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
        if path.isfile(self.socketFilePath):
            remove(self.socketFilePath)
        if path.isfile(self.pidFilePath):
            remove(self.pidFilePath)

    @staticmethod
    def is_running() -> bool:
        return path.isfile(TMP_DIR + "process.pid")

    @staticmethod
    def kill(close_callback: Callable[[], Coroutine[Any, Any, Any] | Any] | None = None):
        async def shutdown():
            await asyncio.sleep(0.1)

            if close_callback:
                if asyncio.iscoroutinefunction(close_callback): # pyright: ignore
                    await close_callback()
                else:
                    close_callback()
            
            if path.isfile(TMP_DIR + ".robotcasino.socket"):
                remove(TMP_DIR + ".robotcasino.socket")

            if path.isfile(TMP_DIR + "process.pid"):
                remove(TMP_DIR + "process.pid")
            
            _exit(0)
            
        asyncio.create_task(shutdown())

__ALL__ = ["ForegroundProcess"]
