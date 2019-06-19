from __future__ import annotations

from logging import getLogger, StreamHandler, DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

from Post import Post
from Token import Token
from Token import TokenStatus
from selenium.webdriver import Chrome
from selenium.webdriver.remote.webelement import WebElement
from typing import List

class RecentPost(Post):

    def show(self, token: Token) -> Post:
        MEDIA_SELECTOR_XPATH = '//*[@id="react-root"]/section/main/div/div[@class=" _2z6nI"]/article/div[1]/div/div[*]/div[*]/a/div[1]/div[2]'

        if token.status != TokenStatus.USER:
            raise Exception

        driver: Chrome = token.driver

        mediaElem: WebElement = driver.find_element_by_xpath(MEDIA_SELECTOR_XPATH)
        mediaElem.click()

        mediaDialogElems: List[WebElement] = driver.find_elements_by_xpath(Post.MEDIA_DIALOG_XPATH)

        if not mediaDialogElems[0].is_displayed():
            raise Exception

        token.status = TokenStatus.POST
        return self

from Login import Login
from User import User
if __name__ == '__main__':
    token: Token = Token("h.yamamoto900@gmail.com")
    Login().doLogin(token, "Sorachan20100605")
    User().show(token, "hiroyuki.happy.papa")
    post: Post = RecentPost().show(token)
    favorited: bool = RecentPost().isFavorited(token)
    logger.debug("最新投稿 良いね済み = {}".format(favorited))
    input("Press key to next.")
    post = post.next(token)
    favorited: bool = RecentPost().isFavorited(token)
    logger.debug("直前投稿 良いね済み = {}".format(favorited))
    post.favorite(token)
    input("Press key to exit.")
