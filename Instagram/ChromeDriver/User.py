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
from Post import Post
from Following import Following

from selenium.webdriver import Chrome
from selenium.webdriver.remote.webelement import WebElement

import urllib.parse
import time
from typing import List

class User:

    FOLLOWING_ELEMS_XPATH = '//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a/span'

    def __init__(self, name: str):
        self.name = name

    def show(self, token: Token):
        INSTAGRAMMER_URL: str = "https://www.instagram.com/{}/?hl=ja"
        USER_NAME_XPATH: str = '//*[@id="react-root"]/section/main/div/header/section/div[1]/h1'

        if token.status != TokenStatus.LOGGED_IN:
            raise Exception

        showUrl: str = INSTAGRAMMER_URL.format(urllib.parse.quote(self.name))

        driver = token.driver
        driver.get(showUrl)

        # 表示確認
        time.sleep(Token.PAGE_WAIT)
        userNameElem: WebElement = driver.find_element_by_xpath(USER_NAME_XPATH)
        if userNameElem.text != self.name:
            raise Exception
        
        token.status = TokenStatus.USER

    def showRecentPost(self, token: Token) -> Post:
        MEDIA_SELECTOR_XPATH = '//*[@id="react-root"]/section/main/div/div[@class=" _2z6nI"]/article/div[1]/div/div[*]/div[*]/a/div[1]/div[2]'

        if token.status != TokenStatus.USER:
            raise Exception

        driver: Chrome = token.driver

        mediaElem: WebElement = driver.find_element_by_xpath(MEDIA_SELECTOR_XPATH)
        mediaElem.click()

        retryCount: int = 0
        while True:
            try:
                mediaDialogElems: List[WebElement] = driver.find_elements_by_xpath(Post.MEDIA_DIALOG_XPATH)

                if mediaDialogElems[0].is_displayed():
                    break

            except Exception as e:
                retryCount = retryCount + 1
                if retryCount >= Token.RETRY:
                    raise e

        token.status = TokenStatus.POST
        return Post(self)

    def getFollowingNum(self, token: Token) -> int:

        if token.status != TokenStatus.USER:
            raise Exception

        # トップページからフォロー数を取得
        driver = token.driver
        followingElem: WebElement = driver.find_element_by_xpath(User.FOLLOWING_ELEMS_XPATH)
        return int(followingElem.text)

    def showFollowing(self, token: Token) -> Following:

        if token.status != TokenStatus.USER:
            raise Exception

        # 「nn人をフォロー中」をクリック
        driver = token.driver
        followingElem: WebElement = driver.find_element_by_xpath(User.FOLLOWING_ELEMS_XPATH)
        followingElem.click()

        retryCount: int = 0
        while True:
            try:
                mediaDialogElems: List[WebElement] = driver.find_elements_by_xpath(Post.MEDIA_DIALOG_XPATH)

                if mediaDialogElems[0].is_displayed():
                    break

            except Exception as e:
                retryCount = retryCount + 1
                if retryCount >= Token.RETRY:
                    raise e

        return Following(self)

from Login import Login
import sys
if __name__ == "__main__":
    token: Token = Token("h.yamamoto900@gmail.com")
    Login().doLogin(token, "Sorachan20100605")
    user: User = User("watanabenaomi703")
    user.show(token)
    logger.debug("ユーザー({0})のフォロー数 : {1}".format(user.name, str(user.getFollowingNum(token))))
    post: Post = user.showRecentPost(token)
    input("Press any key to close.")
    post.close(token)
    input("Press any key to show following.")
    user.showFollowing(token)
    input("Press any key to exit.")
