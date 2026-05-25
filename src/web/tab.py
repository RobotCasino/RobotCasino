from pydoll.browser.tab import Tab as PydollTab
from pydoll.protocol.runtime.events import RuntimeEvent
from pydoll.protocol.fetch.events import FetchEvent
from pydoll.protocol.fetch.types import RequestStage
from pydoll.constants import By
from pydoll.protocol.network.types import ResourceType, ErrorReason
from asyncio import sleep

from collections.abc import Callable

from src.navigators.cookie import Cookie

from src.web.element import Element

from src.domain.scripts.script import Script

class Tab:
    def __init__(self, tab: PydollTab) -> None:
        self.__cookies: list[Cookie] = []

        self.__page = tab
        self.__fetch_listener_id: int | None = None
        self.__blocked_resource_types: set[str] = set()
        self.__blocked_url_substrings: tuple[str, ...] = ()


    async def add_cookie(self, cookie: Cookie):
        self.__cookies.append(cookie)

        return await self.update_cookies()
    
    async def clear_cookies(self):
        self.__cookies.clear()

        return await self.update_cookies()

    async def go_to(self, url: str):
        await self.__page.go_to(url)

    async def update_cookies(self) -> None:
        if len(self.__cookies) == 0:
            await self.__page.delete_all_cookies()
            return

        cookies = [c.to_dict() for c in self.__cookies]

        await self.__page.set_cookies(cookies) # pyright: ignore
    
    async def take_screenshot(self, path: str) -> None:
        await self.__page.take_screenshot(path=path)
    
    async def close(self) -> None:
        await self.__page.close()

    async def html(self) -> str:
        return await self.__page.page_source
    
    async def console(self, callback: Callable[[dict[str, str]], None]) -> None:
        await self.__page.enable_runtime_events()

        await self.__page.on(RuntimeEvent.CONSOLE_API_CALLED, callback) # pyright: ignore

    async def find_element_by_css_selector(self, selector: str) -> Element | None:
        try:
            web_element = await self.__page.find_or_wait_element(By.CSS_SELECTOR, selector, timeout=60)
            if web_element:
                return Element(web_element)
        except Exception:
            pass
        
        return None

    async def find_element_by_css_selector_or_fail(self, selector: str) -> Element:
        web_element = await self.__page.find_or_wait_element(By.CSS_SELECTOR, selector, timeout=60)
        if web_element:
            return Element(web_element)
        
        raise Exception(f"Element with selector '{selector}' not found")

    async def find_element_by_xpath(self, xpath: str) -> Element | None:
        try:
            web_element = await self.__page.find_or_wait_element(By.XPATH, xpath, timeout=60)
            if web_element:
                return Element(web_element)
        except Exception:
            pass
        
        return None

    async def find_element_by_xpath_or_fail(self, xpath: str) -> Element:
        web_element = await self.__page.find_or_wait_element(By.XPATH, xpath, timeout=60)
        if web_element:
            return Element(web_element)
        
        raise Exception(f"Element with xpath '{xpath}' not found")

    async def execute_script(self, script: Script) -> None:
        await self.__page.execute_script(str(script))

    async def sleep(self, seconds: int) -> None:
        return await sleep(seconds)
    
    async def reload(self) -> None:
        await self.__page.refresh()

    async def block_image_requests(self):
        await self.enable_request_blocking({ResourceType.IMAGE})

    async def enable_request_blocking(
        self,
        blocked_resource_types: set[ResourceType],
        blocked_url_substrings: tuple[str, ...] = (),
    ) -> None:
        self.__blocked_resource_types = {resource_type.value for resource_type in blocked_resource_types}
        self.__blocked_url_substrings = blocked_url_substrings

        resource_filter = None
        if len(blocked_resource_types) == 1:
            resource_filter = next(iter(blocked_resource_types))

        await self.__page.enable_fetch_events(
            request_stage=RequestStage.REQUEST,
            resource_type=resource_filter,
        )

        async def on_request_paused(message: dict) -> None:
            params = message.get("params", {}) if isinstance(message, dict) else {}
            request_id = params.get("requestId")
            if not request_id:
                return

            request = params.get("request", {}) if isinstance(params, dict) else {}
            url = request.get("url", "")
            resource_type = params.get("resourceType")
            resource_value = resource_type.value if isinstance(resource_type, ResourceType) else str(resource_type or "")

            should_block = resource_value in self.__blocked_resource_types
            if not should_block and url:
                for token in self.__blocked_url_substrings:
                    if token in url:
                        should_block = True
                        break

            try:
                if should_block:
                    await self.__page.fail_request(request_id, ErrorReason.BLOCKED_BY_CLIENT)
                else:
                    await self.__page.continue_request(request_id)
            except Exception:
                try:
                    await self.__page.continue_request(request_id)
                except Exception:
                    pass

        if self.__fetch_listener_id is None:
            self.__fetch_listener_id = await self.__page.on(FetchEvent.REQUEST_PAUSED, on_request_paused)

    async def disable_request_blocking(self) -> None:
        await self.__page.disable_fetch_events()

__ALL__ = ['Tab']