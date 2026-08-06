import requests, time, threading, feedparser
from datetime import datetime

NTFY = "https://ntfy.sh/M82-Molina-Alerts"
KEY = "d9ovqg9r01qh40a77tn0d9ovqg9r01qh40a77tng"
SEEN = set()

def push(t, body):
    if body in SEEN: return
    SEEN.add(body)
    try:
        requests.post(NTFY, data=body.encode(), headers={"Title":t[:110]}, timeout=8)
        print(f"{datetime.now().strftime('%H:%M:%S')} {t}")
    except: pass

def hunt_google_news():
    while True:
        try:
            # Goldman + Brent + WTI + Iran
            feeds = [
                "https://news.google.com/rss/search?q=Goldman+Brent+oil&hl=en-US&gl=US&ceid=US:en",
                "https://news.google.com/rss/search?q=WTI+Brent+OPEC&hl=en-US&gl=US&ceid=US:en",
                "https://news.google.com/rss/search?q=US+Iran+oil+deal&hl=en-US&gl=US&ceid=US:en"
            ]
            for url in feeds:
                d = feedparser.parse(url)
                for e in d.entries[:5]:
                    title = e.title
                    if any(k.lower() in title.lower() for k in ["brent","wti","goldman","opec","iran","hormuz"]):
                        if title not in SEEN:
                            push(f"OIL {title[:85]}", f"{title} | {e.link} | 10:58 VET")
            time.sleep(60)
        except Exception as e:
            print(f"google err {e}")
            time.sleep(60)

def hunt_all_gappers():
    while True:
        try:
            for exchange in ["NASDAQ","NYSE","AMEX"]:
                r = requests.get(f"https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=100&offset=0&exchange={exchange.lower()}&download=true", headers={"User-Agent":"Mozilla/5.0"}, timeout=10).json()
                for row in r.get('data',{}).get('rows',[])[:100]:
                    try:
                        sym = row['symbol']
                        price = float(str(row['lastsale']).replace('$','').replace(',',''))
                        pct = float(row.get('pctchange','0').replace('%','')) if row.get('pctchange') else 0
                        if abs(pct) >= 5 or (price < 10 and abs(pct) >= 3):
                            push(f"{sym} ${price} {pct:+.1f}%", f"{sym} ${price} {pct:+.1f}% ALL-MARKET")
                    except: continue
            time.sleep(60)
        except: time.sleep(60)

print("M82 ALL-MARKET + OIL HUNTER ON - Brent Goldman patch")
threading.Thread(target=hunt_google_news, daemon=True).start()
threading.Thread(target=hunt_all_gappers, daemon=True).start()
while True: time.sleep(10)
