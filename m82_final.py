import requests, time, os, concurrent.futures
from datetime import datetime

TOKEN = os.environ.get("BOT_TOKEN")
CHAT = os.environ.get("CHAT_ID")
NTFY = "https://ntfy.sh/M82-ESCUPE"

s = requests.Session()
s.headers.update({"User-Agent": "Mozilla/5.0"})

WATCH = ["PLTR", "CL=F", "GC=F", "EGG", "DIT", "FURY", "SPY", "SMH", "XLE", "SLV"]

def send_all(title, body):
    try:
        s.post(NTFY, data=body.encode('utf-8'), headers={"Title": title[:40], "Priority": "high"}, timeout=5)
    except Exception as e:
        print(f"ERR NTFY {e}")
    try:
        s.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT, "text": f"{title}\n{body}"}, timeout=5)
    except Exception as e:
        print(f"ERR TG {e}")

def get_price(tk):
    try:
        r = s.get(f"https://query1.finance.yahoo.com/v8/finance/chart/{tk}?interval=1m&range=1d", timeout=5)
        j = r.json()
        meta = j['chart']['result'][0]['meta']
        p = float(meta.get('regularMarketPrice') or 0)
        prev = float(meta.get('chartPreviousClose') or p)
        pct = ((p - prev) / prev * 100) if prev else 0
        return tk, p, pct
    except:
        return tk, 0, 0

print("--- M82 TURBO V5 ONLINE ---")
send_all("M82 TURBO ONLINE", "Turbo activo 10 tickers cada 10s - ntfy + telegram")

while True:
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:
            results = list(ex.map(get_price, WATCH))

        msg = []
        for tk, p, pct in results:
            if p == 0:
                continue
            msg.append(f"{tk} ${p:.2f} {pct:+.2f}%")
            if abs(pct) >= 0.5 or tk in ["PLTR", "EGG", "DIT", "FURY", "CL=F"]:
                send_all(f"{tk} {pct:+.1f}%", f"{tk} ${p:.2f} {pct:+.2f}% {datetime.now().strftime('%H:%M:%S VET')}")

        # Pulso cada 60s
        if int(time.time()) % 60 < 12:
            send_all("PULSO M82", "\n".join(msg))

        time.sleep(10)
    except Exception as e:
        print(f"ERR LOOP {e}")
        time.sleep(3)
