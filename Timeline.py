from __future__ import annotations

from logging import getLogger, StreamHandler, DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
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
    FAVOLITE_CSS = 'glyphsSpriteHeart__outline__24__grey_9'

    def __init__(self):
        pass

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

        driver = token.driver
        if token.status != TokenStatus.NOT_LOG_IN and driver.current_url == 'https://www.instagram.com':
            raise Exception()

        favoriteIcon: WebElement = None

        driver.implicitly_wait(0)
        try:
            favoriteIcon: WebElement = article.find_element_by_class_name(Timeline.FAVOLITE_CSS)
        except:
            pass
        driver.implicitly_wait(ChromeDriver.IMPLICIT_WAIT)

        return favoriteIcon == None


    '''
    指定された投稿に良いねする
    '''
    def favorite(self, token: Token, article: WebElement):

        driver = token.driver
        if token.status != TokenStatus.NOT_LOG_IN and driver.current_url == 'https://www.instagram.com':
            raise Exception()

        favoriteButton: WebElement = article.find_element_by_class_name(Timeline.FAVOLITE_CSS)
        JavaScript.scrollIntoView(driver, article)

        favoriteButton.click()

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
