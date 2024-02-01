import streamlit as st
import string
from datetime import datetime, timedelta
import random

class SecurityCode:
    def generate_code(self, email):
        # 文字セットを作成：数字、大文字、小文字
        digits = string.digits  # 数字
        uppercase = string.ascii_uppercase  # 大文字
        lowercase = string.ascii_lowercase  # 小文字

        # 必ず1文字以上使用するために1文字ずつ選択
        random_digit = random.choice(digits)
        random_upper = random.choice(uppercase)
        random_lower = random.choice(lowercase)

        # 残りの8文字をランダムに選択
        remaining_chars = ''.join(random.choices(digits + uppercase + lowercase, k=8))
        # 生成した文字列を結合
        result = random_digit + random_upper + random_lower + remaining_chars
        # 文字列をシャッフル
        result_list = list(result)
        random.shuffle(result_list)
        code = ''.join(result_list)

        expiration_time = datetime.now() + timedelta(minutes=5)
        str_expiration_time = str(expiration_time)
        st.session_state['generate_code'] = {email:(code, str_expiration_time)}
        return code


    def verify_code(self, email, user_code):
        code, expiration_time = st.session_state['generate_code'][email]
        datetime_object = datetime.strptime(expiration_time, "%Y-%m-%d %X.%f")
        if datetime.now() < datetime_object and str(code) == user_code:
            return True
        else:
            return False

securitycode = SecurityCode()