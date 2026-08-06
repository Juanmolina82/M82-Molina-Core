import requests, time, os

# Watchlist Extensible - Agrega aquí todos los tickers que quieras rastrear
WATCHLIST = ["SQQQ", "TQQQ", "OIH", "SPXU", "UVXY", "XLE"]

s = requests.Session()
s.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})

def fetch_ticker_data(symbol):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1m&range=1d"
    try:
        r = s.get(url, timeout=5).json()
        meta = r['chart']['result'][0]['meta']
        price = meta.get('regularMarketPrice', 0.0)
        prev_close = meta.get('chartPreviousClose', price)
        volume = meta.get('regularMarketVolume', 0)
        p_change = ((price - prev_close) / prev_close) * 100 if prev_close else 0.0
        return {"price": price, "change": p_change, "volume": volume}
    except Exception:
        return None

print("🔍 [M82 MULTI-TICKER FLOW TRACKER] ONLINE...", flush=True)

while True:
    os.system("clear")
    print("===================================================================", flush=True)
    print(f" 📊 M82 INSTITUTIONAL TICKER FLOW TRACKER • {time.strftime('%H:%M:%S EST')}", flush=True)
    print("===================================================================", flush=True)
    
    for symbol in WATCHLIST:
        data = fetch_ticker_data(symbol)
        if data:
            color = "🟩" if data['change'] >= 0 else "🔴"
            sign = "+" if data['change'] >= 0 else ""
            print(f"{color} {symbol:<8} | Price: ${data['price']:<8.3f} | Chg: {sign}{data['change']:.2f}% | Vol: {data['volume']:,}", flush=True)
        else:
            print(f"⚪ {symbol:<8} | [Data Fetch Error]", flush=True)
            
    print("===================================================================", flush=True)
    print(" 💡 Subir tickers editando la lista WATCHLIST en daemons/m82_flow_tracker.py", flush=True)
    
    time.sleep(30)
