from enum import Enum

from src.infrastructure.web_navigator.safe_resource_chrome import SafeResourceChrome
from src.infrastructure.web_navigator.no_constraints_chrome import NoConstraintsChrome
from src.infrastructure.web_navigator.navigator import Navigator

class Navigators(Enum):
    NO_CONSTRAINTS_CHROME = NoConstraintsChrome()
    SAFE_RESOURCE_CHROME = SafeResourceChrome()

    @staticmethod
    def get_navigator(name: str) -> Navigator:
        match name.lower():
            case "no-constraints-chrome":
                return Navigators.NO_CONSTRAINTS_CHROME.value
            case "safe-resource-chrome":
                return Navigators.SAFE_RESOURCE_CHROME.value
            case _:
                raise ValueError(f"Unknown navigator: {name}")
