from __future__ import annotations

from logging import getLogger, StreamHandler, DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
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
    FOLLOING = 6        # フォローリスト表示中

class Token:
    PAGE_WAIT: int = 2
    RETRY: int = 5

    def __init__(self, name: str):
        self.name: str = name
        self.driver: Chrome = None
        self.status: TokenStatus = TokenStatus.NOT_LOG_IN

