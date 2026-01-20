import logging
from os import error, mkdir
import os
from pathlib import Path

from robotcasino.casinos.casino import Casino

error_path = Path("./logs/error.log")

logging.basicConfig(filename=str(error_path), level=logging.ERROR)

def get_casino(name: str) -> Casino:
    match name:
        case 'one_win':
            from robotcasino.casinos.one_win.one_win import OneWin
            
            return OneWin()
        case _:
            raise ValueError(f'Casino {name} not found')

def get_environment(key: str) -> str:
    r = os.getenv(key)

    if r is None:
        raise ValueError(f'Environment variable {key} not found')
    
    return r
