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

from ArUserData import ArUserData
from Connection import Connection

class ArUser:
    def __init__(self, userData: ArUserData):
        self.userData = userData

    def getPassword(self) -> str:
        cur = Connection.cursor()
        query: str = "select * from users where id={0}".format(self.userData.id)
        cur.execute(query)
        return cur.fetchone()['password']