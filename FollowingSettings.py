from __future__ import annotations

from Connection import Connection
from mysql.connector.cursor import MySQLCursorDict
import datetime
from typing import List
from UserData import UserData
from Instagram import Instagram
from Instagram import Token

from logging import getLogger, StreamHandler, DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

class FollowingSetting:
    def __init__(self, id: int, execution_timing: datetime.datetime, target: str, follow_limit: int):
        self.id: int = id
        self.execution_timing: datetime.datetime = execution_timing
        self.target: str = target
        self.follow_limit: int = follow_limit

class FollowingSettings:
    def __init__(self, user_data: UserData):
        self.user_data: UserData = user_data

    def create_following_task_datas(self):
        logger.debug("フォロータスクデータ生成 : 開始 (id = {id})".format(id = self.user_data.id))
        query: str = None
        cur: MySQLCursorDict = Connection.cursor()
        targets: List[str] = []

        # ユーザーのフォロー数を取得
        token: Token = Instagram.rental_token(self.user_data.name, self.user_data.password)
        Instagram.get_follows(token, self.user_data.name)
        Instagram.return_token(token)

        # ターゲットInstagramerを取得
        query = "select * from target_settings where owner = {owner_id}".format(
            owner_id = self.user_data.id
        )
        cur.execute(query)

        targets = list(map(lambda x: x['target'], cur.fetchall()))
        logger.debug("対象Instagramer : {0}".format(targets))

        # 曜日(0～6)を取得
        today: datetime.datetime = datetime.datetime.now()
        day_of_the_week = today.weekday()

        # 曜日の一致するレコードを取得するクエリ
        query = "select * from following_settings where owner = {owner_id} and weekday = {weekday}".format(
            owner_id = self.user_data.id,
            weekday = day_of_the_week
        )

        # クエリ実行
        cur.execute(query)

        # フォロータスクデータ生成(時・分)


        logger.debug("フォロータスクデータ生成 : 終了")
