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

from mysql.connector.cursor import MySQLCursorDict

from ArConnection import ArConnection
from ArUser import ArUser
from ArFollowTask import ArFollowTask

class ArFollowTaskManager:
    @classmethod
    def getFollowTasks(cls, user: ArUser) -> List[ArFollowTask]:
        cur: MySQLCursorDict= ArConnection.cursor()
        query: str = "select * from following_tasks where owner_id = {0} and execute_timing <= NOW()"
        query = query.format(str(user.id))
        cur.execute(query)

        followTasks: List[ArFollowTask] = []

        for row in cur.fetchall():
            task: ArFollowTask = ArFollowTask(
                user,
                row['execute_timing'],
                row['target'],
                row['following_limit']
            )
            followTasks.append(task)
        return followTasks

    @classmethod
    def deleteFollowTask(cls, task: ArFollowTask):
        cur: MySQLCursorDict= ArConnection.cursor()
        query: str = "delete from following_tasks where owner_id = {0} and execute_timing = '{1:%Y-%m-%d %H:%M:%S}'"
        query = query.format(str(task.user.id), task.executeTiming)
        cur.execute(query)
