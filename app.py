import streamlit as st
import login
import main

class Notpage:
    # アプリのタイトルの設定
    def set_ui(self):
        # UI上の画面上部に表示されるタイトル
        st.set_page_config(page_title="復習カレンダー", page_icon="📚")

    # サイドバーで行われる処理
    def sidebar(self):
        # ラジオボタンで選択したボタンに対応するメソッドを設定
        pages = {
            "今日やること": main.page_multi.schdule_today,
            "予定の追加": main.page_multi.schdule_append,
            "予定の削除": main.page_multi.schdule_del,
            "復習する日数間隔のグループ": main.page_multi.day_interval,
            "カレンダー": main.page_multi.ca
        }
        # サイドバー上にページを選択できるラジオボタンを配置
        selected_page = st.sidebar.radio("【ページの選択】", list(pages.keys()))
        # pages辞書で選択したボタンをメソッドとして実行
        pages[selected_page]()

not_page = Notpage()


if __name__ == "__main__":
    # セッション状態を初期化
    login.page_login.init_session_state()
    # 現在のページに応じて表示内容を変更
    if st.session_state['page'] == 'home':
        login.page_login.home_page()
    elif st.session_state['page'] == 'login':
        login.page_login.login()
    elif st.session_state['page'] == 'signin':
        login.page_login.signin()
    elif st.session_state['page'] == 'forget_security':
        login.page_login.forget_security()
    elif st.session_state['page'] == 're_username_password':
        login.page_login.re_username_password()
    elif st.session_state['page'] == 'signin_email':
        not_page.set_ui()
        not_page.sidebar()
    elif st.session_state['page'] == 'email_push':
        not_page.set_ui()
        not_page.sidebar()
    elif st.session_state['page'] == 'reset_and_login':
        not_page.set_ui()
        not_page.sidebar()