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

from selenium.webdriver import Chrome
from enum import Enum

class TokenStatus(Enum):
    NOT_LOG_IN = 1      # 未ログイン
    LOGGED_IN = 2       # ログイン済み
    USER = 3            # ユーザーページ表示中
    POST = 4            # 投稿表示中
    FAVORITE_LIST = 5   # いいねリスト表示中
    FOLLOWING = 6        # フォローリスト表示中

class Token:
    PAGE_WAIT: int = 2
    RETRY: int = 5

    def __init__(self, name: str, session_id: str = None):
        self.name: str = name
        self.session_id = session_id
        self.driver: Chrome = None
        self.status: TokenStatus = TokenStatus.NOT_LOG_IN

