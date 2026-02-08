import os
import pathlib

os.makedirs("./logs", exist_ok=True)

SOCKET_PATH = pathlib.Path(pathlib.Path.home() / ".robotcasino.socket")
PID_PATH =  pathlib.Path("/tmp/robotcasino.pid")
CONSOLE_LOG_PATH = pathlib.Path("./logs/messages.log")
ERROR_LOG_PATH = pathlib.Path("./logs/errors.log")

CONSOLE_LOG_PATH.touch(exist_ok=True)
ERROR_LOG_PATH.touch(exist_ok=True)

__ALL__ = ["PID_PATH", "SOCKET_PATH", "CONSOLE_LOG_PATH", "ERROR_LOG_PATH"]