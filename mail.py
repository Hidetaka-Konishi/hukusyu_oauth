import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from email.mime.text import MIMEText
import base64

app_name = "復習カレンダー"

class Mail:
    def message_base64_encode(self, message):
        # message変数に格納されたメッセージをGmail APIが要求するBase64エンコーディングされた文字列形式に変換     
        return base64.urlsafe_b64encode(message.as_bytes()).decode()

    def mail_send(self, to_mail, code):
        scopes = ["https://mail.google.com/"]
        # os.environ.get()によってStreamlitの環境変数に保存した情報を取得
        creds_data = {
            "token": os.environ.get("GAPI_TOKEN"),
            "refresh_token": os.environ.get("GAPI_REFRESH_TOKEN"),
            "token_uri": "https://oauth2.googleapis.com/token",
            "client_id": os.environ.get("GAPI_CLIENT_ID"),
            "client_secret": os.environ.get("GAPI_CLIENT_SECRET"),
            "scopes": scopes,
            "universe_domain": "googleapis.com",
            "expiry": "2023-12-17T06:36:06.732872Z"
        }
        # Google APIを使用するための認証情報を生成
        creds = Credentials.from_authorized_user_info(creds_data, scopes)
        # Gmail APIにアクセスするための設定
        service = build('gmail', 'v1', credentials=creds)
        
        # 送りたいメッセージを指定する
        message = MIMEText(f'送信元：{app_name}\n\nあなたのセキュリティコードは {code} です\n\n※有効期限は5分です')
        # 送信先のメールアドレスを指定する
        message['To'] = to_mail
        # 送信元のメールアドレスを指定する
        message['From'] = os.environ.get("GMAIL")
        # 件名を指定する
        message['Subject'] = f'{app_name}のセキュリティコード'
        # メールの内容をエンコードしてGmail APIが要求する形式である辞書に格納
        raw = {'raw': self.message_base64_encode(message)}
        # Gmail APIを使用して自分のアカウントから、あらかじめ設定された内容と宛先を持つメールを送信
        service.users().messages().send(
            userId='me',
            body=raw
        ).execute()

mail = Mail()