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
import datetime

from mysql.connector.cursor import MySQLCursorDict

from Instagram.ChromeDriver.User import User

from ArConnection import ArConnection
from ArUserRestriction import ArUserRestriction

class ArUser:
    def __init__(self, id: int, name: str, start_date: date, session_id: str):
        self.id: int = id
        self.name: str = name
        self.start_date: date = start_date
        self.session_id = session_id
        self.token = None
        self.restriction = None

    def getPassword(self) -> str:
        cur: MySQLCursorDict = ArConnection.cursor()
        query: str = "select * from users where id={0}".format(self.id)
        cur.execute(query)
        return cur.fetchone()['password']

    def saveSession(self):
        cur: MySQLCursorDict = ArConnection.cursor()
        query: str = "update users set session_id='{0}' where name='{1}'".format(self.session_id, self.name)
        cur.execute(query)
        return

    def getRestriction(self) -> ArUserRestriction:
        if self.restriction is None:
            cur: MySQLCursorDict = ArConnection.cursor()
            # 1. ユーザーのフォロー上限（プランによる機能制限）を取得する
            query: str = "select * from user_restriction where owner_id = {owner_id}"
            query = query.format(owner_id = self.id)
            cur.execute(query)
            row = cur.fetchone()
            self.restriction = ArUserRestriction(
                  row['follow_limit']
                , row['slow_start_enabled'] == 1
                , row['tracking_limit']
            )
        
        return self.restriction