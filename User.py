from __future__ import annotations

from datetime import date
from UserData import UserData
from FollowingSettings import FollowingSettings
import datetime

from logging import getLogger, StreamHandler, DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

class User:
    def __init__(self, user_data:UserData):
        self.user_data = user_data

    def create_following_tasks(self, base_date: datetime.datetime):
        logger.debug("フォロータスク生成開始")
        following_settings: FollowingSettings = FollowingSettings(self.user_data)
        following_settings.create_following_task_datas(base_date)
        logger.debug("フォロータスク生成終了")

'''
    def dump(self):
        print(self.id)
        print(self.name)
        print(self.password)
        print(self.start_date)
'''