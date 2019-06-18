from __future__ import annotations

from typing import List

from mysql.connector.cursor import MySQLCursorDict
from datetime import date

from User import User
from Connection import Connection
from UserData import UserData

from logging import getLogger, StreamHandler, DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

class UserManager:

    def __init__(self):
        pass

    def users(self) -> List[User]:   # type: List[User]
        users : List[User] = []
        cur : MySQLCursorDict = Connection.cursor()
        cur.execute("select * from users where enabled=1;")

        for row in cur.fetchall():
            logger.debug("次のユーザーが見つかりました: id = {id}, name = {name}".format(id=row['id'], name=row['name']))
            start_date = row['start_date']
            user : User = User(
                UserData(
                    row['id'],
                    row['name'],
                    row['password'],
                    date(start_date.year, start_date.month, start_date.day),
                    row['slow_start_enabled'] == 1
                )
            )
            users.append(user)

        cur.close

        return users
'''
if __name__ == "__main__":
    conn = connector.connect(user='ActiveRabbit', password='%GEt25v2=PpTbiz?dfx*+!lnM.g2F1', host='localhost', database='ActiveRabbit')
    insta : Instagram = Instagram
    userManager = UserManager(conn, insta)
    users: List[User] = userManager.getUsers()
    for user in users:
        user.dump()
'''