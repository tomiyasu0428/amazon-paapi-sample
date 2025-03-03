# Amazon PA-API 5.0 API リファレンス

このドキュメントでは、このプロジェクトで使用している主なAPIエンドポイントと機能について説明します。

## フロント側API

### 検索API

**エンドポイント**: `/api/search`  
**メソッド**: GET  
**パラメータ**:
- `q` - 検索キーワード（必須）
- `category` - 検索カテゴリ（デフォルト: "All"）

**レスポンス例**:
```json
{
  "products": [
    {
      "asin": "B07XXXXX",
      "title": "商品タイトル",
      "url": "https://www.amazon.co.jp/...",
      "image": "https://m.media-amazon.com/...",
      "price": 1980,
      "currency": "￥",
      "prime": true
    },
    // 他の商品...
  ]
}
```

### 商品詳細API

**エンドポイント**: `/api/product/<asin>`  
**メソッド**: GET  
**パラメータ**:
- `asin` - Amazonの商品ID（URL内に指定）

**レスポンス例**:
```json
{
  "product": {
    "asin": "B07XXXXX",
    "title": "詳細な商品タイトル",
    "url": "https://www.amazon.co.jp/...",
    "image": "https://m.media-amazon.com/...",
    "price": 1980,
    "currency": "￥",
    "features": [
      "商品の特徴1",
      "商品の特徴2"
    ],
    "prime": true
  }
}
```

## PA-API 機能

### amazon_paapi.AmazonApi クラス

このプロジェクトでは、`python-amazon-paapi` ライブラリの `AmazonApi` クラスを使用して、Amazon PA-API にアクセスしています。

主なメソッド:

#### search_items(keywords, search_index, ...)

商品を検索するメソッド。

**パラメータ**:
- `keywords` - 検索キーワード
- `search_index` - 検索カテゴリ
- その他のパラメータについては、最新の公式ドキュメントを参照してください。

**利用例**:
```python
results = amazon.search_items(
    keywords="Python プログラミング",
    search_index="Books"
)
```

#### get_items(asin_list, ...)

指定したASINの商品情報を取得するメソッド。

**パラメータ**:
- `asin_list` - 取得する商品のASINリスト
- その他のパラメータについては、最新の公式ドキュメントを参照してください。

**利用例**:
```python
results = amazon.get_items(
    ["B07XXXXX", "B08YYYYY"]
)
```

#### get_browse_nodes(browse_node_ids, ...)

ブラウズノード（カテゴリ階層）情報を取得するメソッド。

**パラメータ**:
- `browse_node_ids` - ブラウズノードIDのリスト
- その他のパラメータについては、最新の公式ドキュメントを参照してください。

**利用例**:
```python
results = amazon.get_browse_nodes(
    browse_node_ids=["2275256051"]  # エレクトロニクスカテゴリのID
)
```

## 公式ドキュメント

より詳細な情報や最新の仕様については、以下の公式ドキュメントを参照してください：

- [Amazon Product Advertising API 5.0 ドキュメント](https://webservices.amazon.co.jp/paapi5/documentation/)
- [python-amazon-paapi ライブラリ](https://github.com/sergioteula/python-amazon-paapi)