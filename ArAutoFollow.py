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

from ArFollowTaskManager import ArFollowTaskManager
from ArFollowTask import ArFollowTask
from ArUser import ArUser

class ArAutoFollow:
    @classmethod
    def do(cls, user: ArUser):
        # フォロータスクマネージャから対象ユーザーのフォロータスクを取得する
        followTasks: List[ArFollowTask] = ArFollowTaskManager.getFollowTasks(user)

        # フォロータスクを実行する
        for follow in followTasks:
            follow.do()

if __name__ == '__main__':
    ArAutoFollow.do(None)
    logger.debug("テスト")