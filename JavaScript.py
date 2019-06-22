from __future__ import annotations

from logging import getLogger, StreamHandler, DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

from selenium.webdriver.remote.webelement import WebElement
import time
class JavaScript:
    @classmethod
    def scrollIntoView(cls, driver, element: WebElement):
        driver.execute_script("arguments[0].scrollIntoView();", element)
