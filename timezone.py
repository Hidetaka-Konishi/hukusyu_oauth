from datetime import datetime, timedelta, timezone

class WorldTimezone:
    year = ""
    month = ""    
    day = ""

    def japan_timezone(self):
        # 日本のタイムゾーンを定義
        JST = timezone(timedelta(hours=9))
        # 現在のUTC時間を取得し、日本のタイムゾーンに変換
        now = datetime.now(timezone.utc).astimezone(JST)

        self.year = now.year
        self.month = now.month
        self.day = now.day

world_timezone = WorldTimezone()

# 他のファイルでクラス変数を使用するためにメソッドをあらかじめ実行
world_timezone.japan_timezone()