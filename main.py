import streamlit as st
from datetime import datetime, timedelta, date
import time
import message as me
import timezone as ti
import database as da
import encryptdecrypt as en_de

class Page:
    def schdule_today(self):
        if 'uuid_generate' not in st.session_state:
            pass
        else:
            st.info("ゲストログインを次回も行う可能性がある場合は以下のユーザーIDをコピーして保存しておいてください。")
            st.write("ユーザーID👇")
            st.code(st.session_state["uuid_generate"])
            st.write()
            st.info("ユーザーIDは再設定できないので、大切なデータをこのアプリに保存する場合はホーム画面の「サインイン」からアプリにアクセスしてください。")

        st.title("今日やること")
        query_1 = da.database.query(st.session_state["generate_key"], 1)
        if query_1:
            tuple_query_1 = query_1.items()
            # カレンダーのページの上から順に日付が表示されるように昇順に並び替え
            query_1_up = sorted(tuple_query_1)
            # 今日の日付を文字列型に変換
            today_str = str(date(ti.world_timezone.year, ti.world_timezone.month, ti.world_timezone.day))
            # 日付と予定をそれぞれ取り出す
            for day_one, schedule_one in query_1_up:
                if today_str >= day_one:
                    multi_shedule = ""
                    multi_shedule_one = ", "
                    # その日付の予定を一つずつ取り出す
                    for sc_on in schedule_one:
                        decrypted_schedule_one = en_de.encrypt_decrypt.decrypt_message(sc_on.encode('utf-8'), st.session_state["generate_key"])
                        # 1つの日付に予定が1つだけのとき
                        if multi_shedule == "":
                            multi_shedule = multi_shedule + decrypted_schedule_one
                        else:
                            multi_shedule = multi_shedule + multi_shedule_one + decrypted_schedule_one
                    # multi_sheduleの部分だけedited_schedule変数に代入
                    edited_schedule = st.text_input(f"{day_one}", f"{multi_shedule}")
                    col1, col2, col3 = st.columns([1,4,1])

                    with col2:
                        # 中央の列内でさらに2つの列を作成
                        button_col1, button_col2 = st.columns(2)

                        with button_col1:
                            if st.button(f"⭕予定を更新 {day_one}"):
                                with st.info("保存中... 🔄"):
                                    encrypted_edited_schedule = en_de.encrypt_decrypt.encrypt_message(edited_schedule, st.session_state["generate_key"])
                                    decode_edited_schedule = encrypted_edited_schedule.decode('utf-8')
                                    # データベーステーブルに保存する前にリスト型に変換
                                    encrypted_new_schedule_list = decode_edited_schedule.split(", ")
                                    query_1 = da.database.query(st.session_state["generate_key"], 1)
                                    # 編集したあとの予定を日付に紐づける
                                    query_1[day_one] = encrypted_new_schedule_list
                                    da.database.update(query_1)
                                    time.sleep(1)
                                    st.rerun()

                        with button_col2:
                            if st.button(f"❌予定を削除 {day_one}"):
                                day_one_str = str(day_one)
                                query_1 = da.database.query(st.session_state["generate_key"], 1)
                                if day_one_str in query_1:
                                    del query_1[day_one_str]
                                    da.database.update(query_1)
                                    me.message.success("削除しました", 3)
                                st.rerun()


    def schdule_append(self):
        st.title("予定の追加")

        calender = st.date_input("予定を追加する日付", date(ti.world_timezone.year, ti.world_timezone.month, ti.world_timezone.day))
        schedule = st.text_input("予定")
        encrypted_schedule = en_de.encrypt_decrypt.encrypt_message(schedule, st.session_state["generate_key"])

        # メッセージ用の表示エリア
        st_message_area = st.container()
        # メッセージ用の表示エリアをさらに上書き可能なエリアにする
        message_placeholder = st_message_area.empty()

        group_day_interval = ""
        query_0 = da.database.query(st.session_state["generate_key"], 0)
        decrypted_group_text_dict = {}
        selectbox_group_text_key_list = []
        for group_text, group_text_day in query_0.items():
            decrypted_group_text = en_de.encrypt_decrypt.decrypt_message(group_text.encode('utf-8'), st.session_state["generate_key"])
            decrypted_group_text_dict[decrypted_group_text] = group_text_day
            selectbox_group_text_key_list.append(decrypted_group_text)
        selectbox_group_name = st.selectbox("復習する日数間隔のグループを選択してください", selectbox_group_text_key_list)
        study_count = 0
        group_day_interval = ""
        try:
            for di in decrypted_group_text_dict[selectbox_group_name]:
                group_day_interval += f"{study_count}回目の復習日からの間隔：{di}日　"
                study_count += 1
            st.write(group_day_interval)
            st.write()
        except KeyError:
            st.warning("まずは左側のサイドバーの「復習する日数間隔のグループ」からグループを作成してください")

        if st.button("予定を追加"):
            if schedule:
                try:
                    for pear_add in decrypted_group_text_dict[selectbox_group_name]:
                        # 「予定を追加する日付」で選択した日付に「復習する日数間隔のグループ」で選択された復習間隔を足している
                        calender = calender + timedelta(days=pear_add)
                        calender_str = str(calender)
                        query_1 = da.database.query(st.session_state["generate_key"], 1)
                        if calender_str in query_1:
                            # 追加する日付が既にカレンダーのページに存在する場合は、予定をその日付に追加
                            query_1[calender_str].append(encrypted_schedule.decode('utf-8'))
                        else:
                            # 追加する日付がカレンダーのページに存在しない場合は、追加する日付と予定のペアを作成
                            query_1[calender_str] = [encrypted_schedule.decode('utf-8')]
                        da.database.update(query_1)
                    me.placeholder.success("追加しました", message_placeholder, 3)
                except:
                    me.placeholder.error("まずは左側のサイドバーの「復習する日数間隔のグループ」からグループを作成してください", message_placeholder, 10)                  
            else:
                me.placeholder.error("「予定」を記入してください", message_placeholder, 5)


    def day_interval(self):
        st.title("復習する日数間隔のグループ")

        with st.form("save_data"):
            group_name = st.text_input("このグループに一意の名前をつけてください")
            st.write("復習する日数間隔を以下の「＋」から設定してください")

            if 'day_interval' not in st.session_state:
                st.session_state['day_interval'] = []

            # 復習日間隔の日数入力欄の表示エリア
            st_input_area = st.container()
            # メッセージ用の表示エリア
            st_message_area = st.container()
            # 「＋」ボタンと「ー」ボタン用の表示エリア
            st_add_button_area = st.container()

            # メッセージ用の表示エリアをさらに上書き可能なエリアにする
            message_placeholder = st_message_area.empty()

            if st_add_button_area.form_submit_button("＋"):
                st.session_state['day_interval'].append("")

            if st_add_button_area.form_submit_button("ー"):
                if len(st.session_state['day_interval']) > 0:
                    del st.session_state['day_interval'][-1]

            for i in range(len(st.session_state['day_interval'])):
                # st.session_state['day_interval']の中にある""の数だけnumber_inputウイジェットが実行されるので数字を入力する欄の数を調整できる。そして、その""をnumber_inputウイジェットで選択した数字に置き換えている
                st.session_state['day_interval'][i] = st_input_area.number_input(f"{i}回目の復習日からの間隔", 0)

            if st.form_submit_button("決定"):
                if group_name:
                    query_0 = da.database.query(st.session_state["generate_key"], 0)
                    decrypted_past_group_name_list = []
                    for past_group_name in query_0:
                        decrypted_past_group_name_list.append(en_de.encrypt_decrypt.decrypt_message(past_group_name.encode('utf-8'), st.session_state["generate_key"]))
                    # 記入したグループ名が過去に登録されたものではなかったとき
                    if not group_name in decrypted_past_group_name_list:
                        # 復習の間隔(日)の数字を記入済みであるとき
                        if not st.session_state['day_interval'] == []:
                            encrypt_group_name = en_de.encrypt_decrypt.encrypt_message(group_name, st.session_state["generate_key"])
                            decode_group_name = encrypt_group_name.decode('utf-8')
                            query_0[decode_group_name] = [day for day in st.session_state['day_interval']]
                            da.database.update(query_0)
                            del st.session_state['day_interval']
                            me.placeholder.success("追加しました", message_placeholder, 3)
                            st.rerun()
                        else:
                            me.placeholder.error("復習の間隔(日)を以下の「＋」から設定してください", message_placeholder, 5)
                    else:
                        me.placeholder.error("記入したグループ名は既に存在します。違うグループ名をつけてください", message_placeholder, 5)
                else:
                    me.placeholder.error("グループ名が記入されていません", message_placeholder, 5)

        with st.form("group_write"):
            group_day_interval = ""
            query_0 = da.database.query(st.session_state["generate_key"], 0)
            decrypted_group_text_dict = {}
            for group_text, group_text_day in query_0.items():
                decrypted_group_text = en_de.encrypt_decrypt.decrypt_message(group_text.encode('utf-8'), st.session_state["generate_key"])
                decrypted_group_text_dict[decrypted_group_text] = group_text_day
            for decrypted_group_text_key in decrypted_group_text_dict:
                study_count = 0
                group_day_interval = ""
                for di in decrypted_group_text_dict[decrypted_group_text_key]:
                    group_day_interval += f"{study_count}回目の復習日からの間隔：{di}日　"
                    study_count += 1
                st.write()
                st.subheader(decrypted_group_text_key)
                st.write(group_day_interval)

                if st.form_submit_button(f"{decrypted_group_text_key}　削除"):
                    del decrypted_group_text_dict[decrypted_group_text_key]
                    encrypted_group_text_dict = {}
                    for decrypted_group_text_key_update, decrypted_group_text_value_update in decrypted_group_text_dict.items():
                        encrypt_group_text_key = en_de.encrypt_decrypt.encrypt_message(decrypted_group_text_key_update, st.session_state["generate_key"])
                        encrypted_group_text_dict[encrypt_group_text_key.decode('utf-8')] = decrypted_group_text_value_update
                    query_0 = da.database.query(st.session_state["generate_key"], 0)
                    query_0 = encrypted_group_text_dict
                    da.database.update(query_0)
                    me.message.success("削除しました", 3)
                    st.rerun()


    def schdule_del(self):
        st.title("予定の削除")

        with st.form("delete_multi"):
            calender_delete = st.date_input("選択した日付以降の予定をすべて削除", date(ti.world_timezone.year, ti.world_timezone.month, ti.world_timezone.day))

            if st.form_submit_button("予定を削除"):
                query_1 = da.database.query(st.session_state["generate_key"], 1)
                # 削除対象の日付リストを生成
                to_delete = [date_str for date_str in query_1 if datetime.strptime(date_str, '%Y-%m-%d').date() >= calender_delete]
                for date_delete in to_delete:
                    # 削除対象の日付を削除
                    del query_1[date_delete]
                da.database.update(query_1)
                me.message.success("削除しました", 3)

        with st.form("delete_all"):
            st.write("カレンダーのページの予定をすべて削除")
            if st.form_submit_button("予定をすべて削除"):
                query_1 = da.database.query(st.session_state["generate_key"], 1)
                query_1.clear()
                da.database.update(query_1)
                me.message.success("削除しました", 3)


    def ca(self):
        st.title("カレンダー")
        query_1 = da.database.query(st.session_state["generate_key"], 1)
        if query_1:
            tuple_query_1 = query_1.items()
            # カレンダーのページの上から順に日付が表示されるように昇順に並び替え
            query_1_up = sorted(tuple_query_1)
            for day_one, schedule_one in query_1_up:
                multi_shedule = ""
                multi_shedule_one = ", "
                for sc_on in schedule_one:
                    decrypted_schedule_one = en_de.encrypt_decrypt.decrypt_message(sc_on.encode('utf-8'), st.session_state["generate_key"])
                    # 1つの日付に予定が1つだけのとき
                    if multi_shedule == "":
                        multi_shedule = multi_shedule + decrypted_schedule_one
                    else:
                        multi_shedule = multi_shedule + multi_shedule_one + decrypted_schedule_one
                # multi_sheduleの部分だけ変数に代入
                edited_schedule = st.text_input(f"{day_one}", f"{multi_shedule}")
                
                encrypt_edited_schedule = en_de.encrypt_decrypt.encrypt_message(edited_schedule, st.session_state["generate_key"])
                decode_edited_schedule = encrypt_edited_schedule.decode('utf-8')
                col1, col2, col3 = st.columns([1,4,1])

                with col2:
                    # 中央の列内でさらに2つの列を作成
                    button_col1, button_col2 = st.columns(2)
                
                with button_col1:
                    if st.button(f"⭕予定を更新 {day_one}"):
                        with st.info("保存中... 🔄"):
                            # データベーステーブルに保存する前にリスト型に変換
                            new_schedule_list = decode_edited_schedule.split(", ")
                            query_1 = da.database.query(st.session_state["generate_key"], 1)
                            # 編集したあとの予定を日付に紐づける
                            query_1[day_one] = new_schedule_list
                            da.database.update(query_1)
                            time.sleep(1)
                            st.rerun()

                with button_col2:
                    if st.button(f"❌予定を削除 {day_one}"):
                        day_one_str = str(day_one)
                        query_1 = da.database.query(st.session_state["generate_key"], 1)
                        if day_one_str in query_1:
                            del query_1[day_one_str]
                            da.database.update(query_1)
                            me.message.success("削除しました", 3)
                        st.rerun()                    

page_multi = Page()