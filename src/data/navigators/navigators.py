from enum import Enum

from data.navigators.safe_resource_chrome import SafeResourceChrome
from data.navigators.no_constraints_chrome import NoConstraintsChrome
from core.domain.navigators.navigator import Navigator

class Navigators(Enum):
    NO_CONSTRAINTS_CHROME = NoConstraintsChrome()
    SAFE_RESOURCE_CHROME = SafeResourceChrome()

    @staticmethod
    def get_navigator_or_fail(name: str) -> Navigator:
        navigator = Navigators.get_navigator(name)
        if navigator is None:
            raise ValueError(f"Unknown navigator: {name}")
        return navigator

    @staticmethod
    def get_navigator(name: str) -> Navigator | None:
        match name.lower():
            case "no-constraints-chrome":
                return Navigators.NO_CONSTRAINTS_CHROME.value
            case "safe-resource-chrome":
                return Navigators.SAFE_RESOURCE_CHROME.value
            case _:
                return None
