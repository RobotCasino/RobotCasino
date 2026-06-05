import os

from common.constants.directories import TMP_DIR, LOG_DIR, DOWNLOAD_DIR

def init():
    os.makedirs(TMP_DIR, exist_ok=True)
    os.makedirs(LOG_DIR, exist_ok=True)
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

__ALL__ = ["init"]
