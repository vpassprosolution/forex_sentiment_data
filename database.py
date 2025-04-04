# ✅ database.py – Save sentiment article into PostgreSQL
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime

# 🎯 Railway PostgreSQL URL
DB_URL = "postgresql://postgres:vVMyqWjrqgVhEnwyFifTQxkDtPjQutGb@interchange.proxy.rlwy.net:30451/railway"

def save_sentiment(symbol, price, sentiment, recommendation, article):
    try:
        conn = psycopg2.connect(DB_URL, cursor_factory=RealDictCursor)
        cur = conn.cursor()

        title = article.get("title", "")
        summary = article.get("summary", "")
        article_sentiment = article.get("sentiment", "neutral")  # default

        cur.execute("""
            INSERT INTO forex_sentiment (
                symbol, price, sentiment, recommendation, last_updated,
                article_title, article_sentiment, article_summary
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (symbol) DO UPDATE
            SET price = EXCLUDED.price,
                sentiment = EXCLUDED.sentiment,
                recommendation = EXCLUDED.recommendation,
                last_updated = EXCLUDED.last_updated,
                article_title = EXCLUDED.article_title,
                article_sentiment = EXCLUDED.article_sentiment,
                article_summary = EXCLUDED.article_summary;
        """, (
            symbol, price, sentiment, recommendation, datetime.now(),
            title, article_sentiment, summary
        ))

        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ DB Insert Error for {symbol}: {e}")
