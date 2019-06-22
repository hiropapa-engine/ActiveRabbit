from __future__ import annotations

from logging import getLogger, StreamHandler, DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
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
        if '--release' in sys.argv:
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            driver = webdriver.Chrome(executable_path='/home/vpsuser/py3env/lib/python3.6/site-packages/chromedriver_binary/chromedriver', chrome_options=options)
        elif '--headless' in sys.argv:
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            driver = webdriver.Chrome(chrome_options=options)
        elif session_id == None:
            driver = webdriver.Remote(
                command_executor='http://127.0.0.1:4444/wd/hub',
                desired_capabilities=DesiredCapabilities.CHROME
            )

            logger.debug("executor_url : %s" % driver.command_executor._url)
            logger.debug("session_id   : %s" % driver.session_id)
        else:
            driver = webdriver.Remote(
                command_executor='http://127.0.0.1:4444/wd/hub',
                desired_capabilities=DesiredCapabilities.CHROME
            )
            driver.close()
            driver.session_id = session_id

        driver.implicitly_wait(ChromeDriver.IMPLICIT_WAIT)
        driver.set_script_timeout(ChromeDriver.SCRIPT_WAIT)

        return driver
