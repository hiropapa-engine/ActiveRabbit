from __future__ import annotations

from logging import getLogger, StreamHandler, DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

from selenium.webdriver import Chrome

class Token:
    PAGE_WAIT: int = 2

    def __init__(self, name: str):
        self.name: str = name
        self.driver: Chrome = None

    def isLoggedIn(self):
        return (self.driver != None)

