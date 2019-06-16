from __future__ import annotations
from mysql import connector
from typing import Dict

from Instagram import Instagram


class ActiveRabbit:

    conn: connector = None
    instagrams: Dict[str, Instagram] = []

    @classmethod
    def processSchedulingTask(cls):
        pass

    @classmethod
    def processFollowingTask(cls):
        pass

    @classmethod
    def do(cls):
        # コネクションオープン
        cls.conn = connector.connect(user='ActiveRabbit', password='%GEt25v2=PpTbiz?dfx*+!lnM.g2F1', host='localhost', database='ActiveRabbit')

        ''' スケジューリングタスク処理 '''
        # スケジューリングタスク生成(タスクを生成したら、対象データは削除)
        # タスクスケジューラー起動
        # 翌日のスケジューリングタスクデータ生成

        ''' フォロータスク処理 '''
        # フォロータスク生成(タスクを生成したら、対象データは削除)
        # フォロータスク実行

        ''' フォロー解除タスク処理 '''
        # フォロー解除タスク生成(タスクを生成したら、対象データは削除)
        # フォロー解除タスク実行

        ''' フォロー解除タスク処理 '''
        # フォロバタスク生成(フォロバは常時監視のため、対象データを削除しない)
        # フォロバタスク実行

        ''' 良いねタスク処理 '''
        # 良いねタスク生成(良いねは常時監視のため、対象データを削除しない)
        # 良いねタスク実行

        # コネクションクローズ
        cls.conn.close

    @classmethod
    def getInstagram(cls, name: str) -> Instagram:
        if not name in cls.instagrams:
            insta: Instagram = Instagram()
            cls.instagrams[name] = insta
        return cls.instagrams[name]

if __name__ == '__main__':
    ActiveRabbit.do()