import logging
from os import mkdir
import os
from pathlib import Path
from robotcasino.casinos.casino import Casino
from pydoll.browser.options import ChromiumOptions

os.makedirs("./logs", exist_ok=True)

logging.basicConfig(filename=str("./logs/error.log"), level=logging.ERROR)

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

def get_chrome_binary_path() -> str:
    path = "/usr/bin/google-chrome-stable"

    if not os.path.exists(path):
        raise FileNotFoundError(f'Chrome binary not found at {path}')
    
    return path

def get_chrome_options() -> ChromiumOptions:
    chrome_options = ChromiumOptions()

    chrome_options.headless = False
    chrome_options.binary_location = get_chrome_binary_path()
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-plugins")
    chrome_options.add_argument("--disable-breakpad")
    chrome_options.add_argument("--hide-scrollbars")
    chrome_options.add_argument("--mute-audio")
    chrome_options.add_argument("--max-old-space-size=512")
    chrome_options.add_argument("--window-size=800,600")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    return chrome_options

def get_game_js_script(casino: str, game: str) -> str:
    script = Path(f"./robotcasino/casinos/{casino}/scripts/{game}.js").read_text(encoding='utf-8')
    
    return script