import tempfile

from os import getenv
from pydoll.browser.options import ChromiumOptions
from pydoll.browser.tab import Tab as PydollTab
from pydoll.browser.chromium import Chrome

from src.navigators.navigator import Navigator

class NoConstraintsChrome(Navigator):
    def __init__(self):
        self.__chrome_binary_path = getenv("CHROME_BINARY_PATH")
        self.__user_data_dir = getenv("CHROME_USER_DATA_DIR") or tempfile.mkdtemp(prefix="robotcasino-chrome-")
        self.__tabs: list[PydollTab] = []
        self.__navigator: Chrome | None = None

        if self.__chrome_binary_path is None:
            raise ValueError("CHROME_BINARY_PATH environment variable is not set")

    def browser_options(self) -> ChromiumOptions:
        if self.__chrome_binary_path is None:
            raise ValueError("CHROME_BINARY_PATH environment variable is not set")

        options = ChromiumOptions()
        options._start_timeout = 120 # pyright: ignore
        options.binary_location = self.__chrome_binary_path
        options.headless = False
        options.add_argument('--user-data-dir=/tmp/chrome_dev')

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
 
__ALL__ = ['NoConstraintsChrome']