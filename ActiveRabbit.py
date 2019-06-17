from __future__ import annotations

from mysql.connector.cursor import MySQLCursorDict

from UserManager import UserManager
from User import User

from Connection import Connection
from TaskScheduler import TaskScheduler
from Instagram import Instagram

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
        # フォロータスク生成(タスクを生成したら、対象データは削除)
        # フォロータスク実行
        pass

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