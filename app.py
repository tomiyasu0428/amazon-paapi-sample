# シンプルな商品紹介Webアプリケーション (Flask版)
# 必要なライブラリのインストール:
# pip install flask python-amazon-paapi

from flask import Flask, render_template, request, jsonify
from amazon_paapi import AmazonApi
import os
import json
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

app = Flask(__name__)

# Amazon PA-API設定
ACCESS_KEY = os.environ.get('AMAZON_ACCESS_KEY', 'YOUR_ACCESS_KEY')
SECRET_KEY = os.environ.get('AMAZON_SECRET_KEY', 'YOUR_SECRET_KEY')
ASSOCIATE_TAG = os.environ.get('AMAZON_ASSOCIATE_TAG', 'YOUR_ASSOCIATE_TAG')
COUNTRY = os.environ.get('AMAZON_COUNTRY', 'co.jp')  # 日本の場合

# AmazonApiクライアントの初期化
amazon = AmazonApi(ACCESS_KEY, SECRET_KEY, ASSOCIATE_TAG, COUNTRY, throttling=1)

# キーワード検索関数
def search_amazon_products(keywords, search_index='All'):
    try:
        # 最小限のパラメータだけで呼び出してみる
        search_results = amazon.search_items(
            keywords=keywords,
            search_index=search_index
            # resourcesパラメータは省略
        )
        
        if search_results.get('data'):
            products = []
            for item in search_results['data']:
                product_info = {
                    'asin': item.asin,
                    'title': item.title,
                    'url': item.detail_page_url,
                    'image': item.image_large if hasattr(item, 'image_large') else None,
                    'price': item.prices.price if hasattr(item, 'prices') and hasattr(item.prices, 'price') else None,
                    'currency': item.prices.currency if hasattr(item, 'prices') and hasattr(item.prices, 'currency') else None,
                    'prime': item.prime_eligible if hasattr(item, 'prime_eligible') else None
                }
                products.append(product_info)
            return products
        return []
    except Exception as e:
        print(f"検索中にエラーが発生しました: {str(e)}")
        return []

# 商品詳細取得関数
def get_amazon_product_info(asin):
    try:
        # 最小限のパラメータだけで呼び出してみる
        item_results = amazon.get_items(
            [asin]
            # resourcesパラメータは省略
        )
        
        if item_results.get('data'):
            item = item_results['data'][0]
            product_info = {
                'asin': item.asin,
                'title': item.title,
                'url': item.detail_page_url,
                'image': item.image_large if hasattr(item, 'image_large') else None,
                'price': item.prices.price if hasattr(item, 'prices') and hasattr(item.prices, 'price') else None,
                'currency': item.prices.currency if hasattr(item, 'prices') and hasattr(item.prices, 'currency') else None,
                'features': item.features if hasattr(item, 'features') else [],
                'prime': item.prime_eligible if hasattr(item, 'prime_eligible') else None
            }
            return product_info
        return None
    except Exception as e:
        print(f"商品情報取得中にエラーが発生しました: {str(e)}")
        return None

# ルート - 検索ページ
@app.route('/')
def index():
    return render_template('index.html')

# 検索API
@app.route('/api/search', methods=['GET'])
def search():
    keywords = request.args.get('q', '')
    category = request.args.get('category', 'All')
    
    if not keywords:
        return jsonify({'error': 'キーワードを入力してください'}), 400
    
    products = search_amazon_products(keywords, category)
    return jsonify({'products': products})

# 商品詳細API
@app.route('/api/product/<asin>', methods=['GET'])
def product_details(asin):
    product = get_amazon_product_info(asin)
    
    if product:
        return jsonify({'product': product})
    return jsonify({'error': '商品が見つかりませんでした'}), 404

# 商品詳細ページ
@app.route('/product/<asin>')
def product_page(asin):
    product = get_amazon_product_info(asin)
    
    if product:
        return render_template('product.html', product=product)
    return render_template('error.html', message='商品が見つかりませんでした')

if __name__ == '__main__':
    app.run(debug=True)