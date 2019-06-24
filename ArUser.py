from __future__ import annotations

from logging import getLogger, StreamHandler, DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

from datetime import date
import datetime

from Connection import Connection

class ArUser:
    def __init__(self, id: int, name: str, start_date: date, slow_start_enabled: bool, session_id: str):
        self.id: int = id
        self.name: str = name
        self.start_date: date = start_date
        self.slow_start_enabled = slow_start_enabled
        self.session_id = session_id

    def getPassword(self) -> str:
        cur = Connection.cursor()
        query: str = "select * from users where id={0}".format(self.id)
        cur.execute(query)
        return cur.fetchone()['password']

    def saveSession(self):
        cur = Connection.cursor()
        query: str = "update users set session_id='{0}' where name='{1}'".format(self.session_id, self.name)
        cur.execute(query)
        return