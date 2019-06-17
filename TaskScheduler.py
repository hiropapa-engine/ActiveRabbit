from __future__ import annotations

from User import User
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

class TaskScheduler:
    
    def __init__(self):
        pass

    def do(self, user: User):
        logger.debug('スケジューリングタスク : 起動 (owner_id = {owner_id})'.format(owner_id=user.user_data.id))

        fmt: str = '%Y-%m-%d %H:%M:%S'
        query: str = None
        execution_timing: datetime.datetime = None
        next_timing: datetime.datetime = None

        cur: MySQLCursorDict = Connection.cursor()

        # スケジューリングタスクデータ取得
        query = "select * from scheduling_tasks where owner={owner_id} and execution_timing < '{now}'".format(
            owner_id=user.user_data.id,
            now=datetime.datetime.now().strftime(fmt)
        )
        cur.execute(query)
        logger.debug('スケジューリングタスク : 取得件数 {0} 件'.format(cur.rowcount))
        if cur.rowcount == 0:
            logger.debug('スケジューリングタスク : 終了 (無処理)')
            return

        # スケジューリングタスク実行
        for row in cur.fetchall():
            execution_timing = row['execution_timing']

            # ユーザーがフォロータスクを生成
            user.create_following_tasks()
            
        # 処理完了したのでスケジューリングタスクデータを削除
        logger.debug('スケジューリングタスク : 処理済みデータ削除')
        query = "delete from scheduling_tasks where owner={owner_id}".format(
            owner_id=user.user_data.id
        )
        #cur.execute(query)

        # 翌日のスケジューリングタスクデータ生成
        next_timing = execution_timing + datetime.timedelta(days=1)
        logger.debug('スケジューリングタスク : タスクデータ生成 : {0}'.format(next_timing))
        query: str = "insert into scheduling_tasks (owner, execution_timing) values({owner_id}, '{exec_timing}')".format(
            owner_id = row['owner'],
            exec_timing = datetime.datetime.strftime(next_timing, fmt)
        )
        #cur.execute(query)
        logger.debug('スケジューリングタスク : 終了')
