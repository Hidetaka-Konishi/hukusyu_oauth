import json
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# クラス内でデータベースを扱えるように定義
Base = declarative_base()
engine = create_engine('sqlite:///login_signin.db')
# データベースセッションを作成する準備
Session = sessionmaker(bind=engine)
# データベースセッションをインスタンス化してデータベースとの接続を開始するためのもの
session = Session()

# データベースの操作を行うクラス
class Database(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    # ユーザーのメールアドレス
    email = Column(String)
    # その他のユーザーデータ
    data = Column(String)

    # 一番初めに保存するデータ。list_or_dictには[]または{}のどちらかを記述する。
    def default(self, email, list_or_dict):
        list_or_dict_dumps = json.dumps(list_or_dict)            
        list_or_dict_entry = Database(email=email, data=list_or_dict_dumps)
        session.add(list_or_dict_entry)
        session.commit()


    # データベーステーブルからデータを取り出す。offset_numberには取得したいデータベーステーブルの行数から1引いた数字を指定する。
    def query(self, email, offset_number):
        # データベーステーブルから取得した復元されていないデータ
        global query_offset
        # 取得したいデータベーステーブルの行を一行だけ取得
        query_offset = session.query(Database).filter_by(email=email).offset(offset_number).first()
        query_offset_loads = json.loads(query_offset.data)
        # データベーステーブルから取得した復元済みのデータ
        return query_offset_loads


    # データベーステーブルを更新。append_or_deleteはデータを追加または削除し終えたあとに代入する変数。
    def update(self, append_or_delete):
        query_offset.data = json.dumps(append_or_delete)
        session.commit()

# データベーステーブルを作成
Base.metadata.create_all(engine)

database = Database()