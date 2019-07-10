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

from typing import List
from datetime import datetime
from datetime import timedelta
import random

from mysql.connector.cursor import MySQLCursorDict

from ArConnection import ArConnection
from ArLogin import ArLogin
from ArUserManager import ArUserManager
from ArUser import ArUser
from ArUserRestriction import ArUserRestriction
from ArInstagram import ArInstagram
from ArFollowTask import ArFollowTask
from ArFollowTaskManager import ArFollowTaskManager

from Instagram.ChromeDriver.User import User

class ArFollowTaskScheduler:

    @classmethod
    def createFollowTask(cls):
        ArConnection.open()
        # ユーザーマネージャーを利用してユーザーを取得する
        users: List[ArUser] = ArUserManager.getUsers()

        for user in users:
            ArLogin.do(user, user.getPassword())
            ArFollowTaskScheduler.processUser(user)

        ArConnection.close()

    @classmethod
    def processUser(cls, user: ArUser):
        # 0. ユーザー設定の取得
        restriction: ArUserRestriction = user.getRestriction()

        # 1. ユーザーのフォロー上限（プランによる機能制限）を取得する
        follow_limit_by_plan = restriction.follow_limit

        # 2. インスタグラムのフォロー数制限を取得する
        follow_limit_per_day = ArInstagram.getFollowLimitPerDay()

        # 3. フォロー数による1日の最大フォロー数算出
        # ユーザーのフォロー数を取得する
        instance = User(user.name)
        instance.show(user.token)
        following_num: int = instance.getFollowingNum(user.token)

        # フォロー数の1/2を求める
        # フォロー数から算出した最大フォロー数にスロースタートを適用(運用開始5日目まで)
        follow_limit_by_following: int = following_num / 2
        ds: int = (datetime.today() - datetime(user.start_date.year, user.start_date.month, user.start_date.day)).days
        if restriction.slow_start_enabled and ds <= 4:
            multiplex_slow_start: List[float] = [0.1, 0.2, 0.3, 0.4, 0.5]
            follow_limit_by_following = follow_limit_by_following * multiplex_slow_start[ds]

        # 1, 2, 3 のうち最も小さい数字を最大フォロー数として採用する
        # ※ただし、最少は24とする
        follow_limit: int = min([follow_limit_by_plan, follow_limit_per_day, follow_limit_by_following])
        follow_limit = max([follow_limit, 24])

        # データベースから、タスクデータの生成設定を取得する
        # スティール対象取得
        trackings: List[str] = []
        query: str = "select * from user_trackings where owner_id = {owner_id}"
        query = query.format(owner_id = user.id)
        cur : MySQLCursorDict = ArConnection.cursor()
        cur.execute(query)
        for row in cur.fetchall():
            trackings.append(row['tracked_name']) 

        # 当日
        tasks: List[ArFollowTask] = []
        query = "select * from user_schedule where owner_id = {owner_id} and weekday = {week_day} and hours >= 5 and hours <= 23 and enabled = 1"
        query = query.format(owner_id = user.id, week_day = datetime.now().weekday())
        cur.execute(query)
        td: datetime = datetime.today()
        for row in cur.fetchall():
            task = ArFollowTask(
                user,
                datetime(
                    td.year,
                    td.month,
                    td.day,
                    row['hours'],
                    row['minutes']
                ),
                random.choice(trackings),
                0   # 仮に0
            )
            tasks.append(task)

        # 翌日
        query = "select * from user_schedule where owner_id = {owner_id} and weekday = {week_day} and hours >= 0 and hours <= 4 and enabled = 1"
        query = query.format(owner_id = user.id, week_day = (datetime.now().weekday() + 1) % 7)
        cur.execute(query)
        nd: datetime = td + timedelta(days = 1)
        for row in cur.fetchall():
            task = ArFollowTask(
                user,
                datetime(
                    nd.year,
                    nd.month,
                    nd.day,
                    row['hours'],
                    row['minutes']
                ),
                random.choice(trackings),
                0   # 仮に0
            )
            tasks.append(task)

        # 1タスク当たりのフォロー人数と余りを求める
        follow_per_task, follow_random = divmod(follow_limit , len(tasks))

        # フォロー人数を設定
        for t in tasks:
            t.followNum = follow_per_task

        # 余り分の要素をランダムに割り振る
        if follow_random > 0:
            for t in random.choices(tasks, k=follow_random):
                t.followNum = t.followNum + 1

        # タスクをデータベースに保存
        for t in tasks:
            ArFollowTaskManager.insertFollowTask(t)

        cur.close()

if __name__ == "__main__":
    ArFollowTaskScheduler.createFollowTask()