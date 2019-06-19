from __future__ import annotations

from logging import getLogger, StreamHandler, DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

from Token import Token
from Token import TokenStatus
from selenium.webdriver import Chrome
from selenium.webdriver.remote.webelement import WebElement
import urllib.parse
import time

class User:

    def show(self, token: Token, name: str):
        INSTAGRAMMER_URL: str = "https://www.instagram.com/{}/?hl=ja"
        USER_NAME_XPATH: str = '//*[@id="react-root"]/section/main/div/header/section/div[1]/h1'

        if token.status != TokenStatus.LOGGED_IN:
            raise Exception

        showUrl: str = INSTAGRAMMER_URL.format(urllib.parse.quote(name))

        driver = token.driver
        driver.get(showUrl)

        # 表示確認
        time.sleep(Token.PAGE_WAIT)
        userNameElem: WebElement = driver.find_element_by_xpath(USER_NAME_XPATH)
        if userNameElem.text != name:
            raise Exception
        
        token.status = TokenStatus.USER

from Login import Login
import sys
if __name__ == "__main__":
    token: Token = Token("h.yamamoto900@gmail.com")
    Login().doLogin(token, "Sorachan20100605")
    User().show(token, "hiroyuki.happy.papa")
    input("Press key to exit.")
