// ニュースデータを取得する API エンドポイント
export default function handler(req, res) {
    const news = [
      { title: "ITニュースA", link: "https://example.com/news-a" },
      { title: "ITニュースB", link: "https://example.com/news-b" },
      { title: "ITニュースC", link: "https://example.com/news-c" },
      { title: "ITニュースD", link: "https://example.com/news-d" },
      { title: "ITニュースE", link: "https://example.com/news-e" }
    ];
    res.status(200).json(news);
  }
  