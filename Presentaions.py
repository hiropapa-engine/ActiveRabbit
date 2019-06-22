from __future__ import annotations

from logging import getLogger, StreamHandler, DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

from typing import List

from selenium.webdriver import Chrome
from selenium.webdriver.remote.webelement import WebElement

from Token import Token

class Presentations:
    PRESENTATION_SEARCH_XPATH = "/html/body/div[*]"

    @classmethod
    def getPresentation(cls, token: Token):
        driver: Chrome = token.driver
        presCandElems: List[WebElement] = driver.find_elements_by_xpath(Presentations.PRESENTATION_SEARCH_XPATH)

        presElem: WebElement = None
        for elem in presCandElems:
            if elem.get_attribute("role") == "presentation":
                presElem = elem
                break

        if presElem == None:
            raise Exception()

        return presElem