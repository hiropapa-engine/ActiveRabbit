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

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.remote.webelement import WebElement

import sys

class ChromeDriver:
    IMPLICIT_WAIT: int = 10
    SCRIPT_WAIT: int = 5

    def __init__(self):
        self.driver = None
        pass

    def getDriver(self, session_id: str = None):
        logger.debug("getDriver() : 開始(session_id = {0})".format(session_id))
        options = webdriver.ChromeOptions()
        #options.binary_location = '/usr/bin/google-chrome'
        #options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36')

        logger.debug("getDriver() : リモートWebドライバ取得")
        driver = webdriver.Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=options.to_capabilities()
        )

        if session_id != None:
            logger.debug("getDriver() : 新規セッションの終了")
            driver.close()
            logger.debug("getDriver() : セッションの復元")
            driver.session_id = session_id

        logger.debug("getDriver() : タイムアウト値の設定")
        driver.implicitly_wait(ChromeDriver.IMPLICIT_WAIT)
        driver.set_script_timeout(ChromeDriver.SCRIPT_WAIT)

        logger.debug("getDriver() : 終了")
        return driver
