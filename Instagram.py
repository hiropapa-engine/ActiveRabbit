from __future__ import annotations

from typing import Dict
from typing import List

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import WebDriverException

import urllib.parse

import time

import sys

from logging import getLogger, StreamHandler, DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

class Token:
    browser: webdriver.Chrome = None

    def __init__(self, name: str, password: str):
        self.name: str = name
        self.password: str = password

class Instagram:

    tokens: Dict[str, Token] = {}
    FOLLOWS_LIMIT: int = 200
    FAVORITES_LIMIT: int = 500
    UNFOLLOWS_LIMIT: int = 150

    @classmethod
    def rental_token(cls, name: str, password: str) -> Token:
        if not name in cls.tokens.keys():
            token: Token = Token(name, password)
            cls.tokens[name] = token
        return cls.tokens[name]

    @classmethod
    def return_token(cls, token: Token):
        token.browser.close()
        cls.tokens.pop(token.name)

    @classmethod
    def destroy_token(cls):
        for token in cls.tokens.values():
            token.browser.close()

    @classmethod
    def get_follows(cls, token: Token, name: str) -> List[str]:
        logger.debug("フォローリスト取得 : 開始")
        followPath: str = '//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a/span'
        followedUserPath: str = '/html/body/div[3]/div/div[2]/ul/div/li[*]/div/div[1]/div[2]/div[1]/a'

        # 未ログイン(プラウザ未生成)の場合はログイン
        if token.browser == None:
            cls.logging_in(token)

        # 指定ユーザーのトップページを表示
        cls.show(token, name)

        browser: webdriver.Chrome = token.browser

        # トップページから「フォロー数」を取得
        follow_num_elem = browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a/span')
        follow_num = int(follow_num_elem.text)
        logger.debug("フォロー数 : {0}".format(follow_num))

        # 「フォロー」をクリック
        logger.debug("フォローをクリック")
        browser.find_element_by_xpath(followPath).click()
        time.sleep(5)

        # フォロー数とエレメント数が一致するまで PageDownキーを押す
        while True:
            # エレメントリストを取得
            followed_element_list: List[WebElement] = browser.find_elements_by_xpath(followedUserPath)

            l = len(followed_element_list)
            if l == follow_num:
                break

            last_element = followed_element_list[l - 1]
            browser.execute_script("arguments[0].scrollIntoView();", last_element)

        # 「フォロー中」ユーザー名リストを取得
        followed_user_list: List[str] = list(map(lambda x: x.text, followed_element_list))

        logger.debug("フォローリスト : {0}".format(followed_user_list))
        logger.debug("フォローリスト取得 : 終了")

        return followed_user_list

    @classmethod
    def logging_in(cls, token: Token):
        logger.debug("インスタグラムにログイン : name={}".format(token.name))
        loginURL: str = "https://www.instagram.com/"
        loginPath: str = '//*[@id="react-root"]/section/main/article/div[2]/div[2]/p/a'
        usernamePath: str = '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[2]/div/div[1]/input'
        passwordPath = '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[3]/div/div[1]/input'
        loggedInPath = '//*[@id="react-root"]/section/main/div/header/section/div[1]/h1'

        if not token.browser is None:
            logger.debug("=> ログイン済み")
            return

        browser: webdriver.Chrome = None
        if '--release' not in sys.argv:
            browser = webdriver.Chrome()
        else:
            options = Options()
            options.add_argument('--headless')
            browser = webdriver.Chrome(options=options)

        # ログインURL表示
        browser.get(loginURL)
        logging_in: WebElement = browser.find_element_by_xpath(loginPath)
        logger.debug("トップ画面待ち")
        browser.implicitly_wait(30)

        # ログインボタンクリック
        logging_in.click()

        # ユーザー名入力
        username_field: WebElement = browser.find_element_by_xpath(usernamePath)
        logger.debug("ログイン画面待ち")
        browser.implicitly_wait(30)

        username_field.send_keys(token.name)
        time.sleep(5)

        # パスワードを入力
        password_field: WebElement = browser.find_element_by_xpath(passwordPath)
        password_field.send_keys(token.password)

        # Enterキー押下
        password_field.send_keys(Keys.RETURN)
        time.sleep(5)

        # ログイン後、自分のページに飛ぶ
        instagramerURL: str = "https://www.instagram.com/{}/?hl=ja"
        encoded_name = urllib.parse.quote(token.name)
        encoded_url: str = instagramerURL.format(encoded_name)
        browser.get(encoded_url)

        # アカウント名が表示されればログイン完了
        logged_in: WebElement = browser.find_element_by_xpath(loggedInPath)
        logger.debug("自分のトップページ待ち")
        browser.implicitly_wait(30)

        instagram_name: str = logged_in.text

        if not instagram_name == token.name:
            raise Exception

        # トークンにブラウザを登録
        token.browser = browser
        logger.debug("ログイン完了")

    @classmethod
    def show(cls, token: Token, name: str):

        logger.debug("ユーザートップページ表示 : user = {0}, name={1}".format(token.name, name))

        if token.browser == None:
            cls.logging_in(token)

        instagramerURL: str = "https://www.instagram.com/{}/?hl=ja"
        encoded_name = urllib.parse.quote(token.name)
        encoded_url: str = instagramerURL.format(encoded_name)
        token.browser.get(encoded_url)

        loggedInPath = '//*[@id="react-root"]/section/main/div/header/section/div[1]/h1'
        logged_in: WebElement = token.browser.find_element_by_xpath(loggedInPath)
        logger.debug("トップページ待ち")
        token.browser.implicitly_wait(30)

        instagram_name: str = logged_in.text

        if not instagram_name == token.name:
            raise Exception

        logger.debug("表示完了")
