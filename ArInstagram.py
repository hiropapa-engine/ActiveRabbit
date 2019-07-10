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

from ArConnection import ArConnection

class ArInstagram:
    @classmethod
    def getFollowLimitPerDay(cls):
        cur = ArConnection.cursor()
        query = "select * from instagram_restriction where property_name = 'follow_limit_per_day'"
        cur.execute(query)
        row = cur.fetchone()
        insta_follow_limit: int = row['value']
        return insta_follow_limit
