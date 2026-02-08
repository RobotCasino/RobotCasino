import datetime
from typing import Optional

from robotcasino.constants import CONSOLE_LOG_PATH, ERROR_LOG_PATH

class Jarvis:
    @staticmethod
    def log_message(message: str, level: str = "INFO") -> None:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}\n"

        with open(CONSOLE_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(log_entry)

    @staticmethod
    def log_error(error: str, exception: Optional[Exception] = None) -> None:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [ERROR] {error}\n"

        if exception:
            import traceback
            tb = ''.join(traceback.format_exception(type(exception), exception, exception.__traceback__))
            log_entry += f"Traceback:\n{tb}\n"

        with open(ERROR_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(log_entry)

    @staticmethod
    def debug(message: str) -> None:
        Jarvis.log_message(message, level="DEBUG")

    @staticmethod
    def info(message: str) -> None:
        Jarvis.log_message(message, level="INFO")

    @staticmethod
    def warning(message: str) -> None:
        Jarvis.log_message(message, level="WARNING")

    @staticmethod
    def error(error: str, exception: Optional[Exception] = None) -> None:
        Jarvis.log_error(error, exception)
