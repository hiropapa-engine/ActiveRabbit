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

from typing import List
import datetime

from ArUser import ArUser
from Instagram.ChromeDriver.Token import Token
from Instagram.ChromeDriver.User import User
from Instagram.ChromeDriver.Post import Post
from Instagram.ChromeDriver.Favorites import Favorites
from Instagram.ChromeDriver.OtherUser import OtherUser

class ArFollowTask:

    def __init__(self, user: ArUser, executeTiming: datetime, target: str, followNum: int):
        self.user = user
        self.executeTiming = executeTiming
        self.target = target
        self.followNum = followNum

    def do(self):
        # ユーザーからトークンを取得
        token: Token = self.user.token

        # スティール対象ユーザのトップページを表示
        target: User = User(self.target)
        target.show(token)

        # スティール対象ユーザの最新投稿を取得
        post: Post = target.showRecentPost(token)

        # 良いね一覧を表示
        favorites: Favorites = post.showFavorites(token)

        # 良いねしているユーザー名のリストを取得
        otherUsers: List[OtherUser] = favorites.getUsers(token)

        # フォローしていないユーザをフォローターゲットに追加
        followTarget: List[str] = []
        followTarget.extend([user.name for user in otherUsers if user.followed == False])

        # 良いね一覧を閉じる
        favorites.close(token)

        # フォロー対象数に達するまで
        while len(followTarget) < self.followNum:
            # 次投稿を取得
            post = post.next(token)
            # 良いねしているユーザを取得
            favorites = post.showFavorites(token)
            # 良いねしているユーザー名のリストを取得
            otherUsers = favorites.getUsers(token)
            # フォローしていないユーザを取得
            notFollowed = [user.name for user in otherUsers if user.followed == False]
            # Setを利用し、重複が無いようにユーザーを追加
            followTarget = list(set(followTarget) | set(notFollowed))
            # 良いね一覧を閉じる
            favorites.close(token)

        # 投稿を閉じる
        post.close(token)

        # フォロー対象人数分ループ処理でフォローを実行
        for i in range(0, self.followNum):
            # ユーザーページを開く
            user: User = User(followTarget[i])
            user.show(token)
            # 最新投稿にいいね
            post = user.showRecentPost(token)
            '''
            if not post.isFavorited(token):
                post.favorite(token)
            '''
            post.close(token)
            # フォロー
            '''
            user.follow(token)
            '''
