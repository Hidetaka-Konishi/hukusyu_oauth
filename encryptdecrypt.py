from cryptography.fernet import Fernet

class EncryptDecrypt:
    # 暗号化キーを生成する
    def user_generate_key(self):
        # バイト列の暗号化キーが生成される
        return Fernet.generate_key()

    # データを暗号化する。messageは暗号化したい文字列、keyはFernet.generate_key()によって生成された暗号化キーを指定する。
    def encrypt_message(self, message, key):
        # Fernet.generate_key()によって生成されたバイト列の暗号化キー専用のFernetオブジェクトを作成
        f = Fernet(key)
        encrypted_message = f.encrypt(message.encode())
        return encrypted_message

    # データを復号化する
    def decrypt_message(self, encrypted_message, key):
        f = Fernet(key)
        decrypted_message = f.decrypt(encrypted_message).decode()
        return decrypted_message

encrypt_decrypt = EncryptDecrypt()