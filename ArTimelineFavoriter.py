from __future__ import annotations

from logging import getLogger, StreamHandler, DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

from typing import List

from Token import Token
from Login import Login
from Timeline import Timeline

class ArTimelineFavoriter:

    @classmethod
    def do(cls, name: str, password: str):
        # ログイン
        token: Token = Token(name)
        Login().doLogin(token, password)

        # タイムラインの最新投稿を取得
        timeline = Timeline()
        recentPost = timeline.getRecentPost(token)
        if recentPost != None:
            if not timeline.isFavorited(token, recentPost):
                timeline.favorite(token, recentPost)

        token.driver.close()