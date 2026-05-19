from pydoll.elements.web_element import WebElement as PydollWebElement

class Element: 
    def __init__(self, web_element: PydollWebElement):
        self.__web_element = web_element