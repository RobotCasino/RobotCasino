from pydoll.browser import Chrome
from pydoll.browser.options import ChromiumOptions
from pydoll.browser.tab import Tab as PydollTab
from os import getenv

from src.navigators.navigator import Navigator

class SafeResourceChrome(Navigator):
    def __init__(self):
        self.__chrome_binary_path = getenv("CHROME_BINARY_PATH")
        self.__tabs: list[PydollTab] = []
        self.__navigator: Chrome | None = None
        
        if self.__chrome_binary_path is None:
            raise ValueError("CHROME_BINARY_PATH environment variable is not set")

    async def open_tab(self) -> PydollTab:
        if self.__navigator:
            tab = await self.__navigator.new_tab('about:blank', None)
            
            self.__tabs.append(tab)
            
            return tab

        options = self.__browser_options()

        self.__navigator = Chrome(options=options)

        tab = await self.__navigator.start()
        
        self.__tabs.append(tab)

        return tab

    def get_tab(self, index: int) -> PydollTab:
        if index < 0 or index >= len(self.__tabs):
            raise IndexError("Tab index out of range")
        
        return self.__tabs[index]

    def __browser_options(self) -> ChromiumOptions:
        if self.__chrome_binary_path is None:
            raise ValueError("CHROME_BINARY_PATH environment variable is not set")

        options = ChromiumOptions()
        options._start_timeout = 120 # pyright: ignore
        options.binary_location = self.__chrome_binary_path
        options.headless = getenv("HEADLESS", "1") == "1"
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-software-rasterizer")
        options.add_argument("--disable-plugins")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-web-security")
        options.add_argument("--disable-extensions")
        options.add_argument('--user-data-dir=/tmp/chrome_dev')
        options.add_argument("--disable-site-isolation-trials")
        options.add_argument("--hide-scrollbars")
        options.add_argument("--mute-audio")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        options.add_argument("--disable-default-apps")
        options.add_argument("--disable-translate")
        options.add_argument("--disable-features=TranslateUI")
        options.add_argument("--disable-hang-monitor")
        options.add_argument("--disable-ipc-flooding-protection")
        options.add_argument("--disable-renderer-backgrounding")
        options.add_argument("--aggressive-cache-discard")
        options.add_argument("--disable-cache")
        options.add_argument("--disable-application-cache")
        options.add_argument("--media-cache-size=0")
        options.add_argument("--disk-cache-size=0")

        return options

    async def close(self) -> None:
        if self.__navigator is None:
            return
        
        await self.__navigator.close()

__ALL__ = ['SafeResourceChrome']