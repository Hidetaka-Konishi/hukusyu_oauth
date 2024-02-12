import streamlit as st
from datetime import datetime, timedelta
import password_generate as pa_ge

class SecurityCode:
    def generate_code(self, email):
        code = pa_ge.password_generate.alphabet_big_small_number(8)
        expiration_time = datetime.now() + timedelta(minutes=5)
        str_expiration_time = str(expiration_time)
        st.session_state['generate_code'] = {email:(code, str_expiration_time)}
        return code

    def verify_code(self, email, user_code):
        # セキュリティコードと有効期限をそれぞれ変数に代入
        code, str_expiration_time = st.session_state['generate_code'][email]
        datetime_object = datetime.strptime(str_expiration_time, "%Y-%m-%d %X.%f")
        if datetime.now() < datetime_object and str(code) == user_code:
            return True
        else:
            return False

securitycode = SecurityCode()