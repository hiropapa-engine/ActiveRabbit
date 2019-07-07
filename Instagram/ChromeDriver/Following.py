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

from selenium.webdriver.remote.webelement import WebElement
from selenium import webdriver

from Instagram.ChromeDriver.Token import Token
from Instagram.ChromeDriver.Token import TokenStatus

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