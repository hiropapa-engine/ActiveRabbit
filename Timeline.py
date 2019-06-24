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

from selenium.webdriver.remote.webelement import WebElement

from Token import Token
from Token import TokenStatus
from JavaScript import JavaScript
from ChromeDriver import ChromeDriver

class Timeline:
    POST_TAG_NAME = 'article'
    FAVOLITE_CSS = 'glyphsSpriteHeart__outline__24__grey_9'

    def __init__(self):
        pass

    '''
    最新のポストを取得
    '''
    def getRecentPost(self, token: Token) -> WebElement:
        logger.debug("getRecentPost() : start.")
        driver = token.driver
        if token.status != TokenStatus.NOT_LOG_IN and driver.current_url == 'https://www.instagram.com':
            logger.debug("getRecentPost() : error!! illegal token status.")
            raise Exception()

        recentPost: WebElement = None
        driver.implicitly_wait(0)
        try:
            logger.debug("getRecentPost() : get article.")
            recentPost = driver.find_element_by_tag_name("article")
        except:
            logger.debug("getRecentPost() : none articles.")
            pass
        driver.implicitly_wait(ChromeDriver.IMPLICIT_WAIT)
        logger.debug("getRecentPost() : end.")

        return recentPost


    '''
    タイムラインに"表示されている"投稿を取得する
    スクロール後を表示したい場合は基準となる投稿の article を指定する
    def getArticleViewPort(self, token: Token, article: WebElement = None) -> List[WebElement]:

        driver = token.driver
        if token.status != TokenStatus.NOT_LOG_IN and driver.current_url == 'https://www.instagram.com':
            raise Exception()

        # スクロール
        if article != None:
            JavaScript.scrollIntoView(driver, article)

        return driver.find_elements_by_tag_name("article")
    '''

    '''
    指定された投稿が良いね済みか判定
    '''
    def isFavorited(self, token: Token, article: WebElement) -> bool:
        logger.debug("isFavorited() : start.")
        driver = token.driver
        if token.status != TokenStatus.NOT_LOG_IN and driver.current_url == 'https://www.instagram.com':
            logger.debug("isFavorited() : error!! illegal token status.")
            raise Exception()

        favoriteIcon: WebElement = None

        driver.implicitly_wait(0)
        try:
            favoriteIcon: WebElement = article.find_element_by_class_name(Timeline.FAVOLITE_CSS)
        except:
            pass
        driver.implicitly_wait(ChromeDriver.IMPLICIT_WAIT)

        res: bool = favoriteIcon == None

        logger.debug("isFavorited() : end. ({0})".format(str(res)))
        return res


    '''
    指定された投稿に良いねする
    '''
    def favorite(self, token: Token, article: WebElement):
        logger.debug("favorite() : start.")
        driver = token.driver
        if token.status != TokenStatus.NOT_LOG_IN and driver.current_url == 'https://www.instagram.com':
            logger.debug("favorite() : error!! illegal token status.")
            raise Exception()

        JavaScript.scrollIntoView(driver, article)
        favoriteButton: WebElement = article.find_element_by_class_name(Timeline.FAVOLITE_CSS)
        favoriteButton.click()
        logger.debug("favorite() : end.")

import time

if __name__ == "__main__":
    session_id: str = input("ログイン済みセッションID : ")
    token: Token = Token("h.yamamoto900@gmail.com")
    token.driver = ChromeDriver().getDriver(session_id)

    timeline = Timeline()
    checksCount = 0
    lastArticle: WebElement = None
    checked: set = set()
    '''
    while True:
        # 表示中の投稿一覧を取得
        articles: List[WebElement] = timeline.getArticleViewPort(token, lastArticle)
        for article in articles:
            if article.id in checked:
                continue

            if not timeline.isFavorited(token, article):
                timeline.favorite(token, article)

            checked.add(article.id)
            if len(checked) >= 5:
                break

        # 5件チェックしたら終了
        if len(checked) >= 5:
            break

        # 5件チェックしていない場合はビューポートを変えて次へ
        lastArticle = articles[len(articles) - 1]
    '''
