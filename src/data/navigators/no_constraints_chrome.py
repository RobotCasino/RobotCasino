from os import getenv
from pydoll.browser import Chrome
from pydoll.browser.options import ChromiumOptions
from pydoll.browser.tab import Tab as PydollTab

from core.domain.navigators.navigator import Navigator

class NoConstraintsChrome(Navigator):
    def __init__(self):
        self.__chrome_binary_path = "/usr/bin/chromium-browser"
        self.__tabs: list[PydollTab] = []
        self.__navigator: Chrome | None = None

    def browser_options(self) -> ChromiumOptions:
        options = ChromiumOptions()
        options._start_timeout = 120 # pyright: ignore
        options.binary_location = self.__chrome_binary_path
        options.headless = getenv("HEADLESS", "1") == "1"
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-web-security")
        options.add_argument("--disable-site-isolation-trials")
        options.add_argument('--user-data-dir=/tmp/chrome_dev')
        options.add_argument("--window-size=1920,1080") 

        return options
    
    async def open_tab(self) -> PydollTab:
        if self.__navigator:
            tab = await self.__navigator.new_tab('about:blank', None)
            
            self.__tabs.append(tab)
            
            return tab

        options = self.browser_options()

        self.__navigator = Chrome(options=options)

        tab = await self.__navigator.start()
        
        self.__tabs.append(tab)

        return tab
    
    async def close(self) -> None:
        if self.__navigator is None:
            return
        
        await self.__navigator.close()

    def is_optimized_for_low_memory(self) -> bool:
        return False
 
__ALL__ = ['NoConstraintsChrome']