import json
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import streamlit as st
import time
from datetime import datetime, timedelta, timezone, date

# 日本のタイムゾーンを定義
JST = timezone(timedelta(hours=9))

# 現在のUTC時間を取得し、日本のタイムゾーンに変換
now = datetime.now(timezone.utc).astimezone(JST)

year = now.year
month = now.month
day = now.day

# クラス内でデータベースを扱えるように定義
Base = declarative_base()
engine = create_engine('sqlite:///hukusyu.db')
# データベースセッションを作成する準備
Session = sessionmaker(bind=engine)
# データベースセッションをインスタンス化してデータベースとの接続を開始するためのもの
session = Session()


# データベースの操作を行うクラス
class Database(Base):
    # データベーステーブルの名前を設定
    __tablename__ = 'hukusyu'
    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(String)

    # 一番初めに保存するデータ。list_or_dictには[]または{}のどちらかを記述する。
    def default(self, list_or_dict):
        list_or_dict_dumps = json.dumps(list_or_dict)            
        list_or_dict_entry = Database(data=list_or_dict_dumps)
        session.add(list_or_dict_entry)
        session.commit()
    
    # データベーステーブルからデータを取り出す。offset_numberには取得したいデータベーステーブルの行数から1引いた数字を指定する。
    def query(self, offset_number):
        # データベーステーブルから取得した復元されていないデータ
        global query_offset
        # 取得したいデータベーステーブルの行を一行だけ取得
        query_offset = session.query(Database).offset(offset_number).first()
        query_offset_loads = json.loads(query_offset.data)
        # データベーステーブルから取得した復元済みのデータ
        return query_offset_loads
    
    # データベーステーブルを更新。append_or_deleteはデータを追加または削除し終えたあとに代入する変数。
    def update(self, append_or_delete):
        query_offset.data = json.dumps(append_or_delete)
        session.commit()

# データベーステーブルを作成
Base.metadata.create_all(engine)

db_instance = Database()

# 🌟復習の間隔(日)の情報を入れるリスト。データベーステーブルの1行目に追加。
db_instance.default([])
# 🌟🌟日付をキー、「予定」の欄で入力された文字を値として保存する辞書。データベーステーブルの2行目に追加。
db_instance.default({})

# メッセージの表示に関するクラス
class Message:
    # 成功メッセージを表示。send_messageにはダブルクォーテーションで囲んだメッセージが入る。
    def success(self, send_message):
        success_message = st.success(send_message)
        # 成功メッセージを3秒間表示
        time.sleep(3)
        # 成功メッセージが削除される
        success_message.empty()

message = Message()


# サイドバーから選択した際に表示されるページの内容に関するクラス
class Page:
    def schdule_today(self):
        st.title("今日やること")
        # データベーステーブルからデータを取得
        query_1 = db_instance.query(1)
        if query_1:
            tuple_query_1 = query_1.items()
            # カレンダーのページの上から順に日付が表示されるように昇順に並び替え
            query_1_up = sorted(tuple_query_1)
            # 今日の日付を文字列型に変換
            today_str = str(date(year, month, day))
            for day_one, schedule_one in query_1_up:
                if today_str >= day_one:
                    # schedule_oneというリストの中の要素を , (コンマと半角スペース)の部分で結合することで[]がはずれる 
                    schedule_one_plus = ", ".join(schedule_one)
                    # schedule_one_plusの部分だけedited_schedule変数に代入している
                    edited_schedule = st.text_input(f"{day_one}", f"{schedule_one_plus}")
                    if st.button(f"予定を更新 {day_one}"):
                        with st.spinner('保存中...'):
                            # データベーステーブルから取得したデータを上記の ", ".join(schedule_one) によってリストをはずす処理を行うので、このコードではデータベーステーブルに保存する前にリスト型にしている。
                            new_schedule_list = edited_schedule.split(", ")
                            # データベーステーブルからデータを取得
                            query_1 = db_instance.query(1)
                            # 編集したあとの予定を日付に紐づける
                            query_1[day_one] = new_schedule_list
                            # データベーステーブルを更新
                            db_instance.update(query_1)
                            time.sleep(1)
                            st.rerun()
                    if st.button(f"予定を削除 {day_one}"):
                        day_one_str = str(day_one)
                        # データベーステーブルからデータを取得
                        query_1 = db_instance.query(1)
                        if day_one_str in query_1:
                            del query_1[day_one_str]
                            # データベーステーブルを更新
                            db_instance.update(query_1)
                            message.success("削除しました")
                        # Webアプリを再読み込みする
                        st.rerun()                    


    def schdule_append(self):
        st.title("予定の追加")
        with st.form("save_data"):
            calender = st.date_input("予定を追加する日付", date(year, month, day))
            schedule = st.text_input("予定")

            st.write("復習の間隔(日)を以下の「＋」から設定してください")

            # 復習日間隔の日数入力欄の表示エリア
            st_input_area = st.container()
            # 成功メッセージと失敗メッセージ用の表示エリア
            st_message_area = st.container()
            # 「＋」ボタンと「ー」ボタン用の表示エリア
            st_add_button_area = st.container()

            # 成功メッセージと失敗メッセージ用の表示エリアをさらに上書き可能なエリアにする
            message_placeholder = st_message_area.empty()

            # 数字を入力する欄を追加
            if st_add_button_area.form_submit_button("＋"):
                # データベーステーブルからデータを取得
                query_0 = db_instance.query(0)
                query_0.append("")
                # データベーステーブルを更新
                db_instance.update(query_0)

            # 数字を入力する欄を一つ削除
            if st_add_button_area.form_submit_button("ー"):
                # データベーステーブルからデータを取得
                query_0 = db_instance.query(0)
                if len(query_0) > 0:
                    del query_0[-1]
                    # データベーステーブルを更新
                    db_instance.update(query_0)

            # データベーステーブルからデータを取得
            query_0 = db_instance.query(0)
            for i in range(len(query_0)):
                # query_0の中にある""の数だけnumber_inputウイジェットが実行されるので数字を入力する欄の数を調整できる。そしてquery_0に格納された""をnumber_inputウイジェットで選択した数字に置き換えている
                query_0[i] = st_input_area.number_input(f"{i}回目の復習日からの間隔", 0)
                # データベーステーブルを更新
                db_instance.update(query_0)

            if st.form_submit_button("予定を追加"):
                if schedule:
                    # 復習の間隔(日)を「＋」から設定しているとき
                    if query_0:
                        # データベーステーブルからデータを取得
                        query_0 = db_instance.query(0)
                        for add_remove in query_0:
                            # 「予定を追加する日付」で選択した日付に「復習の間隔(日)」で入力した数字を足している。「calender」という同じ変数を使っていることによって前回の復習日からの復習の間隔を設定することを実現している
                            calender = calender + timedelta(days=add_remove)
                            calender_str = str(calender)
                            # データベーステーブルからデータを取得
                            query_1 = db_instance.query(1)
                            if calender_str in query_1:
                                # 指定した日付が既にカレンダーのページに存在する場合は、予定をその日付に追加
                                query_1[calender_str].append(schedule)
                            else:
                                # 指定した日付がカレンダーのページに存在しない場合は、指定した日付と予定のペアを作成
                                query_1[calender_str] = [schedule]
                            # データベーステーブルを更新
                            db_instance.update(query_1)
                        message_placeholder.success("追加しました")
                        # 成功メッセージを3秒間表示
                        time.sleep(3)
                        # 成功メッセージが削除される
                        message_placeholder.empty()
                    else:
                        message_placeholder.warning("復習の間隔(日)を上記の「＋」から設定してください")
                        # 失敗メッセージを5秒間表示
                        time.sleep(5)
                        # 失敗メッセージが削除される
                        message_placeholder.empty()
                # 「予定」の欄が空の場合                  
                else:
                    message_placeholder.warning("「予定」の欄を記入してください")
                    # 失敗メッセージを5秒間表示
                    time.sleep(5)
                    # 失敗メッセージが削除される
                    message_placeholder.empty()


    def schdule_del(self):
        st.title("予定の削除")

        with st.form("delete_multi"):
            calender_delete = st.date_input("選択した日付以降の予定をすべて削除", date(year, month, day))

            if st.form_submit_button("予定を削除"):
                # データベーステーブルからデータを取得
                query_1 = db_instance.query(1)
                # 削除対象の日付リストを生成
                to_delete = [date_str for date_str in query_1 if datetime.strptime(date_str, '%Y-%m-%d').date() >= calender_delete]
                for date_delete in to_delete:
                    # 削除対象の日付を削除
                    del query_1[date_delete]
                # データベーステーブルを更新
                db_instance.update(query_1)
                message.success("削除しました")

        with st.form("delete_all"):
            st.write("カレンダーのページの予定をすべて削除")
            if st.form_submit_button("予定をすべて削除"):
                # データベーステーブルからデータを取得
                query_1 = db_instance.query(1)
                query_1.clear()
                # データベーステーブルを更新
                db_instance.update(query_1)
                message.success("削除しました")


    def ca(self):
        st.title("カレンダー")
        # データベーステーブルからデータを取得
        query_1 = db_instance.query(1)
        if query_1:
            tuple_query_1 = query_1.items()
            # カレンダーのページの上から順に日付が表示されるように昇順に並び替え
            query_1_up = sorted(tuple_query_1)
            for day_one, schedule_one in query_1_up:
                # schedule_oneというリストの中の要素を , (コンマと半角スペース)の部分で結合することで[]がはずれる 
                schedule_one_plus = ", ".join(schedule_one)
                # schedule_one_plusの部分だけ変数に代入している
                edited_schedule = st.text_input(f"{day_one}", f"{schedule_one_plus}")
                if st.button(f"予定を更新 {day_one}"):
                    with st.spinner('保存中...'):
                        # データベーステーブルから取得したデータを上記の ", ".join(schedule_one) によってリストをはずす処理を行うので、このコードではデータベーステーブルに保存する前にリスト型にしている。
                        new_schedule_list = edited_schedule.split(", ")
                        # データベーステーブルからデータを取得
                        query_1 = db_instance.query(1)
                        # 編集したあとの予定を日付に紐づける
                        query_1[day_one] = new_schedule_list
                        # データベーステーブルを更新
                        db_instance.update(query_1)
                        time.sleep(1)
                        st.rerun()
                if st.button(f"予定を削除 {day_one}"):
                    day_one_str = str(day_one)
                    # データベーステーブルからデータを取得
                    query_1 = db_instance.query(1)
                    if day_one_str in query_1:
                        del query_1[day_one_str]
                        # データベーステーブルを更新
                        db_instance.update(query_1)
                        message.success("削除しました")
                    # Webアプリを再読み込みする
                    st.rerun()                    

page_multi = Page()


class Notpage:
    # アプリのタイトルの設定
    def set_ui(self):
        # UI上の画面上部に表示されるタイトル
        st.set_page_config(page_title="復習ノート", page_icon="📚")


    # サイドバーで行われる処理
    def sidebar(self):
        # ラジオボタンで選択したボタンに対応するメソッドを設定
        pages = {
            "今日やること": page_multi.schdule_today,
            "予定の追加": page_multi.schdule_append,
            "予定の削除": page_multi.schdule_del,
            "カレンダー": page_multi.ca
        }
        # サイドバー上にページを選択できるラジオボタンを配置
        selected_page = st.sidebar.radio("【ページの選択】", list(pages.keys()))
        # pages辞書で選択したボタンをメソッドとして実行
        pages[selected_page]()

not_page = Notpage()


if __name__ == "__main__":
    not_page.set_ui()
    not_page.sidebar()