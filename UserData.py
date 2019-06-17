from __future__ import annotations
from datetime import date

class UserData:
    def __init__(self, id: int, name: str, password: str, start_date: date):
        self.id: int = id
        self.name: str = name
        self.password: str = password
        self.start_date: date = start_date
