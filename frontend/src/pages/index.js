import { useState } from 'react';
import NewsItem from '../components/NewsItem';
import TodayQuestion from '../components/TodayQuestion';
import styles from '../styles/Home.module.css';

export default function Home() {
  const [news, setNews] = useState([]);
  const [question, setQuestion] = useState("");
  const [showNews, setShowNews] = useState(false);
  const [showQuestion, setShowQuestion] = useState(false);
  const [selectedNews, setSelectedNews] = useState(null);
  const [explanation, setExplanation] = useState("");

  // 今日の問いを取得する関数
  const fetchQuestion = () => {
    fetch('http://127.0.0.1:5000/api/topic')  // バックエンドのエンドポイントを指定
      .then(res => {
        if (!res.ok) {
          throw new Error('Network response was not ok');
        }
        return res.json();
      })
      .then(data => {
        if (data && data.question) {
          setQuestion(data.question); // 取得したテーマをステートに設定
          setShowQuestion(true); // 表示フラグを true にする
        } else {
          throw new Error('Invalid response format');
        }
      })
      .catch(error => {
        console.error('Error fetching question:', error);
        setQuestion('問いを取得できませんでした。もう一度お試しください。');
        setShowQuestion(true); // エラーメッセージを表示
      });
  };

  // ニュースを取得する関数
  const fetchNews = () => {
    fetch('http://127.0.0.1:5000/api/news')  // バックエンドのエンドポイントを指定
      .then(res => {
        if (!res.ok) {
          throw new Error('Network response was not ok');
        }
        return res.json();
      })
      .then(data => {
        setNews(data);
        setShowNews(true); // 表示フラグを true にする
      })
      .catch(error => {
        console.error('Error fetching news:', error);
      });
  };

  // ニュースを選択する関数
  const selectNews = (newsItem) => {
    setSelectedNews(newsItem);
  };

  // 解説を取得する関数
  const fetchExplanation = async () => {
    if (!selectedNews || !question) {
      alert('解説を表示するにはニュースと問いを選択してください。');
      return;
    }

    try {
      const response = await fetch('http://127.0.0.1:5000/api/explanation', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          news_title: selectedNews.title,
          question: question,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to fetch explanation');
      }

      const data = await response.json();
      setExplanation(data.explanation || '解説を取得できませんでした。');
    } catch (error) {
      console.error('Error fetching explanation:', error);
      setExplanation('解説を取得できませんでした。もう一度お試しください。');
    }
  };

  return (
    <div className={styles.container}>
      <h1>ITアイスブレイクアプリ</h1>
      
      {/* ボタンを中央に配置するためのコンテナ */}
      <div className={styles.buttonContainer}>
        {/* 今日の問いボタン */}
        <button onClick={fetchQuestion} className={styles.button}>
          今日の問いは？
        </button>
        
        {/* ニュースを呼び出すボタン */}
        <button onClick={fetchNews} className={styles.button}>
          Newsを呼び出す
        </button>
      </div>
      
      {/* 今日の問い表示（showQuestion フラグでアニメーションを制御） */}
      {showQuestion && (
        <div className={styles.questionContainer}>
          <TodayQuestion question={question} />
        </div>
      )}
      
      {/* ニュースリスト表示（showNews フラグでアニメーションを制御） */}
      {showNews && (
        <div className={`${styles.newsList} ${showNews ? styles.show : ''}`}>
          {news.map((item, index) => (
            <div 
              key={index} 
              className={`${styles.newsItemContainer} ${selectedNews === item ? styles.selectedNews : ''}`}
              onClick={() => selectNews(item)}
            >
              <NewsItem title={item.title} link={item.source.url} /> {/* source.url を link プロパティとして渡す */}
            </div>
          ))}
        </div>
      )}

      {/* 解説ボタン */}
      <div className={styles.explanationContainer}>
        <button onClick={fetchExplanation} className={styles.button}>
          解説
        </button>
      </div>

      {/* 解説表示 */}
      {explanation && (
        <div className={styles.explanationBox}>
          <p>{explanation}</p>
        </div>
      )}
    </div>
  );
}
