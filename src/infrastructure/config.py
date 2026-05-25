import os
import pathlib

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
PROJECT_DIR = BASE_DIR.parent

LOGS_DIR = PROJECT_DIR / "logs"

IS_DOCKER = pathlib.Path("/app").exists() and pathlib.Path("/.dockerenv").exists()
OUTPUT_DIR = pathlib.Path("/app/output") if IS_DOCKER else PROJECT_DIR / "output"

SOCKET_PATH = str(pathlib.Path(pathlib.Path.home() / ".robotcasino.socket"))
PID_PATH =  str(pathlib.Path("/tmp/robotcasino.pid"))

CONSOLE_LOG_PATH = OUTPUT_DIR / "messages.log"
ERROR_LOG_PATH = OUTPUT_DIR / "errors.log"


def init():
    os.makedirs(LOGS_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    CONSOLE_LOG_PATH.touch(exist_ok=True)
    ERROR_LOG_PATH.touch(exist_ok=True)

__ALL__ = [
    "BASE_DIR", "PROJECT_DIR", "IS_HEADLESS", "LOGS_DIR", "IS_DOCKER",
    "OUTPUT_DIR", "SOCKET_PATH", "PID_PATH", "CONSOLE_LOG_PATH",
    "ERROR_LOG_PATH", "init", "get_environment",
]
