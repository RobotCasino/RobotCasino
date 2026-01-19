import logging
from os import error, mkdir
from pathlib import Path

error_path = Path("./logs/error.log")

logging.basicConfig(filename=str(error_path), level=logging.ERROR)