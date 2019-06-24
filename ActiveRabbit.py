from __future__ import annotations

from logging import getLogger, StreamHandler, DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

from typing import List

from Connection import Connection
from ArUserManager import ArUserManager
from ArUser import ArUser
from ArTimelineFavoriter import ArTimelineFavoriter

class ActiveRabbit:

    @classmethod
    def do(cls):
        Connection.open()

        userManager: ArUserManager = ArUserManager()
        users: List[ArUser] = userManager.getUsers()

        for user in users:
            password: str = user.getPassword()
            ArTimelineFavoriter.do(user, password)

        Connection.close()

if __name__ == '__main__':
    ActiveRabbit.do()