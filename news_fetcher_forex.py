# ✅ news_fetcher_forex.py – Google News 1 article scraper (1 per pair)

import time
from googlesearch import search
from newspaper import Article
import psycopg2
from psycopg2.extras import RealDictCursor
from database import save_sentiment

# 🏦 PostgreSQL DB URL
DB_URL = "postgresql://postgres:vVMyqWjrqgVhEnwyFifTQxkDtPjQutGb@interchange.proxy.rlwy.net:30451/railway"

# 20 major forex pairs
PAIRS = {
    "EURUSD": "euro dollar",
    "GBPUSD": "pound dollar",
    "AUDUSD": "australian dollar",
    "NZDUSD": "new zealand dollar",
    "USDJPY": "us dollar yen",
    "USDCAD": "us dollar cad",
    "USDCHF": "us dollar franc",
    "USDCNH": "us dollar chinese yuan",
    "USDHKD": "us dollar hkd",
    "USDSEK": "us dollar sek",
    "USDSGD": "us dollar sgd",
    "USDNOK": "us dollar nok",
    "USDMXN": "us dollar peso",
    "USDZAR": "us dollar rand",
    "USDTHB": "us dollar baht",
    "USDKRW": "us dollar krw",
    "USDPHP": "us dollar php",
    "USDTRY": "us dollar lira",
    "USDINR": "us dollar rupee",
    "USDVND": "us dollar vnd"
}

def fetch_article(query):
    try:
        print(f"🔍 Searching: {query}")
        urls = list(search(f"{query} forex news", num_results=5, lang="en"))
        for url in urls:
            if "youtube.com" in url or "twitter.com" in url:
                continue
            article = Article(url)
            article.download()
            article.parse()
            return {
                "title": article.title,
                "summary": article.text[:300],  # just first 300 chars
                "sentiment": "neutral"
            }
    except Exception as e:
        print(f"❌ Error fetching article: {e}")
    return None

def get_price_from_db(symbol):
    try:
        conn = psycopg2.connect(DB_URL, cursor_factory=RealDictCursor)
        cur = conn.cursor()
        cur.execute("SELECT price FROM forex_sentiment WHERE symbol = %s", (symbol,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        return row["price"] if row else None
    except Exception as e:
        print(f"❌ DB fetch error for {symbol}: {e}")
        return None

def run():
    print("📡 Running Forex News Fetcher...\n")
    for symbol, keyword in PAIRS.items():
        print(f"🔍 {symbol} → keyword: {keyword}")
        article = fetch_article(keyword)
        if article:
            price = get_price_from_db(symbol)
            if price:
                save_sentiment(symbol, price, "neutral", "HOLD", article)
                print(f"✅ Saved → {symbol} | {article['title'][:60]}...\n")
            else:
                print(f"❌ Price not found for {symbol}")
        else:
            print("  ❌ No article found.\n")
        print("--------------------------------------------------")
        time.sleep(3)

if __name__ == "__main__":
    run()
