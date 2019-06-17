from __future__ import annotations

from datetime import date
from UserData import UserData
from FollowingSettings import FollowingSettings

from logging import getLogger, StreamHandler, DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

class User:
    def __init__(self, id: int, name: str, password: str, start_date: date):
        self.user_data: UserData = UserData(
            id,
            name,
            password,
            start_date
        )

    def create_following_tasks(self):
        logger.debug("フォロータスク生成開始")
        following_settings: FollowingSettings = FollowingSettings(self.user_data)
        following_settings.create_following_task_datas()
        logger.debug("フォロータスク生成終了")

'''
    def dump(self):
        print(self.id)
        print(self.name)
        print(self.password)
        print(self.start_date)
'''