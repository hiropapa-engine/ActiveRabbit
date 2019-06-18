from __future__ import annotations

from logging import getLogger, StreamHandler, DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

from Token import Token
from selenium.webdriver import Chrome
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
import time
import sys
import traceback
import time

class Login:

    @classmethod
    def do(cls, token: Token, password: str):
        LOGIN_URL: str = "https://www.instagram.com/"
        LOGIN_LINK_XPATH: str = '//*[@id="react-root"]/section/main/article/div[2]/div[2]/p/a'
        USER_NAME_NAME_ATTRIBUTE: str = 'username'
        PASSWORD_NAME_ATTRIBUTE: str = 'password'
        
        LOGIN_COMPLETE_XPATH: str = '//*[@id="react-root"]'

        # Chromeオブジェクト(Element30秒待ち)の生成
        driver: Chrome = Chrome()
        driver.implicitly_wait(10)

        success: bool = False
        retryCounter = 5
        while retryCounter > 0:
            try:
                driver.get(LOGIN_URL)

                # ログインリンクをクリック
                loginLink: WebElement = driver.find_element_by_xpath(LOGIN_LINK_XPATH)
                loginLink.click()

                # ユーザー名/パスワード入力欄 取得
                time.sleep(Token.PAGE_WAIT)
                userNameField: WebElement = driver.find_element_by_name(USER_NAME_NAME_ATTRIBUTE)
                passwordField: WebElement = driver.find_element_by_name(PASSWORD_NAME_ATTRIBUTE)

                # ユーザー名/パスワードを入力
                userNameField.send_keys(token.name)
                passwordField.send_keys(password)

                # Enterキー押下
                passwordField.send_keys(Keys.RETURN)

                # 次ページ表示されればログイン完了
                time.sleep(Token.PAGE_WAIT)
                driver.find_element_by_xpath(LOGIN_COMPLETE_XPATH)
                success = True
                break
            except Exception as e:
                logger.debug("Login failed.")
                t, v, tb = sys.exc_info()
                logger.debug(traceback.format_exception(t, v, tb))
                logger.debug(traceback.format_tb(e.__traceback__))
                retryCounter = retryCounter - 1

        if not success:
            raise Exception

        # メンバ変数にChromeドライバを保持
        token.driver = driver

if __name__ == '__main__':
    for i in range(1, 100):
        logger.debug("Trying {}.".format(str(i)))
        token: Token = Token("h.yamamoto900@gmail.com")
        Login.do(token, "Sorachan20100605")
        if token.isLoggedIn():
            logger.debug("OK.")
            time.sleep(2)
        else:
            logger.debug("NG")
            break
    input("Please input any key.")