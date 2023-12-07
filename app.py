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

Base = declarative_base()
engine = create_engine('sqlite:///hukusyu.db')
Session = sessionmaker(bind=engine)
session = Session()


class Database(Base):
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
        query_offset = session.query(Database).offset(offset_number).first()
        query_offset_loads = json.loads(query_offset.data)
        # データベーステーブルから取得した復元済みのデータ
        return query_offset_loads
    
    # データの更新。append_or_deleteはデータを追加または削除し終えたあとに代入する変数。
    def update(self, append_or_delete):
        query_offset.data = json.dumps(append_or_delete)
        session.commit()

    def update_schedule(self, date, new_schedule):
        query_1 = db_instance.query(1)
        query_1[date] = new_schedule
        db_instance.update(query_1)

Base.metadata.create_all(engine)

db_instance = Database()

# 🌟復習の間隔(日)の情報を入れるリスト。データベーステーブルの1行目に追加。
db_instance.default([])
# 🌟🌟日付をキー、「予定」の欄で入力された文字を値として保存する辞書。データベーステーブルの2行目に追加。
db_instance.default({})

class Page:
    # 予定の追加
    def schdule_append(self):
        st.header("予定の追加")
        with st.form("save_data"):
            calender = st.date_input("予定を追加する日付", date(year, month, day))
            schedule = st.text_input("予定")

            st.write("復習の間隔(日)を以下の「＋」から設定してください")

            #「＋」のボタンよりも数字を入力する欄のほうがUI上の画面の上に表示されるようにするために「st_input_area」→「st_add_button_area」という
            #順番にしている
            st_input_area = st.container()
            st_add_button_area = st.container()

            #数字を入力する欄を追加
            if st_add_button_area.form_submit_button("＋"):
                query_0 = db_instance.query(0)
                query_0.append("")
                db_instance.update(query_0)
            #数字を入力する欄を一つ削除
            if st_add_button_area.form_submit_button("ー"):
                query_0 = db_instance.query(0)
                if len(query_0) > 0:
                    del query_0[-1]
                    db_instance.update(query_0)
            
            query_0 = db_instance.query(0)
            for i in range(len(query_0)):
                query_0 = db_instance.query(0)
                # listキーの値であるリストに格納された""をnumber_inputウイジェットで選択した数字に置き換える
                query_0[i] = st_input_area.number_input(f"{i}回目の復習日からの間隔", 0)
                db_instance.update(query_0)

            submit_bt = st.form_submit_button("予定を追加")

            if submit_bt:
                if schedule:
                    # 復習の間隔(日)を「＋」から設定しているとき
                    if query_0:
                        query_0 = db_instance.query(0)
                        for add_remove in query_0:
                            # 「予定を追加する日付」で選択した日付に「復習の間隔(日)」で入力した数字を足している。「calender」という同じ変数を使っていることに
                            #よって前回の復習日からの復習の間隔を設定することを実現している
                            calender = calender + timedelta(days=add_remove)
                            calender_str = str(calender)
                            query_1 = db_instance.query(1)
                            if calender_str in query_1:
                                # キーが既に存在する場合は、値をリストに追加
                                query_1[calender_str].append(schedule)
                            else:
                                # キーが存在しない場合は、新しいリストを作成して値を格納
                                query_1[calender_str] = [schedule]
                            db_instance.update(query_1)
                        success_add = st.success("追加しました")
                        # 成功メッセージを3秒間表示
                        time.sleep(3)
                        # st.success()のメッセージが削除される
                        success_add.empty()
                    # 復習の間隔(日)を「＋」から設定していないとき
                    else:
                        war_schedule = st.warning("復習の間隔(日)を上記の「＋」から設定してください")
                        # 失敗メッセージを5秒間表示
                        time.sleep(5)
                        # st.warning()のメッセージが削除される
                        war_schedule.empty()                        
                # 「予定」の欄が空の場合
                else:
                    war_schedule = st.warning("「予定」の欄を記入してください")
                    # 失敗メッセージを5秒間表示
                    time.sleep(5)
                    # st.warning()のメッセージが削除される
                    war_schedule.empty()

                
    # 予定の削除
    def schdule_del(self):
        st.header("予定の削除")

        with st.form("delete_multi"):
            calender_delete = st.date_input("選択した日付以降の予定をすべて削除", date(year, month, day))
            delete_date = st.form_submit_button("予定を削除")

            if delete_date:
                query_1 = db_instance.query(1)
                # 削除対象の日付リストを生成
                to_delete = [date_str for date_str in query_1 if datetime.strptime(date_str, '%Y-%m-%d').date() >= calender_delete]

                # 削除対象の日付を削除
                for date_delete in to_delete:
                    del query_1[date_delete]

                # データベースを更新
                db_instance.update(query_1)

                success_delete = st.success("削除しました")
                time.sleep(3)
                success_delete.empty()

        with st.form("delete_all"):
            delete_date = st.form_submit_button("予定をすべて削除")

            if delete_date:
                # "shared_data"には予定を追加する日付と予定の情報が格納されているが、これらの情報が格納されていない状態で「予定を削除」ボタン
                #が押されたときにエラーになってしまうので、それを防ぐためにtry-except文を使用する
                try:
                    query_1 = db_instance.query(1)
                    # shared_dataキーと値のペアをすべて削除
                    query_1.clear()
                    db_instance.update(query_1)
                    success_delete = st.success("削除しました")
                    # 成功メッセージを3秒間表示
                    time.sleep(3)
                    # st.success()のメッセージが削除される
                    success_delete.empty()
                except:
                    success_delete = st.success("削除しました")
                    # 成功メッセージを3秒間表示
                    time.sleep(3)
                    # st.success()のメッセージが削除される
                    success_delete.empty()      

    # 日付と予定のペアを表示する
    def ca(self):
        st.header("カレンダー")

        query_1 = db_instance.query(1)
        if query_1:
            tuple_query_1 = query_1.items()
            # カレンダーのページの上から順に日付が表示されるように昇順に並び替え
            query_1_up = sorted(tuple_query_1)
            for day_one, schedule_one in query_1_up:
                # schedule_oneというリストの中の要素を , (コンマと半角スペース)の部分で結合することで[]がはずれる 
                schedule_one_plus = ", ".join(schedule_one)
                # 編集された予定を取得
                edited_schedule = st.text_input(f"{day_one}", f"{schedule_one_plus}")
                if st.button(f"予定を更新 {day_one}"):
                    # データベーステーブルから取得したデータを上記の ", ".join(schedule_one) によってリストをはずす処理を行うので、このコードでは
                    #データベーステーブルに保存する前にリスト型にしている。
                    new_schedule_list = edited_schedule.split(", ")
                    # データベースを更新
                    db_instance.update_schedule(day_one, new_schedule_list)
                    success_delete = st.success(f"{day_one} の予定を更新しました。")
                    # 成功メッセージを3秒間表示
                    time.sleep(3)
                    # st.success()のメッセージが削除される
                    success_delete.empty()      
                if st.button(f"予定を削除 {day_one}"):
                    st.session_state["deleted"] = True  # セッション状態にフラグを設定
                    day_one_str = str(day_one)
                    query_1 = db_instance.query(1)
                    if day_one_str in query_1:
                        del query_1[day_one_str]
                        db_instance.update(query_1)
                        success_delete = st.success("削除しました")
                        # 成功メッセージを3秒間表示
                        time.sleep(3)
                        # st.success()のメッセージが削除される
                        success_delete.empty()      

        # もし削除ボタンが押されたら、ページを再読み込み
        if "deleted" in st.session_state and st.session_state["deleted"]:
            st.session_state["deleted"] = False  # フラグをリセット
            st.experimental_rerun()


page_multi = Page()


class Notpage:

    # UIの設定
    def set_ui(self):
        # UI上の画面上部に表示されるタイトル
        st.set_page_config(page_title="復習ノート", page_icon="📚")


    # サイドバーで行われる処理
    def sidebar(self):
        # ラジオボタンで選択したボタンに対応するメソッドを値として設定
        pages = {
            "カレンダー": page_multi.ca,
            "予定の追加": page_multi.schdule_append,
            "予定の削除": page_multi.schdule_del
        }
        # サイドバー上に「予定を入力」と「カレンダー」を選択できるラジオボタンを配置
        selected_page = st.sidebar.radio("【ページの選択】", list(pages.keys()))
        # pages辞書のキー(ラジオボタンで選択したキー)に対応する値をメソッドとして実行
        pages[selected_page]()

# クラスとメソッドの定義の後に、以下の行を追加
if __name__ == "__main__":
    not_page = Notpage()
    not_page.set_ui()
    not_page.sidebar()