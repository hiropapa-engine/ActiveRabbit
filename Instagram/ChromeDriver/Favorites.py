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
from selenium.common.exceptions import NoSuchElementException

from Instagram.ChromeDriver.Token import Token
from Instagram.ChromeDriver.Token import TokenStatus
from Instagram.ChromeDriver.Presentaions import Presentations
from Instagram.ChromeDriver.JavaScript import JavaScript
from Instagram.ChromeDriver.OtherUser import OtherUser

class Favorites:

    def __init__(self, post):
        self.post = post

    def getUsers(self, token: Token) -> List[str]:

        FAVORITES_RELATIVE_XPATH = "div/div[2]/div/div/div[*]"
        PROFILE_LINK_RELATIVE_XPATH = "div[2]/div/div/a/div/div/div"

        if token.status != TokenStatus.FAVORITE_LIST:
            raise Exception()

        # bodyタグ 直下の divタグ のうち role="presentation" の要素が表示要素なので検索して特定
        # ※ formタグにも role="presentation" が存在し、それだけでは特定出来ないことに注意
        presElem: WebElement = Presentations.getPresentation(token)

        # 追加する対象がいなくなるまでリストアップしてスクロール
        userSet = set()

        lastName = ""
        while True:
            # 表示要素からの相対パス div/div[2]/div/div の直下の div が良いねリスト
            favoriteElems = presElem.find_elements_by_xpath(FAVORITES_RELATIVE_XPATH)
            listLastName = favoriteElems[len(favoriteElems)-1].find_element_by_xpath(PROFILE_LINK_RELATIVE_XPATH).text
            if lastName == listLastName:
                break

            addCount = 0
            for favoriteElem in favoriteElems:
                nameElem: WebElement = favoriteElem.find_element_by_xpath(PROFILE_LINK_RELATIVE_XPATH)
                name = nameElem.text

                otherUser: OtherUser = OtherUser(name, False)
                if len(name) != 0 and not name in map(lambda otherUser: otherUser.name, userSet):
                    userSet.add(otherUser)
                    addCount = addCount + 1
                
                lastName = name

            JavaScript.scrollIntoView(token.driver, favoriteElems[len(favoriteElems)-1])

        logger.debug("favorite lists (size = {0})".format(len(userSet)))
        return list(userSet)

    def close(self, token: Token):
        if token.status != TokenStatus.FAVORITE_LIST:
            raise Exception()

        CLOSE_BUTTON_XPATH = "/html/body/div[4]/div/div[1]/div/div[2]/button"
        driver: Chrome = token.driver
        closeButtonElem = driver.find_element_by_xpath(CLOSE_BUTTON_XPATH)
        closeButtonElem.click()
        
        token.status = TokenStatus.POST