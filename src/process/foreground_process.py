import os
import signal
import asyncio

from src.constants import PID_PATH, SOCKET_PATH


class ForegroundProcess:
    """
    Runs the scraper in the foreground (no fork/daemon).
    Designed for Docker where PID 1 must stay alive.
    """

    def __init__(self, start_callback, close_callback):
        self.start_callback = start_callback
        self.close_callback = close_callback
        self._loop = None

    def start(self):
        PID_PATH.parent.mkdir(parents=True, exist_ok=True)
        PID_PATH.write_text(str(os.getpid()))

        signal.signal(signal.SIGINT, self._handle_terminate)
        signal.signal(signal.SIGTERM, self._handle_terminate)

        try:
            asyncio.run(self.start_callback())
        except KeyboardInterrupt:
            pass
        finally:
            self._cleanup()

    def _handle_terminate(self, signum, frame):
        if self.close_callback is not None:
            if asyncio.iscoroutinefunction(self.close_callback):
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    loop.create_task(self.close_callback())
                else:
                    asyncio.run(self.close_callback())
            else:
                self.close_callback()

        self._cleanup()
        raise SystemExit(0)

    def _cleanup(self):
        SOCKET_PATH.unlink(missing_ok=True)
        PID_PATH.unlink(missing_ok=True)

    @staticmethod
    def is_running() -> bool:
        return PID_PATH.is_file()


__ALL__ = ["ForegroundProcess"]
