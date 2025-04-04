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

# 🎯 Forex Pairs with slash format (✅ required by TwelveData)
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

def fetch_prices():
    print("📡 Fetching Forex Prices...\n")
    for symbol in forex_pairs:
        try:
            response = requests.get(BASE_URL, params={
                'symbol': symbol,
                'apikey': API_KEY
            })
            data = response.json()
            if 'price' in data:
                update_price(symbol, float(data['price']))
            else:
                print(f"❌ API error for {symbol}: {data}")
            time.sleep(8)  # ⏳ Respect TwelveData limit
        except Exception as e:
            print(f"❌ Failed for {symbol}: {e}")

if __name__ == "__main__":
    fetch_prices()
