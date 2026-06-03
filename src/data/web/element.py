from pydoll.constants import By
from pydoll.elements.web_element import WebElement as PydollWebElement
from src.core.domain.scripts.script import Script

class Element: 
    def __init__(self, web_element: PydollWebElement | list[PydollWebElement]):
        self.__web_element = web_element

    async def click(self) -> None:
        if isinstance(self.__web_element, list):
            for element in self.__web_element:
                await element.click()
        else:
            await self.__web_element.click()

    async def click_by_cdp(self) -> None:
        if isinstance(self.__web_element, list):
            for element in self.__web_element:
                await element.click(humanize=False)
        else:
            await self.__web_element.click(humanize=False)

    async def execute_script(self, script: Script | str) -> None:
        if isinstance(self.__web_element, list):
            for element in self.__web_element:
                await element.execute_script(str(script))
        else:
            await self.__web_element.execute_script(str(script))
    
    async def find_element_by_css_selector(self, selector: str) -> 'Element | None':
        try:
            if isinstance(self.__web_element, list):
                web_elements = []
                for element in self.__web_element:
                    try:
                        web_element = await element.find_or_wait_element(By.CSS_SELECTOR, selector, timeout=60)
                        if web_element:
                            web_elements.append(web_element)
                    except Exception:
                        continue
                if web_elements:
                    return Element(web_elements)
            else:
                web_element = await self.__web_element.find_or_wait_element(By.CSS_SELECTOR, selector, timeout=60)
                if web_element:
                    return Element(web_element)
        except Exception:
            pass
        
        return None

    async def find_element_by_css_selector_or_fail(self, selector: str) -> 'Element':
        if isinstance(self.__web_element, list):
            web_elements = []
            for element in self.__web_element:
                try:
                    web_element = await element.find_or_wait_element(By.CSS_SELECTOR, selector, timeout=60)
                    if web_element:
                        web_elements.append(web_element)
                except Exception:
                    continue
            if web_elements:
                return Element(web_elements)
        else:
            web_element = await self.__web_element.find_or_wait_element(By.CSS_SELECTOR, selector, timeout=60)
            if web_element:
                return Element(web_element)
        
        raise Exception(f"Element with selector '{selector}' not found")

    async def find_element_by_xpath(self, xpath: str) -> 'Element | None':
        try:
            if isinstance(self.__web_element, list):
                web_elements = []
                for element in self.__web_element:
                    try:
                        web_element = await element.find_or_wait_element(By.XPATH, xpath, timeout=60)
                        if web_element:
                            web_elements.append(web_element)
                    except Exception:
                        continue
                if web_elements:
                    return Element(web_elements)
            else:
                web_element = await self.__web_element.find_or_wait_element(By.XPATH, xpath, timeout=60)
                if web_element:
                    return Element(web_element)
        except Exception:
            pass
        
        return None

    async def find_element_by_xpath_or_fail(self, xpath: str) -> 'Element':
        if isinstance(self.__web_element, list):
            web_elements = []
            for element in self.__web_element:
                try:
                    web_element = await element.find_or_wait_element(By.XPATH, xpath, timeout=60)
                    if web_element:
                        web_elements.append(web_element)
                except Exception:
                    continue
            if web_elements:
                return Element(web_elements)
        else:
            web_element = await self.__web_element.find_or_wait_element(By.XPATH, xpath, timeout=60)
            if web_element:
                return Element(web_element)
        
        raise Exception(f"Element with xpath '{xpath}' not found")
