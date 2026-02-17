import os
import pathlib

BASE_DIR = pathlib.Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent
LOGS_DIR = PROJECT_DIR / "logs"

os.makedirs(LOGS_DIR, exist_ok=True)

SOCKET_PATH = pathlib.Path(pathlib.Path.home() / ".robotcasino.socket")
PID_PATH =  pathlib.Path("/tmp/robotcasino.pid")
CONSOLE_LOG_PATH = LOGS_DIR / "messages.log"
ERROR_LOG_PATH = LOGS_DIR / "errors.log"

CONSOLE_LOG_PATH.touch(exist_ok=True)
ERROR_LOG_PATH.touch(exist_ok=True)

__ALL__ = ["PID_PATH", "SOCKET_PATH", "CONSOLE_LOG_PATH", "ERROR_LOG_PATH"]