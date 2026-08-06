import yfinance as yf, requests, time, os
from datetime import datetime

TICKERS = ["SNDK","AMD","SMCI","IONQ","SOUN","NET","UBER"]
URL = "https://ntfy.sh/M82-Molina-Alerts"

# Niveles gatillo M82 — tu gamma flip
TRIGGERS = {
    "SNDK": 1400.00,
    "AMD": 185.00,
    "SMCI": 950.00,
    "IONQ": 45.00,
    "SOUN": 6.00,
    "NET": 120.00,
    "UBER": 95.00
}

session = requests.Session()

def send(title, msg):
    for _ in range(3):
        try:
            r = session.post(URL, data=msg.encode(), headers={"Title":title,"Priority":"high","Tags":"rocket,chart_with_upwards_trend"}, timeout=10)
            if r.status_code==200:
                print(f"✅ {title} sent")
                return True
        except Exception as e:
            print(f"Retry {e}")
            time.sleep(2)
    return False

print(f"--- M82 V8.0 LIVE {datetime.now()} ---")
for t in TICKERS:
    try:
        price = yf.Ticker(t).fast_info['last_price']
        trigger = TRIGGERS[t]
        status = "🚀 BREAKOUT" if price >= trigger else "👀 WATCH"
        msg = f"{t} ${price:.2f} {status} | Trigger ${trigger} | {datetime.now().strftime('%H:%M:%S')}"
        print(msg)
        # Solo alerta si rompe trigger o si es SNDK/AMD siempre
        if price >= trigger or t in ["SNDK","AMD"]:
            send(f"{status} {t} ${price:.2f}", msg)
    except Exception as e:
        print(f"❌ {t} error: {e}")
    time.sleep(1.5)

send("M82 V8.0 SCAN COMPLETO", f"Scan {len(TICKERS)} tickers terminado {datetime.now().strftime('%H:%M')}")
