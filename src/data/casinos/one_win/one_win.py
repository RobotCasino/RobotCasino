from common.constants.directories import BASE_DIR
from core.domain.scripts.script import Script
from data.navigators.cookie import Cookie
from core.domain.casinos.casino import Casino
from common.utils.metadata import Metadata
from data.web.tab import Tab
from time import time

class OneWin(Casino):

    def __init__(self):
        name = 'one_win'
        display_name = '1Win'
        url = 'https://1win.com/'
        domain = '1win.com'

        playing_scripts: tuple[Script, ...] = (
            Script("1Win Playing Script", f'{BASE_DIR}data/casinos/one_win/scripts/one-win-cleaner.js'),
        )

        super().__init__(name, url, display_name, domain, playing_scripts)

    async def prepare_before_playing(self, tab: Tab):
        authCookie = Cookie() \
            .set_name("1w_token") \
            .set_value(Metadata.get_or_fail('SESSION_TOKEN')) \
            .set_domain(f"{self.get_domain()}") \
            .set_path("/") \
            .set_expires(time() + 365 * 24 * 3600) \
            .set_http_only(False) \
            .set_secure(True) \
            .set_same_site("None")

        await tab.add_cookie(authCookie)

        await tab.reload()

        await tab.sleep(5)

    
__ALL__ = ['OneWin']