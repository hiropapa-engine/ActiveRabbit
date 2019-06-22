from __future__ import annotations

from logging import getLogger, StreamHandler, DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

from typing import List

from selenium.webdriver.remote.webelement import WebElement

from Token import Token
from Login import Login
from Timeline import Timeline

class ArTimelineFavoriter:

    @classmethod
    def do(cls, name: str, password: str):
        token: Token = Token(name)
        Login().doLogin(token, password)

        count = 0
        while count < 5:
            button = token.driver.find_element_by_class_name(Timeline.FAVOLITE_CSS)
            button.click()
            count = count + 1

        token.driver.close()