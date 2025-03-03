# トラブルシューティングガイド

このドキュメントでは、Amazon PA-API を使用する際によく発生する問題とその解決策について説明します。

## API接続エラー

### 認証エラー

**エラーメッセージ例**: `The request signature we calculated does not match the signature you provided`

**解決策**:
1. `.env` ファイル内の認証情報（アクセスキー、シークレットキー）が正しいことを確認
2. システム時計が正確であることを確認（認証にはタイムスタンプが使用されます）
3. 地域設定が正しいことを確認（例：日本向けは `co.jp`）

### リクエスト制限エラー

**エラーメッセージ例**: `Request is throttled`

**解決策**:
1. `throttling` パラメータの値を大きくして、リクエスト間の間隔を長くする
   ```python
   amazon = AmazonApi(ACCESS_KEY, SECRET_KEY, ASSOCIATE_TAG, COUNTRY, throttling=2)  # 2秒間隔
   ```
2. 必要最小限のリクエストのみを行うようにコードを最適化

## パラメータエラー

### ResourcesパラメータエラーA

**エラーメッセージ例**: `Parameters for search_items request are not correct: SearchItemsRequest.__init__() got an unexpected keyword argument 'search_items_resource'`

**解決策**:
- パラメータ名を `resources` に修正、または最新版のライブラリドキュメントを参照して正しいパラメータ名を確認

### ResourcesパラメータエラーB

**エラーメッセージ例**: `Parameters for search_items request are not correct: amazon_paapi.sdk.models.search_items_request.SearchItemsRequest() got multiple values for keyword argument 'resources'`

**解決策**:
- `resources` パラメータが重複して渡されている可能性があります
- パラメータを完全に省略してみる
- ライブラリのバージョンを確認し、必要に応じて更新またはダウングレード

## データ処理エラー

### 属性アクセスエラー

**エラーメッセージ例**: `AttributeError: 'Item' object has no attribute 'image_large'`

**解決策**:
- APIレスポンスに期待する属性が含まれていない可能性があります
- 常に `hasattr()` でチェックするか、try-except ブロックを使用して安全に属性にアクセス
  ```python
  image = item.image_large if hasattr(item, 'image_large') else None
  ```

### JSON変換エラー

**エラーメッセージ例**: `TypeError: Object of type Decimal is not JSON serializable`

**解決策**:
- JSONエンコード前に、非シリアライズ可能な型を標準の型に変換
  ```python
  # カスタムJSONエンコーダを使用
  class CustomJSONEncoder(json.JSONEncoder):
      def default(self, obj):
          if isinstance(obj, Decimal):
              return float(obj)
          return super().default(obj)
  
  # 使用例
  json.dumps(data, cls=CustomJSONEncoder)
  ```

## アプリケーションエラー

### 静的ファイル404エラー

**エラーメッセージ例**: `GET /static/no-image.jpg HTTP/1.1" 404`

**解決策**:
- `static` ディレクトリに必要なファイルが存在することを確認
- `static` ディレクトリのパスがFlaskアプリで正しく設定されていることを確認

### テンプレートレンダリングエラー

**エラーメッセージ例**: `jinja2.exceptions.UndefinedError: 'product' is undefined`

**解決策**:
- テンプレートに渡すデータが正しいことを確認
- テンプレート内で条件分岐を使って、データが存在しない場合の処理を追加
  ```html
  {% if product %}
      <!-- 製品データがある場合の表示 -->
  {% else %}
      <!-- 製品データがない場合の表示 -->
  {% endif %}
  ```

## その他の問題

### Amazon PA-API制限

Amazonは定期的にPA-APIの仕様や制限を変更することがあります。最新の情報は、以下の公式ドキュメントで確認してください：

- [Amazon Product Advertising API 5.0 ドキュメント](https://webservices.amazon.co.jp/paapi5/documentation/)
- [python-amazon-paapi ライブラリ](https://github.com/sergioteula/python-amazon-paapi)

問題が解決しない場合は、ライブラリのIssueページで類似の問題を検索するか、新しいIssueを報告することを検討してください。