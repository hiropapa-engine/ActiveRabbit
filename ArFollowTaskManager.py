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

from ArUser import ArUser
from ArFollowTask import ArFollowTask

class ArFollowTaskManager:
    @classmethod
    def getFollowTasks(cls, user: ArUser) -> List[ArFollowTask]:
        # TODO: データベースからのタスク一覧取得処理実装
        followTasks: List[ArFollowTask] = []
        followTasks.append(ArFollowTask(user, "fukupiero_", 15))
        return followTasks