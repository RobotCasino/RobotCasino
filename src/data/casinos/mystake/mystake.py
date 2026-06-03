from core.domain.scripts.script import Script
from data.navigators.cookie import Cookie
from core.domain.casinos.casino import Casino
from data.web.tab import Tab
from common.utils.metadata import Metadata
from time import time

class Mystake(Casino):

    def __init__(self):
        name = 'mystake'
        display_name = 'Mystake'
        url = 'https://m.mystake.com'
        domain = 'm.mystake.com'

        playing_scripts: tuple[Script, ...] | tuple[()] = tuple()

        super().__init__(name, url, display_name, domain, playing_scripts)

    async def prepare_before_playing(self, tab: Tab) -> None:
        authCookie = Cookie() \
            .set_name("AppAuth") \
            .set_value(Metadata.get_or_fail('SESSION_TOKEN')) \
            .set_domain(f"{self.get_domain()}") \
            .set_path("/") \
            .set_expires(time() + 365 * 24 * 3600) \
            .set_http_only(False) \
            .set_secure(True) \
            .set_same_site("Lax")

        await tab.add_cookie(authCookie)

        await tab.reload()

        await tab.sleep(5)

        await tab.go_to(self.get_url())

        await tab.sleep(5)

    
__ALL__ = ['Mystake']