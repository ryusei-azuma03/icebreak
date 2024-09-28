// src/app/news/page.js
import React from 'react';
import NewsList from '../../components/NewsItem';

export default function News() {
  return (
    <div>
      <h2>Today's News</h2>
      <NewsList />
    </div>
  );
}
