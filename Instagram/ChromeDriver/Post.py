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
import time

from selenium.webdriver import Chrome
from selenium.webdriver.remote.webelement import WebElement

from Instagram.ChromeDriver.Token import Token
from Instagram.ChromeDriver.Token import TokenStatus
from Instagram.ChromeDriver.Favorites import Favorites

class Post:

    MEDIA_DIALOG_XPATH = '/html/body/div[*]/div[2]/div'

    def __init__(self, user):
        self.user = user
        self.hasNext: bool = True
        self.hasPrev: bool = True
        pass

    def close(self, token: Token):
        CLOSE_BUTTON_XPATH: str = "/html/body/div[3]/button[1]"
        USER_NAME_XPATH: str = '//*[@id="react-root"]/section/main/div/header/section/div[1]/h1'

        if not token.status == TokenStatus.POST:
            raise Exception

        driver: Chrome = token.driver
        closeButton: WebElement = driver.find_element_by_xpath(CLOSE_BUTTON_XPATH)
        closeButton.click()

        userName: WebElement = driver.find_element_by_xpath(USER_NAME_XPATH)

        if userName.text != self.user.name:
            raise Exception

        token.status = TokenStatus.USER

        return self.user

    def next(self, token: Token) -> Post:
        NEXT_POST_LINK_CSS_SELECTOR = 'a.coreSpriteRightPaginationArrow'

        if token.status != TokenStatus.POST:
            raise Exception

        driver : Chrome = token.driver
        nextPostLinkElem: WebElement =  driver.find_element_by_css_selector(NEXT_POST_LINK_CSS_SELECTOR)
        nextPostLinkElem.click()

        retryCount = 0
        while True:
            try:
                mediaDialogElems: List[WebElement] = driver.find_elements_by_xpath(Post.MEDIA_DIALOG_XPATH)

                if mediaDialogElems[0].is_displayed():
                    break

            except Exception as e:
                retryCount = retryCount + 1
                if retryCount >= Token.RETRY:
                    raise e
        
        return self

    def isFavorited(self, token: Token) -> bool:
        HEART_ICON_XPATH = "/html/body/div[3]/div[2]/div/article/div[2]/section[1]/span[1]/button/span"
        FAVORITTING_ATTRS = "aria-label"
        FAVORITTING_MSG = "いいね！"

        if token.status != TokenStatus.POST:
            raise Exception

        driver: Chrome = token.driver
        heartIconElem: WebElement = driver.find_element_by_xpath(HEART_ICON_XPATH)

        msg: str = heartIconElem.get_attribute(FAVORITTING_ATTRS)

        return msg != FAVORITTING_MSG

    def favorite(self, token: Token) -> bool:
        HEART_ICON_XPATH = "/html/body/div[3]/div[2]/div/article/div[2]/section[1]/span[1]/button/span"

        if token.status != TokenStatus.POST:
            raise Exception

        if self.isFavorited(token):
            return False

        driver: Chrome = token.driver
        heartIconElem: WebElement = driver.find_element_by_xpath(HEART_ICON_XPATH)
        heartIconElem.click()

        if not self.isFavorited(token):
            raise Exception()

        return True

    def showFavorites(self, token: Token) -> Favorites:
        FAVORITE_LIST_LINK_XPATH: str = '/html/body/div[3]/div[2]/div/article/div[2]/section[2]/div/div[*]/button/span'
        FAVORITE_LIST_DLG_XPATH: str = '/html/body/div[4]/div'

        if token.status != TokenStatus.POST:
            raise Exception()

        driver: Chrome = token.driver
        favoriteListLink: WebElement = driver.find_element_by_xpath(FAVORITE_LIST_LINK_XPATH)
        favoriteListLink.click()

        favorites: WebElement = driver.find_element_by_xpath(FAVORITE_LIST_DLG_XPATH)
        if not favorites.is_displayed():
            raise Exception()

        time.sleep(1)
        token.status = TokenStatus.FAVORITE_LIST

        return Favorites(self)
