import bcrypt

class CheckUser:
    # ユーザー名が既に登録されているかをチェック。usernameにはハッシュ化する前のユーザー名を記入する。
    def username_check(self, dict_name, username):
        for va in dict_name.values():
            # ユーザー名を順次アクセス
            value_key = next(iter(va))
            # 過去に登録済みのユーザー名と今回入力したユーザー名をそれぞれハッシュ化してチェック
            if bcrypt.checkpw(username.encode('utf-8'), value_key.encode('utf-8')):
                return True


    # ユーザー名とパスワードのペアが既に登録されているかをチェック。登録されている場合はユーザー名とパスワードのペアのインデックスを出力。usernameとpasswordにはハッシュ化する前のユーザー名とパスワードをそれぞれ記入する。
    def username_password_check(self, dict_name, username, password):
        count = -1
        for va in dict_name.values():
            # ユーザー名を順次アクセス
            value_key = next(iter(va))
            # パスワードを順次アクセス
            value_value = va[value_key]
            count += 1
            # 過去に登録済みのユーザー名をそれぞれハッシュ化してチェック
            if bcrypt.checkpw(username.encode('utf-8'), value_key.encode('utf-8')):
                # 過去に登録済みのパスワードをそれぞれハッシュ化してチェック
                if bcrypt.checkpw(password.encode('utf-8'), value_value.encode('utf-8')):
                    return True, count


    # メールアドレスが既に登録されているかをチェック。emailにはハッシュ化する前のメールアドレスを記入する。
    def email_check(self, dict_name, email):
        count = -1
        for em in dict_name.items():
            # メールアドレスを順次アクセス
            email_iter = next(iter(em))
            count += 1
            # 過去に登録済みのメールアドレスをそれぞれハッシュ化してチェック
            if bcrypt.checkpw(email.encode('utf-8'), email_iter.encode('utf-8')):
                return True, count
        return False

check_user = CheckUser()