from UserData import UserData
import datetime

from logging import getLogger, StreamHandler, DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

class SlowStart:
    @classmethod
    def get_magnification(cls, user_data: UserData) -> float:
        if not user_data.slow_start_enabled:
            return 1.0
        
        now: datetime.datetime = datetime.datetime.now()
        now = datetime.datetime(now.year, now.month, now.day)
        stdt = datetime.datetime(user_data.start_date.year, user_data.start_date.month, user_data.start_date.day)

        days = (now-stdt).days
        if days >= 5:
            return 1.0

        magnification = [0.1, 0.2, 0.3, 0.4, 0.5]
        return magnification[days]