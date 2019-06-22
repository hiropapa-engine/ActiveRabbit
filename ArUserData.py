from __future__ import annotations

from datetime import date

class ArUserData:
    def __init__(self, id: int, name: str, start_date: date, slow_start_enabled: bool):
        self.id: int = id
        self.name: str = name
        self.start_date: date = start_date
        self.slow_start_enabled = slow_start_enabled