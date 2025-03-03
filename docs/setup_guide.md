# Amazon PA-API セットアップガイド

このドキュメントでは、Amazon Product Advertising API (PA-API) 5.0 を使用するためのセットアップ手順を説明します。

## 1. Amazon アソシエイトアカウントの取得

Amazon PA-API を利用するには、まず Amazon アソシエイトプログラムに登録する必要があります。

1. [Amazon アソシエイト公式サイト](https://affiliate.amazon.co.jp/)にアクセス
2. 「今すぐ登録」ボタンをクリックし、登録プロセスを完了
3. 審査が完了し、アカウントが承認されるまで待機（通常は数日程度）

## 2. PA-API アクセス権限の取得

Amazon アソシエイトアカウントが承認されたら、PA-API へのアクセス権限を取得します。

1. Amazon アソシエイトセントラルにログイン
2. 「ツール」→「Product Advertising API」を選択
3. 「登録」または「認証情報を管理」を選択
4. 画面の案内に従って、以下の情報を取得し保存してください：
   - アクセスキー ID
   - シークレットアクセスキー
   - アソシエイトタグ

## 3. 必要なライブラリのインストール

このプロジェクトを実行するには、以下のパッケージが必要です：

```bash
pip install -r requirements.txt
```

または、個別にインストールする場合：

```bash
pip install flask python-amazon-paapi python-dotenv
```

## 4. 環境変数の設定

`.env` ファイルを作成し、取得した認証情報を設定します：

```
AMAZON_ACCESS_KEY=あなたのアクセスキー
AMAZON_SECRET_KEY=あなたのシークレットキー
AMAZON_ASSOCIATE_TAG=あなたのアソシエイトタグ
AMAZON_COUNTRY=co.jp
```

## 5. アプリケーションの実行

以下のコマンドでアプリケーションを起動できます：

```bash
python app.py
```

ブラウザで http://localhost:5000 にアクセスして、アプリケーションを使用開始できます。

## 6. API使用上の注意点

- Amazon PA-API には呼び出し制限があります（1秒あたり1リクエスト程度）
- 商用利用の場合は、Amazon の利用規約を必ず確認してください
- アプリケーションにはアソシエイト・プログラムの開示文を含める必要があります