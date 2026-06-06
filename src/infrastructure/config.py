import os

from common.constants.directories import TMP_DIR, LOG_DIR, SCREENSHOT_DIR

def init():
    os.makedirs(TMP_DIR, exist_ok=True)
    os.makedirs(LOG_DIR, exist_ok=True)
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)

__ALL__ = ["init"]
