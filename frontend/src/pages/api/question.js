// 今日の質問を取得する API エンドポイント
export default function handler(req, res) {
    const question = "今年最も重要な技術トレンドは何ですか？";
    res.status(200).json({ question });
  }
  