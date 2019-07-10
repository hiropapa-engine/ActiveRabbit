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

class ArUserRestriction:
    def __init__(self, follow_limit: int, slow_start_enabled: bool, tracking_limit: int):
        self.follow_limit = follow_limit
        self.slow_start_enabled = slow_start_enabled
        self.tracking_limit = tracking_limit