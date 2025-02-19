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

from Instagram.ChromeDriver.Token import Token
from Instagram.ChromeDriver.Login import Login

from ArUser import ArUser

class ArLogin:
    @classmethod
    def do(cls, user: ArUser, password: str):
        # ログイン
        token: Token = Token(user.name, user.session_id)
        Login().doLogin(token, password)
        user.token = token
        user.session_id = token.session_id
        user.saveSession()
