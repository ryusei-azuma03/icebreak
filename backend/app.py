from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import random 
from dotenv import load_dotenv
from openai import OpenAI
import os
import time

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
    "このニュースは彼氏，彼女,家族をどう幸せにするか？",
    "このニュースは、企業にとってどんな事業や経営上の課題を引き起こす可能性があるか？",
    "このニュースによって、引き起こる企業のITに纏わる課題と今後必要とされるITの人材は？",
    "このニュースによって、ビジネスチャンスが生まれる業界や会社は？なぜその業界や会社にビジネスチャンスが生まれるのか？",
    "このニュースによって、10年後生活はどう変わる？",
    "このニュースによって、企業が将来にむけて検討すべき経営アジェンダは？",
    "このニュースは、副業やフリーランス領域の人材事業を運営している企業にとって、どんなビジネスチャンスになるか？"
]
# ランダムに1つのテーマを選んで返す
    response = {
        "question": random.choice(topics)
    }
    
    return jsonify(response)

def search_news(query, max_results=10):
    url = "https://gnews.io/api/v4/search"
    params = {
        "q": query,
        "lang": "ja",
        "country": "jp",
        "max": max_results,
        "apikey": "5ad2f3825f164bf8abdc54e5add5da14"
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get('articles', [])
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return []

@app.route('/api/news', methods=['GET'])
def get_news():
    search_strategies = [
        "テクノロジー OR デジタル OR AI OR IoT",
        "デジタルトランスフォーメーション OR DX OR イノベーション",
        "ビジネス AND (AI OR クラウド OR データ)",
        "企業 AND (デジタル化 OR 自動化)",
        "産業 AND (テクノロジー OR IT)"
    ]
    
    all_articles = []
    for strategy in search_strategies:
        articles = search_news(strategy, max_results=10)
        all_articles.extend(articles)
        if len(all_articles) >= 5:
            break
        time.sleep(1)  # APIリクエスト間に短い遅延を入れる
    
    # 重複を除去
    unique_articles = list({article['url']: article for article in all_articles}.values())
    
    # 関連性でフィルタリング
    relevant_keywords = ['デジタル', 'テクノロジー', 'AI', 'IoT', 'クラウド', 'データ', 'イノベーション', 'DX', '自動化']
    filtered_articles = [
        article for article in unique_articles
        if any(keyword.lower() in (article['title'] + ' ' + article['description']).lower() for keyword in relevant_keywords)
    ]
    
    if not filtered_articles:
        return jsonify({"message": "関連する記事が見つかりませんでした。別のキーワードで試してみてください。"}), 404
    
    return jsonify(filtered_articles[:5])
    
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

