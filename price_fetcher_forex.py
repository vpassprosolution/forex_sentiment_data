# ✅ price_fetcher_forex.py – Fetch and save live forex prices from TwelveData
import requests
import psycopg2
from datetime import datetime
import time

# 📡 TwelveData API
API_KEY = '3d446375f34d469a8d776288c82950e9'
BASE_URL = 'https://api.twelvedata.com/price'

# 🏦 PostgreSQL config
DB_CONFIG = {
    'dbname': 'railway',
    'user': 'postgres',
    'password': 'vVMyqWjrqgVhEnwyFifTQxkDtPjQutGb',
    'host': 'interchange.proxy.rlwy.net',
    'port': '30451'
}

# 🎯 Forex Pairs (TwelveData requires slash format)
forex_pairs = [
    "EUR/USD", "GBP/USD", "AUD/USD", "NZD/USD", "USD/JPY",
    "USD/CAD", "USD/CHF", "USD/CNH", "USD/HKD", "USD/SEK",
    "USD/SGD", "USD/NOK", "USD/MXN", "USD/ZAR", "USD/THB",
    "USD/KRW", "USD/PHP", "USD/TRY", "USD/INR", "USD/VND"
]

def update_price(symbol, price):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO forex_sentiment (symbol, price, last_updated)
            VALUES (%s, %s, %s)
            ON CONFLICT (symbol) DO UPDATE
            SET price = EXCLUDED.price,
                last_updated = EXCLUDED.last_updated
        """, (symbol.replace('/', ''), price, datetime.utcnow()))

        conn.commit()
        cursor.close()
        conn.close()
        print(f"✅ Saved → {symbol} = {price}")
    except Exception as e:
        print(f"❌ DB Error for {symbol}: {e}")

def fetch_price(symbol):
    """Fetch price for a single symbol. Used by news_fetcher_forex."""
    try:
        response = requests.get(BASE_URL, params={
            'symbol': symbol,
            'apikey': API_KEY
        })
        data = response.json()
        if 'price' in data:
            return float(data['price'])
        else:
            print(f"❌ API error for {symbol}: {data}")
    except Exception as e:
        print(f"❌ Failed fetching {symbol}: {e}")
    return None

def fetch_prices():
    print("📡 Fetching Forex Prices...\n")
    for symbol in forex_pairs:
        price = fetch_price(symbol)
        if price is not None:
            update_price(symbol, price)
        time.sleep(8)  # 🔄 Respect API limit (8/minute)

if __name__ == "__main__":
    fetch_prices()
