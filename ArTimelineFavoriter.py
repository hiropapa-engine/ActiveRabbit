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

from ArUser import ArUser

class ArTimelineFavoriter:

    @classmethod
    def do(cls, user: ArUser, password: str):
        # ログイン
        token: Token = Token(user.name, user.session_id)
        Login().doLogin(token, password)
        user.session_id = token.session_id
        user.saveSession()

        # タイムラインの最新投稿を取得
        timeline = Timeline()
        recentPost = timeline.getRecentPost(token)
        if recentPost != None:
            if not timeline.isFavorited(token, recentPost):
                timeline.favorite(token, recentPost)
