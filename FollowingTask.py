from __future__ import annotations

from UserData import UserData
from Instagram import Instagram
from Instagram import Token
from Connection import Connection
from mysql.connector.cursor import MySQLCursorDict

import datetime

from logging import getLogger, StreamHandler, DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

class FollowingTask:
    def __init__(self, user_data: UserData, following_timing: datetime.datetime, target: str, following_limit: int):
        self.user_data = user_data
        self.following_timing = following_timing
        self.target = target
        self.following_limit = following_limit

    def do(self):
        # Instagramからトークン取得
        token: Token = Instagram.rental_token(self.user_data.name, self.user_data.password)
    
        # ターゲットのページを表示
        Instagram.show(token, self.target)

        # 最新の投稿を表示
        Instagram.latest_post(token)

        # 良いねリストを表示
        Instagram.favorites_list(token)

        # 最新投稿に良いねしていてフォローしていない人のリストを取得
        follow_list = Instagram.following_list(token, self.following_limit)
        logger.debug("フォロー対象はコレ！ : {0}".format(follow_list))

        # タスクが紐づくフォロータスクデータを削除
        query: str = "delete from following_tasks where owner={0} and following_timing='{1}'"
        query = query.format(self.user_data.id, datetime.datetime.strftime(self.following_timing, '%Y-%m-%d %H:%M:%S'))
        cursor: MySQLCursorDict = Connection.cursor()
        cursor.execute(query)
