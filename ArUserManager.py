from __future__ import annotations

from logging import getLogger, StreamHandler, DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

from typing import List
from datetime import date

from mysql.connector.cursor import MySQLCursorDict

from Connection import Connection
from ArUser import ArUser

class ArUserManager:

    def __init__(self):
        pass

    def getUsers(self) -> List[ArUser]:   # type: List[User]
        users : List[ArUser] = []
        cur : MySQLCursorDict = Connection.cursor()
        cur.execute("select * from users where enabled=1;")

        for row in cur.fetchall():
            logger.debug("次のユーザーが見つかりました: id = {id}, name = {name}".format(id=row['id'], name=row['name']))
            start_date = row['start_date']
            user : ArUser = ArUser(
                row['id'],
                row['name'],
                date(start_date.year, start_date.month, start_date.day),
                row['slow_start_enabled'] == 1,
                row['session_id']
            )
            users.append(user)

        cur.close

        return users
