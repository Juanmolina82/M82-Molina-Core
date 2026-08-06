import requests, time, os, sys
from datetime import datetime

WATCHLIST = ["SQQQ", "TQQQ", "OIH", "SPXU", "UVXY", "XLE", "KOSPI"]
LOG_FILE = "logs/flow_tracker.log"

s = requests.Session()
s.headers.update({"User-Agent": "M82-Molina-Core/5.0"})

def fetch(symbol):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1m&range=1d"
    try:
        r = s.get(url, timeout=5).json()
        meta = r['chart']['result'][0]['meta']
        price = meta.get('regularMarketPrice', 0)
        prev = meta.get('chartPreviousClose', price)
        vol = meta.get('regularMarketVolume', 0)
        chg = ((price-prev)/prev*100) if prev else 0
        return price, chg, vol
    except Exception:
        return None

def main():
    print("🔍 [M82 MULTI-TICKER FLOW TRACKER v5.0] ONLINE", flush=True)
    while True:
        try:
            os.system("clear")
            print(f"📊 M82 FLOW TRACKER • {datetime.now().strftime('%H:%M:%S VET')} • WATCHLIST {len(WATCHLIST)}")
            print("="*67)
            for sym in WATCHLIST:
                d = fetch(sym)
                if d:
                    p, c, v = d
                    col = "🟩" if c >= 0 else "🔴"
                    print(f"{col} {sym:<6} ${p:<8.2f} {c:+.2f}% Vol:{v:,}")
                else:
                    print(f"⚪ {sym:<6} [FETCH ERROR]")
            print("="*67)
            time.sleep(30)
        except KeyboardInterrupt:
            sys.exit(0)
        except Exception:
            time.sleep(5)

if __name__ == "__main__":
    main()
