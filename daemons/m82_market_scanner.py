import requests, time, os

# Universo de cobertura masiva (Semis, MegaCaps, ETFs Apalancados, Index)
WATCHLIST = [
    "QQQ", "SPY", "SOXL", "SOXS", "TQQQ", "SQQQ", "NVDA", "TSLA", 
    "AMD", "ARM", "MU", "AVGO", "SMCI", "MSFT", "AAPL", "AMZN", 
    "GOOGL", "KORU", "SNXX", "MSTU", "SPCH", "DRAM", "MUU", "BITO"
]

s = requests.Session()
s.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})

def scan_full_market():
    market_data = []
    
    # Ingesta masiva en paralelo/bloque
    symbols_str = ",".join(WATCHLIST)
    url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={symbols_str}"
    
    try:
        r = s.get(url, timeout=5).json()
        results = r.get('quoteResponse', {}).get('result', [])
        
        for item in results:
            symbol = item.get('symbol')
            price = item.get('regularMarketPrice', 0.0)
            chg_pct = item.get('regularMarketChangePercent', 0.0)
            volume = item.get('regularMarketVolume', 0)
            turnover = price * volume # Volumen en Dólares ($)
            
            market_data.append({
                "symbol": symbol,
                "price": price,
                "chg_pct": chg_pct,
                "volume": volume,
                "turnover": turnover
            })
            
        return market_data
    except Exception as e:
        print(f"Error scanning market: {e}", flush=True)
        return []

print("🔥 M82 FULL MARKET SCANNER ONLINE — Realtime Volume & Movers Stream...", flush=True)

while True:
    data = scan_full_market()
    if data:
        # Ordenar por Top Gainers, Top Losers y Mayor Volumen
        gainers = sorted([x for x in data if x['chg_pct'] > 0], key=lambda x: x['chg_pct'], reverse=True)[:5]
        losers = sorted([x for x in data if x['chg_pct'] < 0], key=lambda x: x['chg_pct'])[:5]
        vol_leaders = sorted(data, key=lambda x: x['turnover'], reverse=True)[:5]
        
        os.system("clear")
        print("===================================================================", flush=True)
        print(f" 🚀 M82 LIVE MARKET SCANNER • {time.strftime('%H:%M:%S EST')}", flush=True)
        print("===================================================================", flush=True)
        
        print("\n🟩 TOP GAINERS (%)", flush=True)
        print(f"{'SYMBOL':<8} | {'PRICE':<10} | {'CHANGE (%)':<10} | {'VOLUME':<12}", flush=True)
        print("-" * 50, flush=True)
        for g in gainers:
            print(f"{g['symbol']:<8} | ${g['price']:<9.2f} | +{g['chg_pct']:<9.2f}% | {g['volume']/1e6:<9.2f}M", flush=True)
            
        print("\n🟥 TOP LOSERS (%)", flush=True)
        print(f"{'SYMBOL':<8} | {'PRICE':<10} | {'CHANGE (%)':<10} | {'VOLUME':<12}", flush=True)
        print("-" * 50, flush=True)
        for l in losers:
            print(f"{l['symbol']:<8} | ${l['price']:<9.2f} | {l['chg_pct']:<9.2f}% | {l['volume']/1e6:<9.2f}M", flush=True)

        print("\n💵 TOP TURNOVER / INSTITUTIONAL VOLUME ($)", flush=True)
        print(f"{'SYMBOL':<8} | {'PRICE':<10} | {'CHANGE (%)':<10} | {'TURNOVER ($)':<12}", flush=True)
        print("-" * 50, flush=True)
        for v in vol_leaders:
            print(f"{v['symbol']:<8} | ${v['price']:<9.2f} | {v['chg_pct']:<+9.2f}% | ${v['turnover']/1e9:<9.2f}B", flush=True)

        print("===================================================================", flush=True)

    time.sleep(5) # Refresco ultrasónico cada 5 segundos
