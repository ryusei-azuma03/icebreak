// components/NewsItem.js
import React from 'react';
import styles from '../styles/NewsItem.module.css'; // 必要に応じてスタイルを作成してください

export default function NewsItem({ title, link }) {
  return (
    <div className={styles.newsItem}>
      <h3>{title}</h3>
      <a href={link} target="_blank" rel="noopener noreferrer" className={styles.newsLink}>
        URL: {link}
      </a> {/* リンクをクリック可能にして表示 */}
    </div>
  );
}
