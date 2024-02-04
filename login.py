import streamlit as st
import message as me
from googleapiclient.errors import HttpError
import re
import bcrypt
import database as da
import encryptdecrypt as en_de
import checkuser as ch_us
import securitycode as se_co
import mail

# {メールアドレス:{ユーザー名:パスワード}}。everybadyの1行目に追加。
da.database.default("everybady", {})
# ユーザーを識別するための暗号化キーを保存するリスト。everybadyの2行目に追加。
da.database.default("everybady", [])

class Login:
    # セッション状態を初期化する
    def init_session_state(self):
        if 'page' not in st.session_state:
            # アプリケーションに接続するとホーム画面が表示される。
            st.session_state['page'] = 'home'


    # ホームページの内容
    def home_page(self):
        col1, col2, col3 = st.columns([2,4,2])
        with col2:
            st.title("復習カレンダー")

        col4, col5, col6 = st.columns([3,5,3])
        with col5:
            # 中央の列内でさらに2つの列を作成
            button_col1, button_col2 = st.columns(2)

            with button_col1:
                if st.button("ログイン"):
                    st.session_state['page'] = 'login'
                    st.rerun()

            with button_col2:
                if st.button("初めての方"):
                    st.session_state['page'] = 'signin'
                    st.rerun()                    

        st.image('hukusyu.png', use_column_width="auto")


    def login(self):
        st.title("ログイン")

        if st.button("ホームページに戻る"):
            st.session_state['page'] = 'home'
            st.rerun()

        with st.form("login"):
            login_username = st.text_input("ユーザー名", key="login_username")
            login_password = st.text_input("パスワード", type="password", key="login_password")

            if st.form_submit_button("ログイン"):
                if login_username and login_password:
                    if " " not in login_username and "　" not in login_username:
                        if " " not in login_password and "　" not in login_password:
                            query_0 = da.database.query("everybady", 0)
                            # ユーザー名とパスワードが過去に登録されてないかチェック
                            if ch_us.check_user.username_password_check(query_0, login_username, login_password):
                                # ログイン後の処理をここに記述
                                # ユーザー名とパスワードのペアが保存されているインデックスを変数に代入
                                bo, co = ch_us.check_user.username_password_check(query_0, login_username, login_password)
                                query_1 = da.database.query("everybady", 1)
                                # encryptdecrypt.pyで暗号化復号化する際にバイト列の暗号化キーを使用する必要があるのでencode('utf-8')によってバイト列に変換
                                st.session_state["generate_key"] = query_1[co].encode('utf-8')
                                st.session_state['page'] = 'main_page'
                                st.rerun()
                            else:
                                me.message.error("ユーザー名またはパスワードが間違っています", 5)
                        else:
                            me.message.error("パスワードに半角スペースまたは全角スペースは使用できません", 5)
                    else:
                        me.message.error("ユーザー名に半角スペースまたは全角スペースは使用できません", 5)
                else:
                    me.message.error("すべての項目を埋めてください", 5)

        if st.button("ユーザー名/パスワードを忘れた場合"):
            st.session_state['page'] = 'forget_security'
            st.rerun()


    def forget_security(self):
        st.title("ユーザー名/パスワード再設定")

        if st.button("一つ前の画面に戻る"):
            st.session_state['page'] = 'login'
            st.rerun()

        if 'reset_username_password' not in st.session_state:
            st.session_state['reset_username_password'] = ""

        with st.form("forgot_password"):            
            email_to_reset = st.text_input("このアプリに登録済みのメールアドレスを入力してください", key="forgot_email")
            if st.form_submit_button("送信＆再送信"):
                if " " not in email_to_reset and "　" not in email_to_reset:
                    if email_to_reset:
                        query_0 = da.database.query("everybady", 0)
                        if ch_us.check_user.email_check(query_0, email_to_reset):
                            code = se_co.securitycode.generate_code(email_to_reset)
                            mail.mail.mail_send(email_to_reset, code)
                            me.message.success(f"{email_to_reset} にセキュリティコードを送信しました", 3)
                        else:
                            me.message.error("このアプリに存在しないメールアドレスです。メールアドレスを記入しなおしてください", 5)
                    else:
                        me.message.error("メールアドレスが記入されていません", 5)
                else:
                    me.message.error("メールアドレスに半角スペースまたは全角スペースは使用できません", 5)

        with st.form("new_security_code"):
            entered_code = st.text_input("セキュリティコードを入力", key="reset_code")
            if st.form_submit_button("決定"):
                if email_to_reset:
                    if " " not in entered_code and "　" not in entered_code:
                        query_0 = da.database.query("everybady", 0)
                        # 入力されたメールアドレスを使用して認証
                        if ch_us.check_user.email_check(query_0, email_to_reset) and se_co.securitycode.verify_code(email_to_reset, entered_code):
                            bo, co = ch_us.check_user.email_check(query_0, email_to_reset)
                            st.session_state["co"] = co
                            st.session_state['page'] = 're_username_password'
                            st.rerun()
                        else:
                            me.message.error("セキュリティコードが誤っている、またはコードが期限切れです", 5)
                    else:
                        me.message.error("セキュリティコードに半角スペースまたは全角スペースは使用できません", 5)
                else:
                    me.message.error("メールアドレスを記入して、上記の「送信＆再送信」をクリックしてください", 5)


    def re_username_password(self):
        st.title("ユーザー名/パスワード再設定")
        with st.form("re_username_password"):
            new_username = st.text_input("新しいユーザー名", key="new_reset_username")
            new_password = st.text_input("新しいパスワード（パスワードにはローマ字の大文字、小文字、数字を必ず一つ以上含めるようにして14文字以上であること。全角文字は使用できない。）", type="password", key="new_reset_password")
            if st.form_submit_button("決定"):
                if new_username and new_password:
                    if " " not in new_username and "　" not in new_username:
                        if " " not in new_password and "　" not in new_password:
                            valid_password, error_message = self.validate_password(new_password)
                            if not valid_password:
                                me.message.error(error_message, 20)
                                # ここで処理を終了
                                return

                            query_0 = da.database.query("everybady", 0)
                            # ユーザー名が既に存在するかチェック
                            if ch_us.check_user.username_check(query_0, new_username):
                                me.message.error("このユーザー名は既に存在します", 5)
                            else:
                                # ユーザー名とパスワードの更新＆ログイン後の処理
                                hashed_new_username = bcrypt.hashpw(new_username.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                                hashed_new_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                                query_0 = da.database.query("everybady", 0)
                                query_0_list = list(query_0.keys())
                                query_0_list_email = query_0_list[st.session_state["co"]]
                                query_0[query_0_list_email] = {hashed_new_username:hashed_new_password}
                                da.database.update(query_0)
                                me.message.success("ユーザー名とパスワードが再設定されました", 3)
                                query_1 = da.database.query("everybady", 1)
                                st.session_state["generate_key"] = query_1[st.session_state["co"]].encode('utf-8')
                                st.session_state['page'] = 'main_page'
                                st.rerun()
                        else:
                            me.message.error("パスワードに半角スペースまたは全角スペースは使用できません", 5)
                    else:
                        me.message.error("ユーザー名に半角スペースまたは全角スペースは使用できません", 5)
                else:
                    me.message.error("すべての項目を埋めてください", 5)


    def validate_password(self, password):
        if re.search(r'[^\x00-\x7F]', password) or len(password) < 14 or not re.search("[A-Z]", password) or not re.search("[a-z]", password) or not re.search("[0-9]", password):
            return False, "パスワードにはローマ字の大文字、小文字、数字を必ず一つ以上含めるようにして14文字以上であること。全角文字は使用できない。"
        return True, ""


    def signin(self):
        st.title("初めての方")

        if st.button("ホームページに戻る"):
            st.session_state['page'] = 'home'
            st.rerun()

        if 'signin_button' not in st.session_state:
            st.session_state['signin_button'] = ""

        if 'signin_send_button' not in st.session_state:
            st.session_state['signin_send_button'] = ""

        with st.form("security_code_send"):
            new_username = st.text_input("新規ユーザー名", key="new_username")
            new_password = st.text_input("新規パスワード（パスワードにはローマ字の大文字、小文字、数字を必ず一つ以上含めるようにして14文字以上であること。全角文字は使用できない。）", type="password", key="new_password")
            new_mail = st.text_input("新規メールアドレス", key="new_mail")

            if st.form_submit_button("送信＆再送信"):
                if new_username and new_password and new_mail:
                    if " " not in new_username and "　" not in new_username:
                        if " " not in new_password and "　" not in new_password:
                            if " " not in new_mail and "　" not in new_mail:
                                valid_password, error_message = self.validate_password(new_password)
                                if not valid_password:
                                    me.message.error(error_message, 20)
                                    # ここで処理を終了
                                    return

                                query_0 = da.database.query("everybady", 0)
                                # ユーザー名が既に存在するかチェック
                                if ch_us.check_user.username_check(query_0, new_username):
                                    me.message.error("このユーザー名は既に存在します", 5)
                                # メールアドレスが既に存在するかチェック
                                elif ch_us.check_user.email_check(query_0, new_mail):
                                    me.message.error("このメールアドレスは既にサインインされています", 5)
                                else:
                                    # セキュリティコードの生成
                                    code = se_co.securitycode.generate_code(new_mail)
                                    try:
                                        # セキュリティコードを含むメールを送信
                                        mail.mail.mail_send(new_mail, code)
                                        me.message.success(f"{new_mail} にセキュリティコードを送信しました", 3)
                                    except HttpError:
                                        me.message.error("正しいメールアドレスを入力してください", 5)             
                            else:
                                me.message.error("メールアドレスに半角スペースまたは全角スペースは使用できません", 5)                            
                        else:
                            me.message.error("パスワードに半角スペースまたは全角スペースは使用できません", 5)
                    else:
                        me.message.error("ユーザー名に半角スペースまたは全角スペースは使用できません", 5)
                else:
                    me.message.error("すべての項目を埋めてください", 5)

            # メッセージ用の表示エリア
            message_area_signin_code = st.container()
            # メッセージ用の表示エリアをさらに上書き可能なエリアにする
            message_area_signin_code_empty = message_area_signin_code.empty()            

            entered_code = st.text_input("セキュリティコードを入力", key="security_code")
            if st.form_submit_button("決定"):
                if new_username and new_password and new_mail:
                    if " " not in entered_code and "　" not in entered_code:
                        # 入力されたセキュリティコードが適切であるか検証
                        if se_co.securitycode.verify_code(new_mail, entered_code):
                            # サインインした後の処理をここに記述
                            hashed_new_username = bcrypt.hashpw(new_username.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                            hashed_new_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                            hashed_new_email = bcrypt.hashpw(new_mail.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

                            query_0 = da.database.query("everybady", 0)
                            query_0[hashed_new_email] = {hashed_new_username:hashed_new_password}
                            da.database.update(query_0)
                            st.session_state["generate_key"] = en_de.encrypt_decrypt.user_generate_key()
                            generate_key_decode = st.session_state["generate_key"].decode('utf-8')
                            query_1 = da.database.query("everybady", 1)
                            query_1.append(generate_key_decode)
                            da.database.update(query_1)
                            # 復習する日数間隔グループの情報を入れる辞書。{"グループ1":[2,5,8]}といった形式になる。st.session_state["generate_key"]の1行目に追加。
                            da.database.default(st.session_state["generate_key"], {})
                            # 日付をキー、「予定」の欄で入力された文字を値として保存する辞書。{2024-1-11:[予定1,予定2]}といった形式になる。st.session_state["generate_key"]の2行目に追加。
                            da.database.default(st.session_state["generate_key"], {})
                            st.session_state['page'] = 'main_page'
                            st.rerun()
                        else:
                            me.placeholder.error("セキュリティコードが誤っている、またはコードが期限切れです", message_area_signin_code_empty, 5)
                    else:
                        me.placeholder.error("セキュリティコードに半角スペースまたは全角スペースは使用できません", message_area_signin_code_empty, 5)
                else:
                    me.placeholder.error("セキュリティコード以外のすべての項目を埋めてから、上記の「送信＆再送信」をクリックしてください", message_area_signin_code_empty, 5)

page_login = Login()