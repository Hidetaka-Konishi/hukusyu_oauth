import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from email.mime.text import MIMEText
import base64

app_name = "復習カレンダー"

class Mail:
    def message_base64_encode(self, message):
        return base64.urlsafe_b64encode(message.as_bytes()).decode()

    def mail_send(self, to_mail, code):
        scopes = ["https://mail.google.com/"]
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
        creds = Credentials.from_authorized_user_info(creds_data, scopes)
        service = build('gmail', 'v1', credentials=creds)
        
        # 送りたいメッセージを指定する。
        message = MIMEText(f'送信元：{app_name}\n\nあなたのセキュリティコードは {code} です\n\n※有効期限は5分です')
        # 送信先のメールアドレスを指定する。
        message['To'] = to_mail
        # 送信元のメールアドレスを指定する。
        message['From'] = os.environ["GMAIL"]
        # 件名を指定する。
        message['Subject'] = f'{app_name}のセキュリティコード'
        raw = {'raw': self.message_base64_encode(message)}
        service.users().messages().send(
            userId='me',
            body=raw
        ).execute()

mail = Mail()