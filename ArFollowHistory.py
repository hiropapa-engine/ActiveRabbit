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

from datetime import date

from mysql.connector.cursor import MySQLCursorDict

from ArUser import ArUser
from ArConnection import ArConnection

class ArFollowHistory:
    @classmethod
    def create(cls, user: ArUser, friends_name: str, from_target: str):
        cur: MySQLCursorDict = ArConnection.cursor()
        query: str = "insert into follow_history (owner_id, follow_at, friends_name, from_target) values({owner_id}, CURRENT_TIMESTAMP(), '{friends_name}', '{from_target}')"
        query = query.format(owner_id = user.id, friends_name = friends_name, from_target = from_target)
        cur.execute(query)