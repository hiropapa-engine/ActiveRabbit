from __future__ import annotations

from logging import getLogger, StreamHandler, DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

from typing import List
import time

from selenium.webdriver import Chrome
from selenium.webdriver.remote.webelement import WebElement

from Token import Token
from Token import TokenStatus
from Presentaions import Presentations
from JavaScript import JavaScript

class Favorites:

    def __init__(self, post):
        self.post = post

    def getUsers(self, token: Token) -> List[str]:

        FAVORITES_RELATIVE_XPATH = "div/div[2]/div/div"
        FAVORITE_TAG_NAME = "a"
        USER_NAME_ATTR = 'title'

        if token.status != TokenStatus.FAVORITE_LIST:
            raise Exception()

        # bodyタグ 直下の divタグ のうち role="presentation" の要素が表示要素なので検索して特定
        # ※ formタグにも role="presentation" が存在し、それだけでは特定出来ないことに注意
        presElem: WebElement = Presentations.getPresentation(token)

        # 追加する対象がいなくなるまでリストアップしてスクロール
        userSet = set()
        driver : Chrome = token.driver
        while True:
            # 表示要素からの相対パス div/div[2]/div/div の直下の div が良いねリスト
            favoriteElem = presElem.find_element_by_xpath(FAVORITES_RELATIVE_XPATH)
            favoriteList: List[WebElement] = favoriteElem.find_elements_by_tag_name(FAVORITE_TAG_NAME)

            # リストアップ
            append: int = 0
            for favorite in favoriteList:
                name = favorite.get_attribute(USER_NAME_ATTR)
                if len(name) != 0 and not name in userSet:
                    userSet.add(name)
                    append = append + 1

            if append == 0:
                break
            else:
                JavaScript.scrollIntoView(driver, favoriteList[len(favoriteList) - 1])

        logger.debug("favorite lists (size = {0})".format(len(userSet)))
        return list(userSet)