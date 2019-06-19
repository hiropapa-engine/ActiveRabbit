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
from typing import List
from FavoriteList import FavoriteList

class Post:

    MEDIA_DIALOG_XPATH = '/html/body/div[*]/div[2]/div'

    def __init__(self):
        self.hasNext: bool = True
        self.hasPrev: bool = True
        pass

    def next(self, token: Token) -> Post:
        NEXT_POST_LINK_CSS_SELECTOR = 'a.coreSpriteRightPaginationArrow'

        if token.status != TokenStatus.POST:
            raise Exception

        driver : Chrome = token.driver
        nextPostLinkElem: WebElement =  driver.find_element_by_css_selector(NEXT_POST_LINK_CSS_SELECTOR)
        nextPostLinkElem.click()

        mediaDialogElems: List[WebElement] = driver.find_elements_by_xpath(Post.MEDIA_DIALOG_XPATH)

        if not mediaDialogElems[0].is_displayed():
            raise Exception
        
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

    def favorite(self, token: Token):
        HEART_ICON_XPATH = "/html/body/div[3]/div[2]/div/article/div[2]/section[1]/span[1]/button/span"

        if token.status != TokenStatus.POST:
            raise Exception

        if self.isFavorited(token):
            return

        driver: Chrome = token.driver
        heartIconElem: WebElement = driver.find_element_by_xpath(HEART_ICON_XPATH)
        heartIconElem.click()

        if not self.isFavorited(token):
            raise Exception()