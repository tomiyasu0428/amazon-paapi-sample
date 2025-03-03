# Amazon PA-API 5.0 シンプルな商品紹介サイト用サンプルコード

# 必要なライブラリをインストール
# pip install python-amazon-paapi

from amazon_paapi import AmazonApi
import json

# APIキー設定
ACCESS_KEY = 'YOUR_ACCESS_KEY'      # Amazon PA-APIから取得したアクセスキー
SECRET_KEY = 'YOUR_SECRET_KEY'      # Amazon PA-APIから取得したシークレットキー
ASSOCIATE_TAG = 'YOUR_ASSOCIATE_TAG'  # Amazonアソシエイトタグ
COUNTRY = 'co.jp'  # 日本の場合は 'co.jp'、米国の場合は 'com'

# AmazonApiクライアントの初期化
amazon = AmazonApi(ACCESS_KEY, SECRET_KEY, ASSOCIATE_TAG, COUNTRY, throttling=1)  # throttling: API呼び出しの間隔（秒）

# 商品情報を取得する関数（キーワード検索）
def search_amazon_products(keywords, search_index='All'):
    """
    キーワードで商品を検索する関数
    
    Parameters:
    keywords (str): 検索キーワード
    search_index (str): 検索カテゴリ（All, Books, Electronics など）
    
    Returns:
    list: 商品情報のリスト
    """
    try:
        # 検索実行
        search_results = amazon.search_items(
            keywords=keywords,
            search_index=search_index,
            resources=[
                'ItemInfo.Title',
                'ItemInfo.ByLineInfo',
                'ItemInfo.Features',
                'Images.Primary.Large',
                'Offers.Listings.Price',
                'Offers.Listings.DeliveryInfo.IsPrimeEligible'
            ]
        )
        
        # 検索結果の処理
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

# 特定の商品情報を取得する関数（ASIN指定）
def get_amazon_product_info(asin_list):
    """
    ASINで商品情報を取得する関数
    
    Parameters:
    asin_list (list): 取得したい商品のASINリスト
    
    Returns:
    list: 商品情報のリスト
    """
    try:
        # 商品情報の取得
        item_results = amazon.get_items(
            asin_list,
            resources=[
                'ItemInfo.Title',
                'ItemInfo.ByLineInfo',
                'ItemInfo.Features',
                'ItemInfo.ContentInfo',
                'ItemInfo.ProductInfo',
                'ItemInfo.TechnicalInfo',
                'Images.Primary.Large',
                'Images.Variants.Large',
                'Offers.Listings.Price',
                'Offers.Listings.DeliveryInfo.IsPrimeEligible'
            ]
        )
        
        # 結果の処理
        if item_results.get('data'):
            products = []
            for item in item_results['data']:
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
                products.append(product_info)
            return products
        return []
    except Exception as e:
        print(f"商品情報取得中にエラーが発生しました: {str(e)}")
        return []

# ベストセラー商品を取得する関数
def get_amazon_bestsellers(browse_node_id='2275256051'):  # デフォルトはエレクトロニクス
    """
    特定カテゴリのベストセラー商品を取得する関数
    
    Parameters:
    browse_node_id (str): ブラウズノードID（カテゴリID）
    
    Returns:
    list: 商品情報のリスト
    """
    try:
        # ベストセラー検索
        results = amazon.get_browse_nodes(
            browse_node_ids=[browse_node_id],
            resources=[
                'BrowseNodes.Ancestor',
                'BrowseNodes.Children'
            ]
        )
        
        if results and 'data' in results:
            # ブラウズノードの情報を返す
            nodes = []
            for node in results['data']:
                node_info = {
                    'id': node.id,
                    'name': node.name,
                    'children': [{'id': child.id, 'name': child.name} for child in node.children] if hasattr(node, 'children') else []
                }
                nodes.append(node_info)
            return nodes
        return []
    except Exception as e:
        print(f"ベストセラー取得中にエラーが発生しました: {str(e)}")
        return []

# サンプル実行部分
if __name__ == '__main__':
    # キーワード検索の例
    print("=== キーワード検索 ===")
    products = search_amazon_products("Python プログラミング", search_index='Books')
    print(json.dumps(products[:3], indent=4, ensure_ascii=False))
    
    # 特定商品情報取得の例
    print("\n=== 特定商品情報 ===")
    product_info = get_amazon_product_info(['B07G9NLF5C'])  # サンプルASIN
    print(json.dumps(product_info, indent=4, ensure_ascii=False))
    
    # カテゴリ情報取得の例
    print("\n=== カテゴリ情報 ===")
    categories = get_amazon_bestsellers()
    print(json.dumps(categories, indent=4, ensure_ascii=False))