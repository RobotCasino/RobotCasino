import os
from urllib.parse import quote
from src.casinos import Casino
from pydoll.browser.options import ChromiumOptions
from src.constants import BASE_DIR, IS_HEADLESS

def get_casino(name: str) -> Casino:
    match name:
        case 'one_win':
            from src.casinos.one_win import OneWin
            
            return OneWin()
        case _:
            raise ValueError(f'Casino {name} not found')

def get_environment(key: str, default: str = None) -> str:
    r = os.getenv(key)

    if r is None and default is None:
        raise ValueError(f'Environment variable {key} not found')
    
    return r

def get_chrome_binary_path() -> str:
    path = "/usr/bin/google-chrome-stable"

    if not os.path.exists(path):
        raise FileNotFoundError(f'Chrome binary not found at {path}')
    
    return path

def get_chrome_options(
    proxy_server: str | None = None,
    proxy_username: str | None = None,
    proxy_password: str | None = None,
) -> ChromiumOptions:
    chrome_options = ChromiumOptions()

    chrome_options._start_timeout = 120
    chrome_options.binary_location = get_chrome_binary_path()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.add_argument("--disable-plugins")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument('--user-data-dir=/tmp/chrome_dev')
    chrome_options.add_argument("--disable-site-isolation-trials")
    chrome_options.add_argument("--hide-scrollbars")
    chrome_options.add_argument("--mute-audio")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    chrome_options.add_argument("--disable-default-apps")
    chrome_options.add_argument("--disable-translate")
    chrome_options.add_argument("--disable-features=TranslateUI")
    chrome_options.add_argument("--disable-hang-monitor")
    chrome_options.add_argument("--disable-ipc-flooding-protection")
    chrome_options.add_argument("--disable-renderer-backgrounding")
    chrome_options.add_argument("--aggressive-cache-discard")
    chrome_options.add_argument("--disable-cache")
    chrome_options.add_argument("--disable-application-cache")
    chrome_options.add_argument("--media-cache-size=0")
    chrome_options.add_argument("--disk-cache-size=0")
    
    if proxy_server:
        proxy_value = proxy_server
        if proxy_username and proxy_password and "@" not in proxy_server:
            if "://" in proxy_server:
                scheme, host = proxy_server.split("://", 1)
            else:
                scheme, host = "http", proxy_server
            proxy_value = f"{scheme}://{quote(proxy_username, safe='')}:{quote(proxy_password, safe='')}@{host}"
        chrome_options.add_argument(f"--proxy-server={proxy_value}")

    chrome_options.headless = IS_HEADLESS

    return chrome_options
