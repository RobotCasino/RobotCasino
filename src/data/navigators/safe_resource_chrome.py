from pydoll.browser import Chrome
from pydoll.browser.options import ChromiumOptions
from pydoll.browser.tab import Tab as PydollTab
from os import getenv

from data.navigators.navigator import Navigator

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
        # --- Crucial Docker & Security constraints ---
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-web-security")
        options.add_argument("--disable-site-isolation-trials")
        options.add_argument('--user-data-dir=/tmp/chrome_dev')

        # --- Aggressive Viewport Shrinking ---
        # A tiny viewport drastically limits visual rasterization and painting memory buffers
        options.add_argument("--window-size=1280,720") 
        options.add_argument("--force-device-scale-factor=1")
        options.add_argument("--hide-scrollbars")

        # --- Disable Media & UI Engines ---
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-software-rasterizer")
        options.add_argument("--mute-audio")
        options.add_argument("--disable-plugins")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-notifications")

        
        # Blocking APIs and WebGL drastically reduces memory footprint 
        # for canvas-heavy games if you only interact with the DOM via scraping
        options.add_argument("--disable-webgl")
        options.add_argument("--disable-3d-apis")
        options.add_argument("--disable-permissions-api")
        options.add_argument("--disable-speech-api")
        options.add_argument("--disable-webrtc")
        

        # Disable logging and crash reporting memory overhead
        options.add_argument("--disable-logging")
        options.add_argument("--disable-crash-reporter")
        options.add_argument("--disable-in-process-stack-traces")
        
        # --- Extreme Reductions ---
        # options.add_argument("--disable-remote-fonts") # Both flags 
        # options.add_argument("--disable-reading-from-canvas") # cause problems with the iframe! NEVER USE THEM
        options.add_argument("--disable-client-side-phishing-detection")
        options.add_argument("--disable-component-extensions-with-background-pages")
        options.add_argument("--disable-default-apps")
        options.add_argument("--disable-ipc-flooding-protection")
        options.add_argument("--disable-background-timer-throttling")
        options.add_argument("--metrics-recording-only")
        options.add_argument("--v8-cache-options=none")

        # Block image rendering entirely at the engine level
        options.add_argument("--blink-settings=imagesEnabled=true") 

        # --- Process & Memory Trimming ---
        options.add_argument("--renderer-process-limit=1")
        options.add_argument("--process-per-site")
        options.add_argument("--disable-background-networking")
        options.add_argument("--disable-backgrounding-occluded-windows")
        options.add_argument("--disable-renderer-backgrounding")
        options.add_argument("--disable-sync")
        options.add_argument("--disable-translate")

        # --- Cache Restriction ---
        options.add_argument("--disk-cache-size=5242880") # Reduce to 5MB
        options.add_argument("--media-cache-size=1")      # Virtually eliminate media caching
        options.add_argument("--disable-application-cache")

        # --- Fixed V8 Execution Engine Flags ---
        # Aggressive GC flags: force global GC, optimize for size, and flush compiled code
        options.add_argument("--js-flags=--max-old-space-size=250 --expose-gc --optimize-for-size --flush-bytecode --gc-global")

        options.add_argument("--user-agent=Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36")
        return options

    async def close(self) -> None:
        if self.__navigator is None:
            return
        
        await self.__navigator.close()
    
    def is_optimized_for_low_memory(self) -> bool:
        return True

__ALL__ = ['SafeResourceChrome']