from __future__ import annotations

import logging
import sys
from logging import getLogger, FileHandler, StreamHandler, DEBUG
formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s : %(message)s')
handler = FileHandler('/var/log/ActiveRabbit.log', 'a+') if len(sys.argv) > 1 and '--release' in sys.argv else StreamHandler()
handler.setLevel(DEBUG)
handler.setFormatter(formatter)
logger = getLogger(__name__)
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