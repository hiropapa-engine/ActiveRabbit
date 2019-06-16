from __future__ import annotations

from typing import List

from mysql import connector
from mysql.connector import MySQLConnection
from mysql.connector.cursor import MySQLCursorDict
from datetime import date

from User import User

class UserManager:
    def __init__(self : UserManager):
        pass

    def getUsers(self : UserManager) -> List[User]:   # type: List[User]
        users : List[User] = []
        cur : MySQLCursorDict = self.connection.cursor(dictionary = True)
        cur.execute("select * from users;")

        for row in cur.fetchall():
            user : User = User(
                self.connection,
                self.instagram,
                row['id'],
                row['name'],
                row['password'],
                date.strftime(row['start_date'], '%Y-%m-%d')
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