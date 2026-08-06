import requests, time, feedparser
from datetime import datetime

NTFY = "https://ntfy.sh/M82-Molina-Alerts"
KEY = "d9ovqg9r01qh40a77tn0d9ovqg9r01qh40a77tng"
SEEN = set()

def push(title, body, tags="wallstreet"):
    if body in SEEN: return
    SEEN.add(body)
    try:
        r = requests.post(NTFY, data=body.encode(), headers={"Title":title[:100]}, timeout=8)
        print(f"{datetime.now().strftime('%H:%M:%S')} {r.status_code} {title}")
    except Exception as e:
        print(f"ERR {e}")

print("M82 WALLSTREET REALTIME - ON")

while True:
    # FINNHUB NEWS
    try:
        data = requests.get(f"https://finnhub.io/api/v1/news?category=general&token={KEY}", timeout=10).json()
        for n in data[:15]:
            hl = n['headline']
            if any(k.lower() in hl.lower() for k in ["Bezos","AMZN","PLTR","OXY","WTI","Brent","Hormuz","Iran","Gold","KKR","Block","Offering"]):
                if hl not in SEEN:
                    push(f"{hl[:90]}", f"{hl} | {n.get('source','')} {n.get('url','')}")
    except Exception as e:
        print(f"finnhub err {e}")

    # BENZINGA LOW TICKETS
    try:
        d = feedparser.parse("https://www.benzinga.com/feed")
        for e in d.entries[:10]:
            if "Offering" in e.title or "Halt" in e.title or "%" in e.title:
                push(e.title[:90], e.title)
    except: pass

    time.sleep(25)
