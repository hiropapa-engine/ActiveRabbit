from __future__ import annotations

from Connection import Connection
from mysql.connector.cursor import MySQLCursorDict
import datetime
from typing import List
from UserData import UserData
from Instagram import Instagram
from Instagram import Token
from SlowStart import SlowStart
import random

from logging import getLogger, StreamHandler, DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

class FollowingTaskData:
    def __init__(self, id: int, execution_timing: datetime.datetime, target: str, follow_limit: int):
        self.id: int = id
        self.execution_timing: datetime.datetime = execution_timing
        self.target: str = target
        self.follow_limit: int = follow_limit

class FollowingSettings:
    def __init__(self, user_data: UserData):
        self.user_data: UserData = user_data

    def create_following_task_datas(self, base_date: datetime.datetime):
        logger.debug("フォロータスクデータ生成 : 開始 (id = {id})".format(id = self.user_data.id))
        query: str = None
        cur: MySQLCursorDict = Connection.cursor()
        targets: List[str] = []

        # ユーザーのフォロー数を取得
        token: Token = Instagram.rental_token(self.user_data.name, self.user_data.password)
        follow_list = Instagram.get_follows(token, self.user_data.name)
        Instagram.return_token(token)

        # フォロー数の半分による1日の最大フォロー数算出
        magnification = SlowStart.get_magnification(self.user_data)
        logger.debug("スロースタート倍率 : {0}".format(magnification))
        f_len = float(len(follow_list))
        max_by_follow_num: int = int(f_len / 2.0 * magnification)
        logger.debug("フォロー数からの最大フォロー数 : {}".format(max_by_follow_num))

        # 機能制限による1日の最大フォロー数算出
        query = "select * from limit_settings where owner = {id}".format(
            id = self.user_data.id
        )
        cur.execute(query)
        row = cur.fetchone()
        max_by_function_limit = row['follows']

        # インスタグラムのシステム制限による1日の最大フォロー数算出
        max_by_instagram = Instagram.FOLLOWS_LIMIT

        # 3つの最大フォロー数のうち最小のものを適用
        max_follow_num = min([max_by_follow_num, max_by_function_limit, max_by_instagram])
        max_follow_num = max([max_follow_num, 24])

        # ターゲットInstagramerを取得
        query = "select * from target_settings where owner = {owner_id}".format(
            owner_id = self.user_data.id
        )
        cur.execute(query)
        targets = list(map(lambda x: x['target'], cur.fetchall()))
        logger.debug("対象Instagramer : {0}".format(targets))


        # 曜日(0～6)を取得
        day_of_the_week = base_date.weekday()

        # 曜日の一致するレコードを取得するクエリ
        query = "select * from following_settings where owner = {0} ".format(self.user_data.id)
        query = query + "and ("
        query = query + "(weekday = {0} and hour between 4 and 23) ".format(day_of_the_week)
        query = query + "or (weekday = {0} and hour between 0 and 3)".format(day_of_the_week + 1)
        query = query + ")"

        logger.debug(query)

        # クエリ実行
        cur.execute(query)

        # 1タスク当たりのフォロー最大数を求める
        max_for_task = int(max_follow_num / cur.rowcount)
        reminder = max_follow_num % cur.rowcount

        # フォロータスクデータ生成(時・分)
        task_datas = []
        for row in cur.fetchall():
            exec_timing = None
            if row['weekday'] == day_of_the_week:
                exec_timing = datetime.datetime(
                    year=base_date.year,
                    month=base_date.month,
                    day=base_date.day,
                    hour=row['hour'],
                    minute=row['minutes'])
            else:
                tom = datetime.datetime(base_date + datetime.timedelta(day=1))
                logger.debug(type(tom))
                exec_timing = datetime.datetime(
                    year=tom.year,
                    month=tom.month,
                    day=tom.day,
                    hour=row['hour'],
                    minute=row['minutes'])

            task_data : FollowingTaskData = FollowingTaskData(
                id = self.user_data.id,
                execution_timing = exec_timing,
                target = targets[random.randint(0, len(targets) - 1)],
                follow_limit = max_for_task
            )
            task_datas.append(task_data)

        logger.debug("フォロータスク数 : {0}".format(len(task_datas)))

        while reminder > 0:
            index = random.randint(0, len(task_datas) - 1)
            task_datas[index].follow_limit = task_datas[index].follow_limit + 1
            reminder = reminder - 1

        for td in task_datas:
            query = "insert into following_tasks (owner, following_timing, target, following_limit) "
            query = query + "values({0}, '{1}', '{2}', {3})".format(td.id, td.execution_timing, td.target, td.follow_limit)
            logger.debug(query)
            cur.execute(query)

        logger.debug("フォロータスクデータ生成 : 終了")
