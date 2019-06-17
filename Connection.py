from __future__ import annotations

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
