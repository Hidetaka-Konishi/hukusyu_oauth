from cryptography.fernet import Fernet

class EncryptDecrypt:
    # 暗号化キーを生成する
    def generate_key(self):
        return Fernet.generate_key()

    # データを暗号化する
    def encrypt_message(self, message, key):
        f = Fernet(key)
        encrypted_message = f.encrypt(message.encode())
        return encrypted_message

    # データを復号化する
    def decrypt_message(self, encrypted_message, key):
        f = Fernet(key)
        decrypted_message = f.decrypt(encrypted_message).decode()
        return decrypted_message

encrypt_decrypt = EncryptDecrypt()
