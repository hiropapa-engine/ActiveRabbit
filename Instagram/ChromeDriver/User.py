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

import urllib.parse
import time
from typing import List

from selenium.webdriver import Chrome
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from Token import Token
from Token import TokenStatus
from Post import Post
from Favorites import Favorites
from Following import Following

class User:

    FOLLOWING_ELEMS_XPATH = '//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a/span'
    FOLLOWING_LINKS_XPATH = '//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a'

    def __init__(self, name: str):
        self.name = name

    def show(self, token: Token):
        INSTAGRAMMER_URL: str = "https://www.instagram.com/{}/?hl=ja"
        USER_NAME_XPATH: str = '//*[@id="react-root"]/section/main/div/header/section/div[1]/h1'

        if token.status == TokenStatus.NOT_LOG_IN:
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

        # ToDo : 投稿が表示されたかチェック

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

        # 「nn人をフォロー中」リンクをクリック
        self.show(token)
        driver: Chrome = token.driver
        followingElem: WebElement = driver.find_element_by_xpath(User.FOLLOWING_LINKS_XPATH)
        followingElem.click()

        # ToDo : フォロー中ダイアログが表示されたかチェック

        token.status = TokenStatus.FOLLOWING

        return Following(self)

from ChromeDriver import ChromeDriver

if __name__ == "__main__":

    session_id: str = input("ログイン済みセッションID : ")
    token: Token = Token("h.yamamoto900@gmail.com")
    token.driver = ChromeDriver().getDriver(session_id)
    token.status = TokenStatus.LOGGED_IN

    user: User = User("misumisu0722")
    time.sleep(1)
    user.show(token)
    logger.debug("ユーザー({0})のフォロー数 : {1}".format(user.name, str(user.getFollowingNum(token))))
    time.sleep(1)
    post: Post = user.showRecentPost(token)
    time.sleep(1)
    user = post.close(token)
    time.sleep(1)
    following: Following = user.showFollowing(token)
    time.sleep(1)
    following.close(token)
    input("Press any key to close.")
