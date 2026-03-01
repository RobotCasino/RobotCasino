import datetime
import logging
import os
import sys
from typing import Optional

MAX_LOG_SIZE = 1 * 1024 * 1024  # 1 MB

from src.constants import CONSOLE_LOG_PATH, ERROR_LOG_PATH

# Configure the root logger for stdout/stderr output
_stream_formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

_console_handler = logging.StreamHandler(sys.stdout)
_console_handler.setLevel(logging.DEBUG)
_console_handler.setFormatter(_stream_formatter)

_stderr_handler = logging.StreamHandler(sys.stderr)
_stderr_handler.setLevel(logging.ERROR)
_stderr_handler.setFormatter(_stream_formatter)

_logger = logging.getLogger("robotcasino")
_logger.setLevel(logging.DEBUG)
_logger.addHandler(_console_handler)
_logger.addHandler(_stderr_handler)


class Jarvis:
    @staticmethod
    def _rotate_log_if_needed(path):
        """Truncate log file to half size when it exceeds MAX_LOG_SIZE."""
        try:
            if os.path.getsize(path) > MAX_LOG_SIZE:
                with open(path, 'rb') as f:
                    f.seek(-MAX_LOG_SIZE // 2, 2)
                    content = f.read()
                with open(path, 'wb') as f:
                    f.write(content)
        except (OSError, IOError):
            pass

    @staticmethod
    def log_message(message: str, level: str = "INFO") -> None:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}\n"

        # Rotate log if needed, then write
        Jarvis._rotate_log_if_needed(CONSOLE_LOG_PATH)
        with open(CONSOLE_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(log_entry)

        # Write to stdout via logging
        log_level = getattr(logging, level.upper(), logging.INFO)
        _logger.log(log_level, message)

    @staticmethod
    def log_error(error: str, exception: Optional[Exception] = None) -> None:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [ERROR] {error}\n"

        if exception:
            import traceback
            tb = ''.join(traceback.format_exception(type(exception), exception, exception.__traceback__))
            log_entry += f"Traceback:\n{tb}\n"

        # Rotate log if needed, then write
        Jarvis._rotate_log_if_needed(ERROR_LOG_PATH)
        with open(ERROR_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(log_entry)

        # Write to stderr via logging
        if exception:
            _logger.error(error, exc_info=exception)
        else:
            _logger.error(error)

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
