# ...existing code...
import os
import pathlib
import signal
import asyncio

from robotcasino.constants import PID_PATH, SOCKET_PATH

class DaemonProcess:

    def __init__(self, start_callback, close_callback ):
        self.start_callback = start_callback
        self.close_callback = close_callback
        self.pid = None

    def start(self):
        try:
            pid = os.fork()
            if pid > 0:
                os._exit(0)
        except OSError as e:
            raise RuntimeError(f"First fork failed: {e}") from e

        try:
            pid = os.fork()
            if pid > 0:
                os._exit(0)
        except OSError as e:
            raise RuntimeError(f"Second fork failed: {e}") from e

        os.setpgid(0, 0)
        os.umask(0)

        PID_PATH.parent.mkdir(parents=True, exist_ok=True)
        PID_PATH.write_text(str(os.getpid()))

        self.pid = os.getpid()

        signal.signal(signal.SIGINT, self.handle_terminate)
        signal.signal(signal.SIGTERM, self.handle_terminate)

        asyncio.run(self.start_callback())

    def handle_terminate(self, signum, frame):
        if self.close_callback is not None:
            if asyncio.iscoroutinefunction(self.close_callback):
                asyncio.create_task(self.close_callback())
            else:
                self.close_callback()

        SOCKET_PATH.unlink(missing_ok=True)
        PID_PATH.unlink(missing_ok=True)

        if (self.pid is not None):
            os.killpg(int(self.pid), signal.SIGKILL)
    
    def set_handle_start(self, callback):
        self.start_callback = callback
    
    def set_handle_close(self, callback):
        self.close_callback = callback


__ALL__ = ["DaemonProcess"]