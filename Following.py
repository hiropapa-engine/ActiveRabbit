from __future__ import annotations

from logging import getLogger, StreamHandler, DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

from selenium.webdriver.remote.webelement import WebElement
from selenium import webdriver

from Token import Token
from Token import TokenStatus

class Following:
    CLOSE_BUTTON_XPATH = '/html/body/div[3]/div/div[1]/div/div[2]/button'

    def __init__(self, user):
        self.user = user

    def close(self, token: Token):
        if token.status != TokenStatus.FOLLOWING:
            raise Exception()

        driver: webdriver.Chrome = token.driver
        closeBtnElem: WebElement = driver.find_element_by_xpath(Following.CLOSE_BUTTON_XPATH)
        closeBtnElem.click()

        token.status = TokenStatus.USER

        return self.user