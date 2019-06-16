from __future__ import annotations

from mysql.connector import MySQLConnection
from Instagram import Instagram
from datetime import date

class User:
    def __init__(self, id: int, name: str, password: str, start_date: date):
        self.id: int = id
        self.name: str = name
        self.password: str = password
        self.start_date: date = start_date

'''
    def dump(self):
        print(self.id)
        print(self.name)
        print(self.password)
        print(self.start_date)
'''