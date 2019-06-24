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

from mysql import connector
from mysql.connector import MySQLConnection
from mysql.connector.cursor import MySQLCursorDict

class Connection:
    conn: MySQLConnection = None

    @classmethod
    def open(cls):
        cls.conn = connector.connect(user='ActiveRabbit', password='%GEt25v2=PpTbiz?dfx*+!lnM.g2F1', host='localhost', database='ActiveRabbit', buffered=True)
        cls.conn.autocommit = True

    @classmethod
    def cursor(cls) -> MySQLCursorDict:
        return cls.conn.cursor(dictionary = True)

    @classmethod
    def close(cls):
        cls.conn.close
