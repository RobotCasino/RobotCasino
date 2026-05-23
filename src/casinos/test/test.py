from src.domain.casinos.casino import Casino
from src.web.tab import Tab

class Test(Casino):
    def __init__(self):
        name = "test"
        url = "https://blankslate.io/"
        display_name = "Test Casino"
        domain = "blankslate.io"

        super().__init__(name, url, display_name, domain)

    async def prepare_before_playing(self, tab: Tab):
        await tab.go_to(self.get_url())
