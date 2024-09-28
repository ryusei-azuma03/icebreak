from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import random 
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)  # 


# APIキーの取得
apikey ="5ad2f3825f164bf8abdc54e5add5da14"
print(f"GNEWS_API_KEY: {apikey}")  # デバッグ用


@app.route('/api/topic', methods=['GET'])
def get_topic():
    topics = [
    "このニュースは彼氏，彼女をどう幸せにするか？",
    "このニュースは我々のビジネスにどんな機会をもたらすか？",
    "このニュースは我々のビジネスにどんな脅威があるか？",
    "このニュースによって、儲ける会社は？",
    "このニュースによって、10年後生活はどう変わる？"
]
# ランダムに1つのテーマを選んで返す
    response = {
        "question": random.choice(topics)
    }
    
    return jsonify(response)


# 前日のニュース
@app.route('/api/news', methods=['GET'])
def get_news():
    url = "https://gnews.io/api/v4/top-headlines"
    params = {
        "lang": "ja",          # 日本語
        "country": "jp",       # 日本
        "category": "technology",  # テクノロジー（必要に応じて変更可能）
        "max": 5,             # 取得する記事数（必要に応じて変更可能）
        "apikey": apikey
    }

    # デバッグ: パラメータの確認
    print(f"Requesting GNews API with params: {params}")

    # APIリクエストを送信
    response = requests.get(url, params=params)

    # レスポンスのステータスコードと内容をログに出力
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")

    try:
        data = response.json()
    except ValueError as e:
        # JSONデコードエラーの場合の処理
        print("JSONDecodeError:", e)
        return jsonify({"error": "Invalid JSON response from GNews API"}), 500

    if response.status_code == 200:
        articles = data.get('articles', [])
        return jsonify(articles)
    else:
        error = data.get('errors', 'Unknown error occurred')
        return jsonify({"error": error}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)

