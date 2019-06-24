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