import streamlit as st
import time

class Message:
    def success(self, send_message, count):
        success_message = st.success(send_message)
        # 成功メッセージを指定した秒数表示
        time.sleep(count)
        # 成功メッセージが削除される
        success_message.empty()
    
    def error(self, send_message, count):
        error_message = st.error(send_message)
        # エラーメッセージを指定した秒数表示
        time.sleep(count)
        # エラーメッセージが削除される
        error_message.empty()


class Placeholder:
    # nameにはst.container()を代入した変数にempty()を加えたものが代入された変数名を指定する
    def success(self, send_message, name, count):
        success_message = name.success(send_message)
        # 成功メッセージを指定した秒数表示
        time.sleep(count)
        # 成功メッセージが削除される
        success_message.empty()

    # nameにはst.container()を代入した変数にempty()を加えたものが代入された変数名を指定する
    def error(self, send_message, name, count):
        error_message = name.error(send_message)
        # エラーメッセージを指定した秒数表示
        time.sleep(count)
        # エラーメッセージが削除される
        error_message.empty()

message = Message()
placeholder = Placeholder()