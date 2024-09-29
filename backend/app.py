from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import random 
from dotenv import load_dotenv
from openai import OpenAI
import os

app = Flask(__name__)
CORS(app)

# APIキーの取得
apikey = "5ad2f3825f164bf8abdc54e5add5da14"
print(f"GNEWS_API_KEY: {apikey}")  # デバッグ用

# 環境変数からAPIキーを取得し、エラーハンドリング
openai_api_key = os.getenv("OPENAI_API_KEY")

# OpenAIクライアントの初期化
client = OpenAI(api_key=openai_api_key)


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


@app.route('/api/news', methods=['GET'])
def get_news():
    url = "https://gnews.io/api/v4/search"
    query = (
        '(テクノロジー OR デジタル OR IT OR AI OR データ OR クラウド OR '
        '5G OR IoT OR ロボット OR 自動化 OR サイバーセキュリティ) AND '
        '(企業 OR ビジネス OR 産業 OR 経済 OR 戦略 OR イノベーション)'
    )
    params = {
        "q": query,
        "lang": "ja",
        "country": "jp",
        "max": 100,  # 取得する記事数を増やす
        "apikey": apikey
    }

    response = requests.get(url, params=params)

    try:
        data = response.json()
    except ValueError as e:
        print("JSONDecodeError:", e)
        return jsonify({"error": "Invalid JSON response from GNews API"}), 500

    if response.status_code == 200:
        articles = data.get('articles', [])
        # タイトルまたは説明文でフィルタリング
        tech_related_keywords = [
            'テクノロジー', 'デジタル', 'it', 'ai', 'データ', 'クラウド', '5g', 'iot', 
            'ロボット', '自動化', 'サイバーセキュリティ', 'dx', 'デジタル化', 
            'イノベーション', 'スマート', 'オンライン', 'リモート', 'デジタルトランスフォーメーション'
        ]
        filtered_articles = [
            article for article in articles
            if any(keyword in (article['title'] + ' ' + article['description']).lower() 
                   for keyword in tech_related_keywords)
        ]
        
        # 記事が見つからない場合のメッセージ
        if not filtered_articles:
            return jsonify({"message": "関連する記事が見つかりませんでした。"}), 404
        
        return jsonify(filtered_articles[:5])  # 最大5件に制限
    else:
        error = data.get('errors', 'Unknown error occurred')
        return jsonify({"error": error}), response.status_code
    
# ニュースと問いに基づいた解説を生成するエンドポイント
@app.route('/api/explanation', methods=['POST'])
def get_explanation():
    data = request.json
    news_title = data.get("news_title")
    question = data.get("question")

    if not news_title or not question:
        return jsonify({"error": "ニュースタイトル、問いが必要です"}), 400

    prompt = f"ニュース: {news_title}\n質問: {question}\n上記のニュースと質問に基づいて解説を作成してください。"

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        explanation = response.choices[0].message.content.strip()
        return jsonify({"explanation": explanation})
    except Exception as e:
        print(f"OpenAI API Error: {str(e)}")  # エラーログ
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)

