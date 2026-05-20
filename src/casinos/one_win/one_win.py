from src.navigators.cookie import Cookie
from src.domain.casinos.casino import Casino
from src.web.tab import Tab
from time import time

from os import getenv

class OneWin(Casino):

    def __init__(self):
        name = 'one_win'
        display_name = '1Win'
        domain = '1win.com'
        url = 'https://1win.com/'

        super().__init__(name, url, display_name, domain)

    async def prepare(self, tab: Tab):
        authCookie = Cookie() \
            .set_name("1w_token") \
            .set_value(str(getenv("SESSION_TOKEN"))) \
            .set_domain(f"{self.get_domain()}") \
            .set_path("/") \
            .set_expires(time() + 365 * 24 * 3600) \
            .set_http_only(False) \
            .set_secure(True) \
            .set_same_site("None")

        await tab.add_cookie(authCookie)

        await tab.reload()

        await tab.sleep(5)

        await tab.go_to(self.get_url())

        await tab.sleep(5)

    
__ALL__ = ['OneWin']