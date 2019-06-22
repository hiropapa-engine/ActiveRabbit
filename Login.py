from __future__ import annotations

from logging import getLogger, StreamHandler, DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

import time
import sys
import traceback

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys

from Token import Token
from Token import TokenStatus
from ChromeDriver import ChromeDriver

class Login:

    def doLogin(self, token: Token, password: str):
        logger.debug("Login.doLogin : 開始(token.user = {0})".format(token.name))

        LOGIN_URL: str = "https://www.instagram.com/"
        LOGIN_LINK_XPATH: str = '//*[@id="react-root"]/section/main/article/div[2]/div[2]/p/a'
        NOTICE_AFTER_BUTTON_XPATH: str = '/html/body/div[3]/div/div/div[3]/button[2]'
        USER_NAME_NAME_ATTRIBUTE: str = 'username'
        PASSWORD_NAME_ATTRIBUTE: str = 'password'
        
        LOGIN_COMPLETE_XPATH: str = '//*[@id="react-root"]'

        # Chromeオブジェクト(Element30秒待ち)の生成
        driver = ChromeDriver().getDriver()

        retryCounter = 5
        while retryCounter > 0:
            try:
                logger.debug('Login.doLogin : driver.get("{0}")'.format(LOGIN_URL))
                driver.get(LOGIN_URL)

                # ログインリンクをクリック
                logger.debug('Login.doLogin : driver.find_element_by_xpath("{0}")'.format(LOGIN_LINK_XPATH))
                loginLink: WebElement = driver.find_element_by_xpath(LOGIN_LINK_XPATH)
                loginLink.click()

                # ユーザー名/パスワード入力欄 取得
                time.sleep(Token.PAGE_WAIT)
                logger.debug('Login.doLogin : driver.find_element_by_name("USER_NAME_NAME_ATTRIBUTE")')
                userNameField: WebElement = driver.find_element_by_name(USER_NAME_NAME_ATTRIBUTE)
                logger.debug('Login.doLogin : driver.find_element_by_name("PASSWORD_NAME_ATTRIBUTE")')
                passwordField: WebElement = driver.find_element_by_name(PASSWORD_NAME_ATTRIBUTE)

                # ユーザー名/パスワードを入力
                logger.debug('Login.doLogin : userNameField.send_keys("{0}")'.format(token.name))
                userNameField.send_keys(token.name)
                logger.debug('Login.doLogin : passwordField.send_keys("******")')
                passwordField.send_keys(password)

                # Enterキー押下
                logger.debug('Login.doLogin : passwordField.send_keys(Keys.RETURN)')
                passwordField.send_keys(Keys.RETURN)

                # お知らせをオンにする / あとでの「あとで」をクリック
                time.sleep(Token.PAGE_WAIT)
                try:
                    logger.debug('Login.doLogin : driver.find_element_by_xpath("NOTICE_AFTER_BUTTON_XPATH")')
                    noticeAfterButtonElem: WebElement = driver.find_element_by_xpath(NOTICE_AFTER_BUTTON_XPATH)
                    noticeAfterButtonElem.click()
                except:
                    logger.debug('Login.doLogin : skip.')

                # ページ表示されたらログイン完了
                logger.debug('Login.doLogin : driver.find_element_by_xpath(LOGIN_COMPLETE_XPATH)')
                driver.find_element_by_xpath(LOGIN_COMPLETE_XPATH)

                # トークンの状態をログイン済みに設定
                token.status = TokenStatus.LOGGED_IN
                break
            except Exception as e:
                logger.debug('Login failed.')
                t, v, tb = sys.exc_info()
                logger.debug(traceback.format_exception(t, v, tb))
                logger.debug(traceback.format_tb(e.__traceback__))
                retryCounter = retryCounter - 1

        if token.status != TokenStatus.LOGGED_IN:
            raise Exception

        # メンバ変数にChromeドライバを保持
        token.driver = driver

        logger.debug('Login.doLogin : 正常終了')

import selenium

if __name__ == '__main__':
    for i in range(1, 2):
        logger.debug("Trying {}.".format(str(i)))
        token: Token = Token("h.yamamoto900@gmail.com")
        Login().doLogin(token, "Sorachan20100605")
        if token.status == TokenStatus.LOGGED_IN:
            logger.debug("OK.")
            time.sleep(2)
        else:
            logger.debug("NG")
            break
