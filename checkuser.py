import bcrypt

class CheckUser:
    # ユーザー名が既に登録されているかをチェック。usernameには暗号化する前のユーザー名を記入する。
    def username_check(self, dict_name, username):
        for va in dict_name.values():
            # ユーザー名を順次アクセス
            value_key = next(iter(va))
            # 過去に登録済みのユーザー名と今回入力したユーザー名が一致するかチェック
            if bcrypt.checkpw(username.encode('utf-8'), value_key.encode('utf-8')):
                return True


    # ユーザー名とパスワードのペアが既に登録されているかをチェック。登録されている場合はユーザー名とパスワードのペアのインデックスを出力。usernameとpasswordには暗号化する前のユーザー名とパスワードをそれぞれ記入する。
    def username_password_check(self, dict_name, username, password):
        count = -1
        for va in dict_name.values():
            # ユーザー名を順次アクセス
            value_key = next(iter(va))
            # パスワードを順次アクセス
            value_value = va[value_key]
            count += 1
            # 過去に登録済みのユーザー名と今回入力したユーザー名が一致するかチェック
            if bcrypt.checkpw(username.encode('utf-8'), value_key.encode('utf-8')):
                # 過去に登録済みのパスワードと今回入力したパスワードが一致するかチェック
                if bcrypt.checkpw(password.encode('utf-8'), value_value.encode('utf-8')):
                    return True, count


    # メールアドレスが既に登録されているかをチェック。emailには暗号化する前のメールアドレスを記入する。
    def email_check(self, dict_name, email):
        count = -1
        for em in dict_name.items():
            # メールアドレスを順次アクセス
            email_iter = next(iter(em))
            count += 1
            # 過去に登録済みのメールアドレスと今回入力したメールアドレスが一致するかチェック
            if bcrypt.checkpw(email.encode('utf-8'), email_iter.encode('utf-8')):
                return True, count

check_user = CheckUser()