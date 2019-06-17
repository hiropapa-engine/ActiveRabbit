from __future__ import annotations

from mysql.connector.cursor import MySQLCursorDict

from UserManager import UserManager
from User import User

from Connection import Connection
from TaskScheduler import TaskScheduler
from Instagram import Instagram

from FollowingTask import FollowingTask

import datetime

from logging import getLogger, StreamHandler, DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

class ActiveRabbit:

    @classmethod
    def processSchedulingTask(cls, user: User):
        scheduler: TaskScheduler = TaskScheduler
        scheduler.do(scheduler, user)

    @classmethod
    def processFollowingTask(cls, user: User):
        n = datetime.datetime.now()
        n_str = datetime.datetime.strftime(n, "%Y-%m-%d %H:%M:%S")
        # フォロータスク生成(タスクを生成したら、対象データは削除)
        cur = Connection.cursor()
        query = "select * from following_tasks where owner = {0}".format(user.user_data.id)
        query = query + " " + "and following_timing <= '{0}' order by owner".format(n_str)
        cur.execute(query)
        # フォロータスク実行
        for row in cur.fetchall():
            task: FollowingTask = FollowingTask(user.user_data, row['following_timing'], row['target'], row['following_limit'])
            task.do()

    @classmethod
    def processUnfollowingTask(cls, user: User):
        # フォロー解除タスク生成(タスクを生成したら、対象データは削除)
        # フォロー解除タスク実行
        pass

    @classmethod
    def processFollowingBackTask(cls, user: User):
        # フォロバタスク生成(フォロバは常時監視のため、対象データを削除しない)
        # フォロバタスク実行
        pass
    
    @classmethod
    def processFavorittingTask(cls, user: User):
        # 良いねタスク生成(良いねは常時監視のため、対象データを削除しない)
        # 良いねタスク実行
        pass

    @classmethod
    def do(cls):
        # コネクションオープン
        Connection.open()

        ''' ユーザー一覧を取得 '''
        userManager: UserManager = UserManager()

        for user in userManager.users():
            ''' スケジューリングタスク処理 '''
            cls.processSchedulingTask(user)

            ''' フォロータスク処理 '''
            cls.processFollowingTask(user)

            ''' フォロー解除タスク処理 '''
            cls.processUnfollowingTask(user)

            ''' フォロバタスク処理 '''
            cls.processFollowingBackTask(user)

            ''' 良いねタスク処理 '''
            cls.processFavorittingTask(user)

        # コネクションクローズ
        Connection.close

        # トークン破棄
        Instagram.destroy_token()

if __name__ == '__main__':
    ActiveRabbit.do()