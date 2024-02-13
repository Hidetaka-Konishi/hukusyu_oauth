## アプリの概要
学習した内容をアプリに記載することで、その学習した内容の復習するべき日の当日に表示するアプリです。

今日、復習するべき内容が一目でわかるようになっています。

以下のURLから実際にアプリをお使いになっていただくことができます。ゲストログイン機能も搭載しています。

https://hukusyuwhen-eauhgtv3ecvypzktmr6tp3.streamlit.app/

## ログイン機能
![Streamlit-GoogleChrome2024-02-1311-45-22-ezgif com-speed](https://github.com/Hidetaka-Konishi/hukusyu_when/assets/142459457/41fe0f99-bc02-4e23-99a8-6a1336e7fa4f)

## ユーザー名/パスワード再設定
![Streamlit-GoogleChrome2024-02-1312-19-46-ezgif com-speed](https://github.com/Hidetaka-Konishi/hukusyu_when/assets/142459457/db8f3b50-3402-4ebf-b809-d250e0ad8c18)

## 復習する内容をカレンダーに振り分ける
![Streamlit-GoogleChrome2024-02-1312-00-35-ezgif com-speed](https://github.com/Hidetaka-Konishi/hukusyu_when/assets/142459457/e5fa1426-57dc-4c2a-a1ea-fce8bd3b1a26)

## 工夫したところ
アプリを使うユーザーがユーザー名/パスワードを忘れてしまったときの対処を工夫しました。

ユーザーがサインイン時に登録したメールアドレスにセキュリティコードを送信します。

このセキュリティコードをアプリに入力することでユーザー名/パスワードを再設定できる項目が表示されます。

セキュリティコードの解読は41年かかる文字列を有効期限5分間に設定することで総当たり攻撃を防いでいます。

## 苦労した点
データベースの操作を行うコードは特殊で理解するのに少し時間がかかりました。

ただ、実際に手を動かしてコードを書き続けることによって、今ではスラスラと書けるようになりました。

## このアプリを作った理由
資格試験の学習をしていた際にカレンダーを使って復習する日を管理していました。

復習する日をカレンダーに割り振る時間を短縮して学習する時間を増やしたいという思いがあり、このアプリを作りました。

AWSエンジニアになった際、インフラのコード化に対して、このアプリ制作で学んだコードを書くスキルが活かせます。

## アプリの構築手順
### 前提条件
・ Streamlitにサインイン済みあること。

・ GoogleとGitHubのアカウントを持っていること。

・ gitがローカル環境にインストール済みであること。

・ Pythonの実行環境があること(Python3.6以上)。

### 手順
1. まずは、Gmailを使ってメール送信するための設定を行います。このURLにアクセスしてください。https://console.cloud.google.com/?hl=ja
2. 「利用規約」にチェックを入れて、「同意して続行」を押します。
![](./image/check_and_agree.png)
3. 検索欄に「Gmail」と記入し、「Gmail API」を選択します。
![](./image/gmail_search.png)
4. 「有効にする」を押します。
![](./image/valid.png)
5. 「認証情報を作成」を押します。
![](./image/certification_create.png)
6. 「ユーザーデータ」を選択し、「次へ」を押します。
![](./image/userdata_cheak.png)
7. 「アプリ名」には好きな名前を付けて、ユーザーサポートメールに自分のメールアドレスを入力します。
![](./image/app_name.png)
8. 「デベロッパーの連絡先情報」の「メールアドレス」にさきほど入力したメールアドレスを入力し、「保存して次へ」を押します。
![](./image/developer_mail.png)
9. 下にスクロールし、「保存して次へ」を押します。
![](./image/under_scroll.png)
10. 「アプリケーションの種類」で「デスクトップアプリ」を選択し、「作成」を押します。
![](./image/desktop_app.png)
11. 「ダウンロード」を押し、「完了」を押します。
![](./image/json_download.png)
12. 「OAuth同意画面」を押します。
![](./image/oauth_agree.png)
13. 「アプリを公開」を押します。
![](./image/app_public.png)
14. 「確認」を押します。
![](./image/push_check.png)
15. ローカルで新しくフォルダを作成して、そのフォルダのターミナルで以下のコマンドを実行します。

```
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
``` 
16. フォルダの中にさっきダウンロードしたjsonファイルを配置します。

17. フォルダの中に好きな名前でPythonのファイルを作成し、以下のコードを記載します。`download.json`の部分はダウンロードしたjsonファイルの相対パスに置き換えてください。そして、このコードを実行します。

```python
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://mail.google.com/']

flow = InstalledAppFlow.from_client_secrets_file(
# ダウンロードしたJSONファイルのパスを指定する
'./download.json', SCOPES)

creds = flow.run_local_server(port=0)

with open('token.json', 'w') as token:
    token.write(creds.to_json())
```

18. 自分のアカウントを選択します。
![](./image/acount_choise.png)
19. 「詳細」を押します。
![](./image/detail.png)
20. 「(安全ではないページ)に移動」を押します。
![](./image/danger_page.png)
21. 「続行」を押します。
![](./image/danger_continue.png)
22. 新たに二つ目のフォルダを作成します。
23. 一つ目のフォルダから二つ目のフォルダに`token.json`ファイルのみを移動させます。これ以降の操作は二つ目のフォルダで行います。
24. ターミナルで以下のコマンドを実行します。

```
git clone https://github.com/Hidetaka-Konishi/hukusyu_when.git
cd hukusyu_when
```
25.  GitHubのダッシュボードから「New」を押します。
![](./image/dashborad_new.png)
26. 「Repository name」に好きな名前を付けて、「Public」を選択します。
![](./image/repository_name.png)
27. 下にスクロールして「Create repository」を押します。
![](./image/create_repository.png)
28. ターミナルで以下のコマンドを実行します。

```
git remote rename origin upstream
```

29. GitHubに戻って、さきほど作成したリポジトリのURLをコピーします。
![](./image/url_copy.png)
1.  ターミナルで以下のコマンドを実行します。「コピーしたURL」の部分はさきほどコピーしたURLに置き換えてください。

```
git remote add origin コピーしたURL 
git push -u origin main
```

31. このURLからStreamlitの公式ページに移動します。https://streamlit.io/
32. 「Sign up」を押します。
![](./image/sign_up.png)
33. 「New app」を押します。
![](./image/new_app.png)
34. 「Repository」にさきほど作成したリポジトリを選択し、「Main file path」を`app.py`に書き換えて、「Deploy!」を押します。
![](./image/deploy_app.png)
35. 以下の画面が表示されるまで待ちます。表示されたら「Manage app」を押します。
![](./image/home_page.png)
36. 縦に「・」が三つある部分を押します。
![](./image/manage_app.png)
37. 「Settings」を押します。
![](./image/settings.png)
38. 「Secrets」を押します。
![](./image/secrets.png)
39.  以下の画像の赤枠に以下のコードを貼り付けます。以下のコードの各変数の値は書かれている説明の通りに書き換えてください。注意点として各変数の値は""(ダブルクォーテーション)で囲んだものを記入してください。最後に、「Save」を押すことでアプリの構築が完了します。
![](./image/environmental_variables.png)

```
GMAIL = メール送信するための設定で入力したメールアドレス

GAPI_TOKEN = token.jsonファイルの"token"の値に書かれている文字列

GAPI_REFRESH_TOKEN = token.jsonファイルの"refresh_token"の値に書かれている文字列

GAPI_CLIENT_ID = token.jsonファイルの"client_id"の値に書かれている文字列

GAPI_CLIENT_SECRET = token.jsonファイルの"client_secret"の値に書かれている文字列
```
